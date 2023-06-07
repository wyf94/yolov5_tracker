import numpy as np

import tracker
from detector import Detector
import cv2
import time 
import json
from config.taffic_config import TRACK_CLASSES_LIST as list_track_classes
import traffic_count.traffic_count_utils as traffic_count

import byte_tracker

def read_json(polygon_path):
    '''
    读取json文件 获取碰撞线collision_lines, 统计区域polygons
    '''
    f = open(polygon_path, encoding="UTF-8")
    file = json.load(f)
    lines = file['reference_point']['collision_lines']
    polygons = file['reference_point']['measure_filter_range']
    return lines, polygons


def image_mask(list_point, color_value, size):
    '''
    生成包含值为color_value的多边形，尺寸为size的mask
    :param point_list_first: [(x1，y1), (x2，y2), ... , (xn，yn)]
    :param color_value: 1-255
    :param size: (x，y) 
    :return: mask.
    '''
    # 根据视频尺寸，填充一个polygon，供撞线计算使用
    mask_image_temp = np.zeros(size, dtype=np.uint8)

    # 初始化撞线polygon
    ndarray_pts = np.array(list_point, np.int32)
    polygon_color_value = cv2.fillPoly(mask_image_temp, [ndarray_pts], color=color_value)
    polygon_color_value = polygon_color_value[:, :, np.newaxis]

    return polygon_color_value

def regional_statistics(area_points, bboxes, image_size):
    
    area_object = []
    
    roi_mask_value = image_mask(area_points, 1, image_size)
    for i in range(0, len(bboxes)):
        x1, y1, x2, y2, score, calss_id, track_id = bboxes[i]
        
        # 撞线的点(矩形下边的中心点)
        x = int(x1 + ((x2 - x1) * 0.5))
        if y2 >= image_size[0]:
            y = image_size[0] - 1
        else:
            y = int(y2)
        # print("x: ", x, "y: ", y)

        # 判断车辆（中心点）是否在roi区域
        if roi_mask_value[y, x] == 1:
            area_object.append(list(bboxes[i]))
            # print(bboxes[i])
            # print(" object in.")
    
    return area_object

def line_intersecting(line1, line2):
    x1, y1, x2, y2 = line1[0][0], line1[0][1], line1[1][0], line1[1][1]
    x3, y3, x4, y4 = line2[0][0], line2[0][1], line2[1][0], line2[1][1]

    # 计算向量
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3

    # 计算向量叉积
    cross_product = dx1 * dy2 - dx2 * dy1

    # 判断是否平行或共线
    if cross_product == 0:
        return False

    # 计算交点的参数
    t1 = ((x3 - x1) * dy2 - (y3 - y1) * dx2) / cross_product
    t2 = ((x3 - x1) * dy1 - (y3 - y1) * dx1) / cross_product

    # 判断交点是否在两条线段之间
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        return True

    return False

def lane_change_detect(lane_line, bboxes,  image_size):
    lane_change_info = []
    for i in range(0, len(bboxes)):
        x1, y1, x2, y2, score, calss_id, track_id = bboxes[i]
        point1_x = int(x1 + ((x2 - x1) * 0.25))
        
        point2_x = int(x2 - ((x2 - x1) * 0.25))
        if y2 >= image_size[0]:
            y = image_size[0] - 1
        else:
            y = int(y2)
        
        car_line = [(point1_x, y), (point2_x, y)]
        car_line = np.array(car_line)
        lane_change = line_intersecting(car_line, lane_line)
        if lane_change:
            lane_change_info.append(bboxes[i])

    return lane_change_info

