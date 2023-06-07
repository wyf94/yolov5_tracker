import cv2
import torch
import numpy as np


from byte_track.byte_tracker import BYTETracker
from utils.visualize import plot_tracking
from utils.timer import Timer
import argparse

def make_parser():
    parser = argparse.ArgumentParser("ByteTrack Yolo Test!!")

    parser.add_argument("--tsize", default=(608, 1088), type=tuple, help="test image size")
    # tracking args
    parser.add_argument("--track_thresh", type=float, default=0.5, help="tracking confidence threshold")
    parser.add_argument("--track_buffer", type=int, default=30, help="the frames for keep lost tracks")
    parser.add_argument("--match_thresh", type=float, default=0.8, help="matching threshold for tracking")
    parser.add_argument("--min-box-area", type=float, default=10, help="filter out tiny boxes")
    parser.add_argument("--aspect_ratio_thresh", type=float, default=16, help="threshold for filtering out boxes of which aspect ratio are above the given value")

    return parser


args = make_parser().parse_args()
byte_tracker = BYTETracker(args, frame_rate=30)



def get_classes(class_file_name='coco_classes.names'):
    '''loads class name from a file'''
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names



def draw_bboxes(image, bboxes, color, line_thickness,  classes=get_classes()):
    line_thickness = line_thickness or round(
        0.002 * (image.shape[0] + image.shape[1]) * 0.5) + 1

    list_pts = []
    point_radius = 4
    for (x1, y1, x2, y2, score, cls_id, pos_id) in bboxes:
        classes_name = classes[int(cls_id)]

        # 撞线的点
        check_point_x = int(x1 + ((x2 - x1) * 0.5))
        check_point_y = y2

        c1, c2 = (int(x1), int(y1)), (int(x2), int(y2))
        cv2.rectangle(image, c1, c2, color, thickness=line_thickness, lineType=cv2.LINE_AA)

        font_thickness = max(line_thickness - 1, 1)
        
        t_size = cv2.getTextSize(classes_name, 0, fontScale=line_thickness / 1, thickness=font_thickness)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(image, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(image, '{} ID-{}'.format(classes_name, int(pos_id)), (c1[0], c1[1] - 2), 0, line_thickness / 1,
                    [0, 0, 0], thickness=font_thickness, lineType=cv2.LINE_AA)

        list_pts.append([check_point_x - point_radius, check_point_y - point_radius])
        list_pts.append([check_point_x - point_radius, check_point_y + point_radius])
        list_pts.append([check_point_x + point_radius, check_point_y + point_radius])
        list_pts.append([check_point_x + point_radius, check_point_y - point_radius])

        ndarray_pts = np.array(list_pts, np.int32)

        cv2.fillPoly(image, [ndarray_pts], color=(0, 0, 255))

        list_pts.clear()

    return image



def update(bboxes, image_size):
    # bboxes(x1, y1, x2, y2, obj_conf, class_conf, class_pred)
    track_bbox = []
    if len(bboxes) != 0:
        online_targets = byte_tracker.update(bboxes, image_size, args.tsize)
        online_tlwhs = []
        online_tids = []
        online_cids = []
        online_scores = []
        for t in online_targets:
            tlwh = t.tlwh
            tid = t.track_id 
            cid = t.class_id
            vertical = tlwh[2]/tlwh[3] > args.aspect_ratio_thresh
            if tlwh[2] * tlwh[3] > args.min_box_area and not vertical:
                online_tlwhs.append(tlwh)
                online_tids.append(tid)
                online_cids.append(cid)
                online_scores.append(t.score)

        for i, tlwh in enumerate(online_tlwhs):
            x1, y1, w, h = tlwh
            # intbox = tuple(map(int, (x1, y1, x1 + w, y1 + h)))s
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x1 + w)
            y2 = int(y1 + h)
            track_id = int(online_tids[i])
            calss_id = int(online_cids[i])
            score = float(online_scores[i])
            bbox = [x1, y1, x2, y2, score, calss_id, track_id]
            track_bbox.append(bbox)
    track_bbox = np.array(track_bbox)
    
    
    return track_bbox
