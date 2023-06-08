import numpy as np
import cv2
import math
import time 
from traffic_count.yolo_classes import CLASSES_LIST


def image_mask(list_point, color_value, size):
    '''
    生成包含值为color_value的多边形, 尺寸为size的mask
    :param point_list_first: [(x1, y1), (x2, y2), ... , (xn, yn)]
    :param color_value: 1-255
    :param size: (x, y) 
    :return: mask.
    '''
    # 根据视频尺寸, 填充一个polygon, 供撞线计算使用
    mask_image_temp = np.zeros(size, dtype=np.uint8)

    # 初始化撞线polygon
    ndarray_pts = np.array(list_point, np.int32)
    polygon_color_value = cv2.fillPoly(mask_image_temp, [ndarray_pts], color=color_value)
    polygon_color_value = polygon_color_value[:, :, np.newaxis]

    return polygon_color_value

def polygon_mask(point_list_first, point_list_second, size):
    '''
    生成合并两个多边形, 尺寸为size的mask
    :param point_list_first: [(x1, y1), (x2, y2), ... , (xn, yn)]
    :param point_list_second: [(x1, y1), (x2, y2), ... , (xn, yn)]
    :param size: (x, y) 
    :return: 不设置颜色的mask, 设置颜色的mask.
    '''
    polygon_value_first = image_mask(point_list_first, 1, size)
    polygon_value_second = image_mask(point_list_second, 2, size)
    
    # 撞线检测用mask, 包含2个polygon, （值范围 0、1、2）, 供撞probability线计算使用
    polygon_mask_first_and_second = polygon_value_first + polygon_value_second

    # set the first  polygon to blue
    blue_color_plate = [255, 0, 0]
    blue_image = np.array(polygon_value_first * blue_color_plate, np.uint8)
    # set the first  polygon to yelllow
    yellow_color_plate = [0, 255, 255]
    yellow_image = np.array(polygon_value_second * yellow_color_plate, np.uint8)
    # 彩色图片（值范围 0-255）用于图片显示
    polygon_color_image = blue_image + yellow_image

    return polygon_mask_first_and_second,  polygon_color_image

def  line2polygon(line, padding, size, show_image = True):
    '''
    以碰撞线为分界线, 将碰撞线填充为两个值分别为1, 2的矩形, 同时生成包含矩形, 尺寸为size的mask
    :param line: (x, y) 
    :param padding: (x, y) 
    :param size: (x, y) 
    :return: 不设置颜色的mask, 设置颜色的mask.
    '''
    width, height = padding[0], padding[1]
    polygon_0  = [line[0], line[1], [line[1][0] + width, line[1][1] + height], [line[0][0] + width, line[0][1] + height]]
    polygon_1  = [line[0], line[1], [line[1][0] - width, line[1][1] - height], [line[0][0] - width, line[0][1] - height]]
    polygon_value_first = image_mask(polygon_0, 1, size)
    polygon_value_second = image_mask(polygon_1, 2, size)
    polygon_mask_first_and_second = polygon_value_first + polygon_value_second

    if show_image:
        # set the first  polygon to blue
        blue_color_plate = [255, 0, 0]
        blue_image = np.array(polygon_value_first * blue_color_plate, np.uint8)
        # set the first  polygon to yelllow
        yellow_color_plate = [0, 255, 255]
        yellow_image = np.array(polygon_value_second * yellow_color_plate, np.uint8)
        polygon_color_image = blue_image + yellow_image
    else:
        polygon_color_image = 0
    
    return polygon_mask_first_and_second,  polygon_color_image