if __name__ == '__main__':

    # 读取josn文件里的lines, polygons  
    polygon_path = "config/polygon.json" 
    lines, polygons = read_json(polygon_path)
    multi_line = [[0] for i in range(len(lines))]

    count = 0
    for line in lines:
        multi_line[count] = line['points']
        count = count + 1
        print(multi_line[count-1])  
    
    print(multi_line)
    # 视频文件的名称和编解码器
    filename = 'output.mp4'
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    width = 1920
    height = 1080
    is_color = True
    # 创建VideoWriter对象
    video_writer = cv2.VideoWriter(filename, codec, 30, (width, height), is_color)

    blue_list = [[] for i in range(len(lines))]
    yellow_list = [[] for i in range(len(lines))]
    up_count = np.zeros((len(lines),  len(list_track_classes)))
    down_count = np.zeros((len(lines),  len(list_track_classes)))

    roi_color =  [(0,0,255),(255,0,0),(0,255,0),(255,0,255),(225,255,0),(0,255,255), (0,0,0)]


    # 初始化 yolov5
    detector = Detector()
    
    # 打开视频
    # capture = cv2.VideoCapture('./video/test.mp4')
    # capture = cv2.VideoCapture('/home/wyf/wyf_2023/PaddleDetection/video/1_1080.mp4')
    capture = cv2.VideoCapture('/home/wyf/wyf_2023/video/001-20230302123112936.mp4')

    emergency_lane = [[760,514],[957,497],[588,34],[542,39]]
    # lane_line = [(760,514),(536,31)]
    lane_line = [(1508,1028),(1072,62)]
    illegal_area = [[13,218],[10,328],[137,361],[337,106],[267,105],[198,96]]
    
    # emergency_lane = [[372,214],[438,214],[352,90],[333,90]]
    # # lane_line = [(367,207),(331,82)]
    # lane_line = [(1468,828),(1324,328)]
    # illegal_area = [[55,184],[93,214],[161,214],[248,128],(181,126)]
    
    
    emergency_lane = np.array(emergency_lane, np.int32)
    emergency_lane = emergency_lane*2
    emergency_lane = emergency_lane.reshape((-1, 1, 2))
    illegal_area = np.array(illegal_area, np.int32)
    illegal_area = illegal_area*2
    illegal_area = illegal_area.reshape((-1, 1, 2))
    while True:
        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break
        img_size = im.shape[0:2]
        # 缩小尺寸，1920x1080->960x540
        # im = cv2.resize(im, (960, 540))

        list_bboxs = []
        t1 = time.time()
        bboxes = detector.detect(im)
        # print(bboxes)
        bboxes = np.array(bboxes)
        
        cv2.line(im, lane_line[0], lane_line[1],(0, 0, 255), 2)
        cv2.polylines(im, [emergency_lane], True, (0,255,0), thickness=2)
        cv2.polylines(im, [illegal_area], True, (0,0,255), thickness=2)
        # tracker_bboxes = []

        # for i in range(0, len(bboxes)):
        #     cls = bboxes[i][4]
        #     if cls in list_track_classes:
        #         tracker_bboxes.append(bboxes[i])
        
        # tracker_bboxes = np.array(tracker_bboxes)
        
        # 如果画面中 有bbox
        if len(bboxes) > 0:
            # list_bboxs = tracker.update(tracker_bboxes, im)
            
            list_bboxs = byte_tracker.update(bboxes, img_size)
            # print(list_bboxs)

            # 画框
            # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
            output_image_frame = byte_tracker.draw_bboxes(im, list_bboxs, color=(0,255,0), line_thickness=1)
            # output_image_frame = im
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass
        
        t2 = time.time()
        
        illegal_object = regional_statistics(illegal_area, list_bboxs, img_size)
        area_object = regional_statistics(emergency_lane, list_bboxs, img_size)
        lane_change_info = lane_change_detect(lane_line, list_bboxs, img_size)
        output_image_frame = byte_tracker.draw_bboxes(output_image_frame, lane_change_info, color=(0,0,255), line_thickness=1)
        output_image_frame = byte_tracker.draw_bboxes(output_image_frame, illegal_object, color=(255,0,0), line_thickness=1)
        output_image_frame = byte_tracker.draw_bboxes(output_image_frame, area_object, color=(255,0,0), line_thickness=1)
        # for i in range(len(lane_change_info)):
        #     print("track_id : ", lane_change_info[i][6])
        # print("------------------------")

        # # print("time: ", int((t2-t1)*1000))

        # # # 输出图片
        # # # output_image_frame = cv2.add(output_image_frame, color_polygons_image)
    

        # padding = [0, 100]
        # size = [2048, 2448]
        # # 各个类别穿过每条线的统计情况
        # Line_statistics = []
        
        # for index in range(0, len(multi_line)):
        #     # 判断line中点加上padding之后是否超出图片范围
        #     for i in range(0, 2):
        #         if multi_line[index][i][0]+padding[0] >= size[1] or multi_line[index][i][0]+padding[0] <= 0:
        #             print(" The point of lines out off range or padding out off range")
        #         if multi_line[index][i][1]+padding[1] >= size[0] or multi_line[index][i][1]+padding[1] <= 0:
        #             print(" The point of lines out off range or padding out off range")

        #     # 周期性统计各个类别穿过每条线的情况
        #     polygon_mask_blue_and_yellow, polygon_color_image = traffic_count.line2polygon(multi_line[index], padding, size, True)
        
        #     up_count[index], down_count[index] = traffic_count.traffic_count(list_bboxs, size,  list_track_classes,  polygon_mask_blue_and_yellow, 
        #                                                                      blue_list[index], yellow_list[index],  up_count[index], down_count[index])
        #     output_image_frame = cv2.add(output_image_frame, polygon_color_image)
            
        # for index in range(0, len(multi_line)):
        #         # cv_image = cv2.add(cv_image, polygon_color_image)
        #         ptStart = (multi_line[index][0][0], multi_line[index][0][1])
        #         ptEnd = (multi_line[index][1][0], multi_line[index][1][1])
        #         cv2.line(im, ptStart, ptEnd, color=roi_color[index], thickness=5)

        #         text_draw = 'line' + str(index) + ': \n' 
        #         for i in range(0, len(list_track_classes)):
        #             text_draw = text_draw + list_track_classes[i] + ': ' + str(up_count[index][i] + down_count[index][i]) + '\n'
        #         for i, line in enumerate(text_draw.split('\n')):
        #             dy = 30
        #             draw_text_postion = (multi_line[index][0][0], (multi_line[index][0][1] - 180 + dy*i))
        #             im = cv2.putText(img=im, text=line,
        #                                 org=draw_text_postion,
        #                                 fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #                                 fontScale=1, color=(255, 0, 0), thickness=2)

        video_writer.write(output_image_frame)

        result_image = cv2.resize(output_image_frame, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('demo', result_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        pass
    pass

    # 释放VideoWriter和摄像头或文件资源
    video_writer.release()
    capture.release()
    cv2.destroyAllWindows()     
