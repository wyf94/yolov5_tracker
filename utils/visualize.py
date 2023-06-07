#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cv2
import numpy as np

# load project labels
categories = ['bicycle', 'fire-extinguisher', 'person', 'reflective-clothes', 'safety-triangle', 'speed-bump', 'traffic-cone', 'vehicle']

_COLORS = np.array(
    [
        0.000, 0.447, 0.741,
        0.850, 0.325, 0.098,
        0.929, 0.694, 0.125,
        0.494, 0.184, 0.556,
        0.466, 0.674, 0.188,
        0.301, 0.745, 0.933,
        0.635, 0.078, 0.184,
        0.300, 0.300, 0.300,
        0.600, 0.600, 0.600,
        1.000, 0.000, 0.000,
        1.000, 0.500, 0.000,
        0.749, 0.749, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 1.000,
        0.667, 0.000, 1.000,
        0.333, 0.333, 0.000,
        0.333, 0.667, 0.000,
        0.333, 1.000, 0.000,
        0.667, 0.333, 0.000,
        0.667, 0.667, 0.000,
        0.667, 1.000, 0.000,
        1.000, 0.333, 0.000,
        1.000, 0.667, 0.000,
        1.000, 1.000, 0.000,
        0.000, 0.333, 0.500,
        0.000, 0.667, 0.500,
        0.000, 1.000, 0.500,
        0.333, 0.000, 0.500,
        0.333, 0.333, 0.500,
        0.333, 0.667, 0.500,
        0.333, 1.000, 0.500,
        0.667, 0.000, 0.500,
        0.667, 0.333, 0.500,
        0.667, 0.667, 0.500,
        0.667, 1.000, 0.500,
        1.000, 0.000, 0.500,
        1.000, 0.333, 0.500,
        1.000, 0.667, 0.500,
        1.000, 1.000, 0.500,
        0.000, 0.333, 1.000,
        0.000, 0.667, 1.000,
        0.000, 1.000, 1.000,
        0.333, 0.000, 1.000,
        0.333, 0.333, 1.000,
        0.333, 0.667, 1.000,
        0.333, 1.000, 1.000,
        0.667, 0.000, 1.000,
        0.667, 0.333, 1.000,
        0.667, 0.667, 1.000,
        0.667, 1.000, 1.000,
        1.000, 0.000, 1.000,
        1.000, 0.333, 1.000,
        1.000, 0.667, 1.000,
        0.333, 0.000, 0.000,
        0.500, 0.000, 0.000,
        0.667, 0.000, 0.000,
        0.833, 0.000, 0.000,
        1.000, 0.000, 0.000,
        0.000, 0.167, 0.000,
        0.000, 0.333, 0.000,
        0.000, 0.500, 0.000,
        0.000, 0.667, 0.000,
        0.000, 0.833, 0.000,
        0.000, 1.000, 0.000,
        0.000, 0.000, 0.167,
        0.000, 0.000, 0.333,
        0.000, 0.000, 0.500,
        0.000, 0.000, 0.667,
        0.000, 0.000, 0.833,
        0.000, 0.000, 1.000,
        0.000, 0.000, 0.000,
        0.143, 0.143, 0.143,
        0.286, 0.286, 0.286,
        0.429, 0.429, 0.429,
        0.571, 0.571, 0.571,
        0.714, 0.714, 0.714,
        0.857, 0.857, 0.857,
        0.000, 0.447, 0.741,
        0.314, 0.717, 0.741,
        0.50, 0.5, 0
    ]
).astype(np.float32).reshape(-1, 3)


def get_color(idx):
    idx = idx * 3
    color = ((37 * idx) % 255, (17 * idx) % 255, (29 * idx) % 255)

    return color


def plot_tracking(image, tlwhs, obj_ids, calss_ids, scores=None, frame_id=0, spend_time=(0,0,0), ids2=None):
    im = np.ascontiguousarray(np.copy(image))
    im_h, im_w = im.shape[:2]

    top_view = np.zeros([im_w, im_w, 3], dtype=np.uint8) + 255

    #text_scale = max(1, image.shape[1] / 1600.)
    #text_thickness = 2
    #line_thickness = max(1, int(image.shape[1] / 500.))
    text_scale = 2
    text_thickness = 2
    line_thickness = 3
    t1,t2,t3 = spend_time
    radius = max(5, int(im_w/140.))
    # cv2.putText(im, 'frame: %d fps: %.2f num: %d' % (frame_id, fps, len(tlwhs)),
    #             (0, int(15 * text_scale)), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), thickness=2)
    if t3 != t1:
        fps = (1. / (t3 - t1)) 
    else:
        fps = -1
    cv2.putText(im, 'FPS: {:.2f}'.format(fps), (50, 40), 0, 1, (255,0,0), 2)

    cv2.putText(im, 'Detector_Time: {:.3f}ms'.format((t2 - t1)*1e3), (50, 80), 0, 1, (255,0,0), 2)
    cv2.putText(im, 'Tracker_Time: {:.3f}ms'.format((t3 - t2)*1e3), (50, 120), 0, 1, (255,0,0), 2)
    cv2.putText(im, 'Image_Shape: {} X {}'.format(im.shape[0],im.shape[1]), (50, 160), 0, 1, (255,0,0), 2)

    for i, tlwh in enumerate(tlwhs):
        x1, y1, w, h = tlwh
        intbox = tuple(map(int, (x1, y1, x1 + w, y1 + h)))
        obj_id = int(obj_ids[i])
        calss_id = int(calss_ids[i])
        id_text = '{} {:.2f}'.format(
            int(obj_id), scores[i]) if scores is not None else '{}-{}'.format(int(obj_id),str(categories[calss_id]))
        if ids2 is not None:
            id_text = id_text + ', {}'.format(int(ids2[i]))
        color = get_color(abs(obj_id))
        cv2.rectangle(im, intbox[0:2], intbox[2:4],
                      color=color, thickness=line_thickness)
        cv2.putText(im, id_text, (intbox[0], intbox[1]), cv2.FONT_HERSHEY_PLAIN, text_scale, (255,0,0),
                    thickness=text_thickness)
    return im


def add_vp_objs(vp_objs, tlwhs, obj_tids, obj_cids, tids_lpr, scores):
    # add_vp_objs(target_infos, online_tlwhs, online_tids, online_cids, tids_lpr=tids_lpr, scores=online_scores, frame_id=frame_id + 1, spend_time=spend_time)

    print("\033[0;31;40m  obj nums: {} \033[0m".format(len(tlwhs)))   

    for i, tlwh in enumerate(tlwhs):
        x1, y1, w, h = tlwh
        
        obj_tid = int(obj_tids[i])
        obj_cid = int(obj_cids[i])
        score = int(scores[i])
   
        if tids_lpr: 
            lic = tids_lpr.get(obj_tid, "")
            if lic:
                print("lic : {}".format(lic))
        else:
            lic = ""
        
        
        vp_objs.add(track_id=obj_tid,
                            x=1,
                            y=1,
                            z=1,
                            vx=2,
                            vy=2,
                            vz=2,
                            length=3,
                            width=3,
                            height=3,
                            azimuth=4,
                            img_x= int(x1),
                            img_y=int(y1),
                            img_len=7,
                            img_wid=int(w),
                            img_hig=int(h),
                            img_len_ang=10,
                            img_wid_ang=11,
                            img_hig_ang=12,
                            type=obj_cid + 1,
                            confidence=score,
                            lic=lic,
                            lane_id=0
                )
    

    return vp_objs