def roi_count_queue(roi_point, list_bboxes, list_classes, stop_point, color, size, queue_speed):
    """
    统计全图各个类别的数量。
    :param roi_point: [(x1, y1), (x2, y2), ... , (xn, yn)] 统计的roi区域
    :param list_bboxes: BoundingBoxs list
    :param list_classes: Classes list
    :param stop_point: 区域的停车点(起始点)
    :param color: [x, x, x], x = 0-255
    :param size: (x, y)
    :param queue_speed: v 判断是否为排队的平均速度
    :param is_show_image: true/false 
    :return: 区域内各个类别的数量,  设置颜色的roi图,  区域统计信息, 排队信息.
    """
    class_num = [0]*len(list_classes)

    roi_mask_value = image_mask(roi_point, 1, size)

    # if is_show_image:
    #     # set the roi to red
    #     color_plate = color
    #     roi_color_image = np.array(roi_mask_value * color_plate, np.uint8)
    # else:
    #     roi_color_image = 0

    area_info = {}
    queue_up_info = {}
    distances = []
    roi_v = []

    for i in range(0, len(list_bboxes)):
        cls = list_bboxes[i].target_class
        if cls in list_classes:
            track_id = list_bboxes[i].id
            x1 = list_bboxes[i].xmin
            y1 = list_bboxes[i].ymin
            x2 = list_bboxes[i].xmax
            y2 = list_bboxes[i].ymax
            ground_x = list_bboxes[i].x
            ground_y = list_bboxes[i].y
            vx = list_bboxes[i].vx
            vy = list_bboxes[i].vy

            # print("list_bboxes",list_bboxes[i])
            # 撞线的点(矩形下边的中心点)
            x = int(x1 + ((x2 - x1) * 0.5))
            if y2 >= size[0]:
                y = size[0] - 1
            else:
                y = int(y2)
            # print("x: ", x, "y: ", y)

            # 判断车辆（中心点）是否在roi区域
            if roi_mask_value[y, x] == 1:
                cls_index = list_classes.index(cls)
                class_num[cls_index] += 1

                dis = math.sqrt(math.pow(ground_x - stop_point[0], 2) + math.pow(ground_y - stop_point[1], 2))
                v =round(math.sqrt(vx*vx + vy*vy), 2)
                distances.append(dis)
                roi_v.append(v)

    classified_statistic =[]
    sum_car = 0
    for i in range(0, len(list_classes)):
        sum_car += class_num[i]
        classified_count = {
            "class":list_classes[i],
            "num":class_num[i]
        }
        classified_statistic.append(classified_count)   
    
    if sum_car > 0:
        max_dis = max(distances)
        min_dis = min(distances)

        tail_index = distances.index(max_dis)
        head_index = distances.index(min_dis)
        tail_v = roi_v[tail_index]
        head_v = roi_v[head_index]

        mean_v = np.mean(roi_v)
        mean_dis = (max_dis - min_dis) / len(distances)

        area_info = {
            "car_num": sum_car,
            "count_list": classified_statistic,
            "ave_car_speed": round(mean_v, 2),
            "car_distribute": round(mean_dis, 2),
            "head_car_pos": round(min_dis, 2),
            "head_car_speed": round(head_v, 2),
            "tail_car_pos": round(max_dis, 2),
            "tail_car_speed": round(tail_v, 2),
        }

        if mean_v < queue_speed:
            queue_up_info = {
                "queue_len": round(max_dis, 2),
                "head_car_pos": round(min_dis, 2),
                "tail_car_pos": round(max_dis, 2),
                "car_count": len(distances)
                }
        else:
            queue_up_info = {
                "queue_len": 0,
                "head_car_pos": 0,
                "tail_car_pos": 0,
                "car_count": 0
                }
    return class_num, area_info, queue_up_info

def image_count(list_bboxes, list_classes):
    """
    统计全图各个类别的数量。
    :param list_bboxes: BoundingBoxs list
    :param list_classes: Classes list
    :return: 各个类别的数量.
    """
    class_num = [0]*len(list_classes)
  
    for i in range(0, len(list_bboxes)):
        x1 = list_bboxes[i].xmin
        y1 = list_bboxes[i].ymin
        x2 = list_bboxes[i].xmax
        y2 = list_bboxes[i].ymax
        cls = list_bboxes[i].target_class
        # 撞线的点(中心点)
        x = int(x1 + ((x2 - x1) * 0.5))
        y = int(y1 + ((y2 - y1) * 0.5))

        cls_index = list_classes.index(cls)
        class_num[cls_index] += 1

    return class_num


# def bboxes_mask(tracks_msg,  size,  color_value = 1):
#     img_bboxes_mask = np.zeros(size, dtype=np.uint8)
#     img_bboxes_mask = img_bboxes_mask[:, :, np.newaxis]

#     if len(tracks_msg.data) > 0:
#         for i in range(0, len(tracks_msg.data)):
#             x1 = tracks_msg.data[i].xmin
#             y1 = tracks_msg.data[i].ymin
#             x2 = tracks_msg.data[i].xmax
#             y2 = tracks_msg.data[i].ymax
#             point_list = [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]
#             bboxes_mask = image_mask(point_list, 1, size)
#             img_bboxes_mask += bboxes_mask

#     # set the first  polygon to yelllow
#     yellow_color_plate = [255, 255, 255]
#     yellow_image = np.array(img_bboxes_mask * yellow_color_plate, np.uint8)

#     return img_bboxes_mask, yellow_image

def compute_IOU(rec1,rec2):
    """
    计算两个矩形框的交并比。
    :param rec1: (x0,y0,x1,y1)      (x0,y0)代表矩形左上的顶点, （x1,y1）代表矩形右下的顶点。下同。
    :param rec2: (x0,y0,x1,y1)
    :return: 交并比IOU.
    """
    left_column_max  = max(rec1[0],rec2[0])
    right_column_min = min(rec1[2],rec2[2])
    up_row_max       = max(rec1[1],rec2[1])
    down_row_min     = min(rec1[3],rec2[3])
    #两矩形无相交区域的情况
    if left_column_max>=right_column_min or down_row_min<=up_row_max:
        return 0
    # 两矩形有相交区域的情况
    else:
        S1 = (rec1[2]-rec1[0])*(rec1[3]-rec1[1])
        S2 = (rec2[2]-rec2[0])*(rec2[3]-rec2[1])
        S_cross = (down_row_min-up_row_max)*(right_column_min-left_column_max)
        return S_cross/(S1+S2-S_cross)

