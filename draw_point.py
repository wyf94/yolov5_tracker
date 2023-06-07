import numpy as np

import tracker
from detector import Detector
import cv2
import time 
import json


# 鼠标点击获取坐标
def on_EVENT_LBUTTONDOWN(self, event, x, y,flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("location:({0},{1})".format(x,y))

if __name__ == '__main__':

    # 打开视频
    # capture = cv2.VideoCapture('./video/test.mp4')
    capture = cv2.VideoCapture('/home/wyf/wyf_2023/PaddleDetection/video/1_1080.mp4')


    while True:
        # 读取每帧图片
        _, im = capture.read()
        if im is None:
            break

        # 缩小尺寸，1920x1080->960x540
        im = cv2.resize(im, (960, 540))

        list_bboxs = []
        t1 = time.time()

        # 如果画面中 有bbox
        if len(bboxes) > 0:
            list_bboxs = tracker.update(bboxes, im)

            # 画框
            # 撞线检测点，(x1，y1)，y方向偏移比例 0.0~1.0
            output_image_frame = tracker.draw_bboxes(im, list_bboxs, line_thickness=1)
            pass
        else:
            # 如果画面中 没有bbox
            output_image_frame = im
        pass
        
        t2 = time.time()

        print("time: ", int((t2-t1)*1000))


        cv2.imshow('demo', output_image_frame)
        cv2.waitKey(1)

        pass
    pass

    capture.release()
    cv2.destroyAllWindows()     
