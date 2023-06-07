from audioop import avg
from vp_comm_lib_pyapi import *


if __name__ == "__main__":
    
    ## 指定动态库路径
    vp_py = vp_common_pyapi(lib_path="../Debug/lib2_video_process_share_lib.so")
    print("versions", vp_py.pyapi_video_process_ver)
    # send_vp_statistics recv_img send_vp_objs
    test = "send_vp_objs"
    
    if test == "recv_img":
        #### 1. socket接收图像测试 ####
        ## socket初始化,此时为阻塞时等待连接
        vp_py.socket_init()
        print ("val socket: ",vp_py.socket_fd)

        t_sum = 0
        test_count = 10000
        frame_count = 0
        while True:
            ## 2. 获取到图像数据
            flag,frame_header = vp_py.get_img_data()
            if flag < 0:
                print("failed to get img")
                continue;

            ## flag > 0时 vp_py.img_rgb_data 为获取到的图像数据
            # cv2.imshow("hello", vp_py.img_rgb_data)
            # cv2.waitKey(50)
            
            # cv2.imwrite("hello.bmp", vp_py.img_rgb_data)
            # 帧号
            frame_count = vp_py.img_header_infos.frame_count
            # 图像的时间戳
            timestamp = vp_py.img_header_infos.timestamp
            
            t_sum += time.time() - timestamp

            print("py: [%06d, %f] \n" %(frame_count, time.time() - timestamp), end='' ,flush=True)
            print ("img size : [%04d x %04d], resize: [%04d x %04d]" %(
                        vp_py.img_header_infos.img_width,
                        vp_py.img_header_infos.img_height,
                        vp_py.img_header_infos.img_resize_width,
                        vp_py.img_header_infos.img_resize_height,
            ))

            # if(frame_count > test_count):
            #     break

        print("\n",t_sum/frame_count)

    elif test == "send_vp_objs":
        #### 2. msg 发送秒结果测试 ####
        # msg 发送示例代码
        # msg初始化，默认使用msg队列为1234，根据实际配置文件获取
        vp_py.msg_init()
        vp_py.ver_main  = 0x00
        vp_py.ver_sub   = 0x01
        vp_py.ver_fixed = 0x01

        # 目标消息结构体初始化
        # target_infos = target_infos_per()
        target_infos = obj_union()
        
        # 目标个数
        targets_len = 20
        # 目标赋值
        for i in range(0,targets_len):
            target_infos.add(track_id=i,
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
                                img_x= i * 10 + 5,
                                img_y=6,
                                img_len=7,
                                img_wid=8,
                                img_hig=9,
                                img_len_ang=10,
                                img_wid_ang=11,
                                img_hig_ang=12,
                                type=13,
                                confidence=90,
                                lic="京A88888",
                                lane_id = 1
            )

        # 测试使用，实际使用需要使用get_img_data的返回值的第二个参数
        test_frame_header = frame_header_infos()
        test_frame_header.infos.header = 0x5A5A5A5A
        test_frame_header.infos.protocol_ver = 0x00030100
        test_frame_header.infos.img_width = 100
        test_frame_header.infos.img_height = 100
        test_frame_header.infos.img_resize_width = 100
        test_frame_header.infos.img_resize_height = 100
        
        while True:
            # 发送目标结果, test_frame_header在实际使用时，需要将get_img_data的返回值的第二个参数作为输入，必须注意的是，输入的目标信息需要和输入的帧头信息对应，保证帧头和目标结果是同一帧
            vp_py.send_vp_rst(target_infos.targets_list, test_frame_header)
            print("snd")
            time.sleep(1)

    elif test == "send_vp_statistics":
        ## 初始化消息队列
        vp_py.msg_init()
        
        # 测试使用，实际使用需要使用get_img_data的返回值的第二个参数
        test_frame_header = frame_header_infos()
        test_frame_header.header = 0x5A5A5A5A
        test_frame_header.protocol_ver = 0x00030100
        
        ## 测试使用，生成统计数据
        ## 断面统计+断面统计帧头
        test_fracture_header = statistics_fracture_header(
            period= 60,
            len_a= 10,
            len_b= 20,
            len_c= 30,
            lane_num=5
            )
        test_fracture_objs = statistics_fracture_lane_infos()
        for i in range(0, test_fracture_header.infos.lane_num) :
            test_fracture_objs.add(
                lane_id=i,
                car_num=i+10,
                car_a_count=i*2+1,
                car_b_count=i*3+2,
                car_c_count=i*4+3,
                occupacy=10,
                avg_speed=i + 10,
                avg_car_len=i + 20,
                avg_car_head_time=i + 30,
                avg_car_body_time=i + 40
            )

        
        ## 触发统计+触发统计帧头
        test_trigger_header = statistics_trigger_header(trigger_num=3)
        test_trigger_objs = statistics_trigger_lane_infos()
        for i in range (0, test_trigger_header.infos.trigger_num) :
            test_trigger_objs.add(
                obj_id=i,
                lane_id=i+10,
                trigger_lane_position=100 + i,
                speed=200 + i,
                trigger_status=int(i/2)
            )
        
        ## 区域统计+区域统计帧头
        test_area_header = statistics_area_header(
            period=1,
            near_pos=100,
            far_pos=200,
            lane_num=5
        )
        test_area_objs = statistics_area_lane_infos()
        for i in range (0, test_area_header.infos.lane_num):
            test_area_objs.add(
                lane_id=i,
                car_num=10 + i,
                occupacy=20,
                avg_speed=30,
                distribute=40,
                head_car_pos=100,
                head_car_speed=110,
                tail_car_pos=200,
                tail_car_speed=210
            )
        
        ## 排队统计+排队统计帧头
        test_queue_header = statistics_queue_header(
            period=1,
            dis_threshhold=10,
            speed_threshhold=20,
            lane_num=5)
        
        test_queue_objs = statistics_queue_lane_infos()
        for i in range(0, test_queue_header.infos.lane_num) :
            test_queue_objs.add(
                lane_id=i,
                queue_length=10,
                head_car_pos=100,
                tail_car_pos=200,
                queue_num=20
            )
        
        
        while True:
            ## 发送断面统计信息
            print ("send statistic fracture")
            vp_py.send_vp_rst(test_fracture_objs.targets_list, test_frame_header, test_fracture_header, msg_type="statistics_fracture")
            time.sleep(1)
            
            ## 发送触发统计信息
            print ("send statistic trigger")
            vp_py.send_vp_rst(test_trigger_objs.targets_list, test_frame_header, test_trigger_header, msg_type="statistics_trigger")
            time.sleep(1)
            
            # 发送区域统计信息
            print ("send statistic area")
            vp_py.send_vp_rst(test_area_objs.targets_list, test_frame_header, test_area_header, msg_type="statistics_area")
            time.sleep(1)
            
            ## 发送排队统计信息
            print ("send statistic queue")
            vp_py.send_vp_rst(test_queue_objs.targets_list, test_frame_header, test_queue_header, msg_type="statistics_queue")
            time.sleep(1)
            # exit(0)
            
            