def occupancy(tracks_msg, line, padding, line_occupy_flag, line_occupy_time):
    '''
    判断碰撞线上是否有车辆占据
    :param tracks_msg:  订阅的追踪数据话题
    :param line: (x0,y0,x1,y1) 
    :param padding: (x, y) line填充为矩形的长宽
    :param line_occupy_flag: list 每帧是否存在碰撞线被占据
    :param line_occupy_flag: list 记录占据时间
    :return: 碰撞线占据list.
    '''
    l_x1, l_y1, l_x2, l_y2 = line[0][0], line[0][1], line[1][0], line[1][1]
    rec1 = (l_x1, l_y1, l_x2 + padding[0] , l_y2 + padding[1])
    
    occupy_flag = 0
    # 计算boundingboxes和由线填充的矩形之间的交并比, 如果大于0, 则相交
    if len(tracks_msg.data) > 0:
        for i in range(0, len(tracks_msg.data)):
            track_id = tracks_msg.data[i].id
            x1 = tracks_msg.data[i].xmin
            y1 = tracks_msg.data[i].ymin
            x2 = tracks_msg.data[i].xmax
            y2 = tracks_msg.data[i].ymax
            rec2 = (x1, y1, x2, y2)
            iou = compute_IOU(rec1,rec2)
            if iou > 0:
                occupy_flag |= 1

    #  判断boundingboxes是否与检测线相交, 如果相交则为有车存在, 并记录有车->无车, 无车->有车的时间点
    if (line_occupy_flag == 0 and occupy_flag ==1) or (line_occupy_flag == 1 and occupy_flag == 0):
        line_occupy_time.append(tracks_msg.header.stamp.sec)
    #
    if occupy_flag:
        line_occupy_flag = 1
    else:
        line_occupy_flag = 0

    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print("line_occupy_time: ", line_occupy_time)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    return line_occupy_flag


def traffic_count(bboxes, size, list_classes,  polygon_mask_first_and_second, first_list, second_list, up_count, down_count):
    """
    统计通过碰撞线的数量。
    :param tracks_msg:  追踪话题
    :param size: (x, y)
    :param list_classes: Classes list
    :param polygon_mask_first_and_second: 包含的mask
    :param first_list:  通过第一个矩形的track—id
    :param second_list: 通过第二个矩形的track—id
    :param up_count: 1--->2 方向的通过数量
    :param down_count: 2--->1 方向的通过数量
    :return: 1--->2 方向的通过数量,  2--->1 方向的通过数量.
    """
    if len(bboxes) > 0:
        for i in range(0, len(bboxes)):
            cls_id = int(bboxes[i][5])
            cls = CLASSES_LIST[cls_id]
            
            # print("{}:{}".format(cls, cls_id))
            if cls in list_classes:
                cls_index = list_classes.index(cls)
                # print(bboxes[i])
                # x1, y1, x2, y2, cls, track_id = bboxes[i]
                
                x1, y1, x2, y2, score, calss_id, track_id = bboxes[i]

                # 撞线的点(矩形下方中心点)
                x = int(x1 + ((x2 - x1) * 0.5))
                if y2 >= size[0]:
                    y = size[0] - 1
                else:
                    y = int(y2)

                # 判断目标在是否在多边形0和1内
                if polygon_mask_first_and_second[y,x]==1 or polygon_mask_first_and_second[y, x] == 3:
                    # 记录通过第一个polygon的时间戳以及速度
                    # 如果撞 第一个 polygon
                    if track_id not in first_list:
                        first_list.append(track_id)
                    # 判断 第二个 polygon list 里是否有此 track_id
                    # 有此 track_id, 则 认为是 2--->1 方向
                    if track_id in second_list:
                        # 2--->1方向 +1
                        down_count[cls_index] += 1
                        print('2--->1 count:', down_count, ', 2--->1 id:', second_list)
                        print("calss: ", cls)
                        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                        # 删除 第二个polygon list 中的此id
                        second_list.remove(track_id)


                elif polygon_mask_first_and_second[y, x] == 2:
                    # 如果撞第二个 polygon
                    if track_id not in second_list:
                        second_list.append(track_id)
                    # 判断第一个polygon list 里是否有此 track_id
                    # 有此 track_id, 则 认为是 1--->2 方向
                    if track_id in first_list:
                        #  1--->2 方向 +1
                        up_count[cls_index] += 1
                        print('1--->2 count:', up_count, ', 1--->2  id:', first_list)
                        print("calss: ", cls)
                        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                        # 删除 第一个polygon list 中的此id
                        first_list.remove(track_id)

        # ----------------------清除无用id----------------------
        list_overlapping_all = second_list + first_list
        for id in list_overlapping_all:
            is_found = False
            for _, _, _, _, _, _, bbox_id in bboxes:
                if bbox_id == id:
                    is_found = True
                    break

            if not is_found:
                # 如果没找到, 删除id
                if id in second_list:
                    second_list.remove(id)
                if id in first_list:
                    first_list.remove(id)
        list_overlapping_all.clear()



    else:
        # 如果图像中没有任何的bbox, 则清空list
        first_list.clear()
        second_list.clear()

    return up_count, down_count

