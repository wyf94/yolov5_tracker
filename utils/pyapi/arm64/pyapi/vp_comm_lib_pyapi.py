from ctypes import *
import struct
import numpy as np
import time
import cv2


##
#   当前版本基于协议V0.3.1定义
##

##
#   定义接收数据的结构体
##
## 定义VP目标帧头结构体
class frame_header_infos_struct(Structure):
    _pack_ = 1
    _fields_ = [
        ('header',      c_uint32),
        ('data_len',    c_uint32),
        ('data_type',   c_int8),
        ('protocol_ver',c_uint32),
        ('dev_sn',      c_uint32),
        ('sensor_sn',   c_uint32),
        ('dev_lon',     c_double),
        ('dev_lat',     c_double),
        ('dev_alt',     c_float),
        ('dev_azimuth', c_float),
        ('enu_lon',     c_double),
        ('enu_lat',     c_double),
        ('enu_alt',     c_float),
        ('pixel2enu',   c_double * 9),
        ('enu2pixel',   c_double * 9),
        ('frame_count', c_uint32),
        ('timestamp',   c_double),
        ('fs',          c_uint16),
        ('img_width',   c_uint16),
        ('img_height',  c_uint16),
        ('img_format',  c_uint16),
        ('img_size',    c_uint32),
        ('img_resize_width', c_uint16),
        ('img_resize_height', c_uint16)
    ]

class frame_header_infos(Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   frame_header_infos_struct),
        ('total',   c_uint8 * 1024)
    ]


# 定义统计数据帧头结构体
class frame_header_infos_vp_statistics_struct(Structure):
    _pack_ = 1
    _fields_ = [
        ('header',      c_uint32),
        ('data_len',    c_uint32),
        ('data_type',   c_int8),
        ('protocol_ver',c_uint32),
        ('dev_sn',      c_uint32),
        ('sensor_sn',   c_uint32),
        ('dev_lon',     c_double),
        ('dev_lat',     c_double),
        ('dev_alt',     c_float),
        ('dev_azimuth', c_float),
        ('enu_lon',     c_double),
        ('enu_lat',     c_double),
        ('enu_alt',     c_float),
        ('pixel2enu',   c_double * 9),
        ('enu2pixel',   c_double * 9),
        ('frame_count', c_uint32),
        ('timestamp',   c_double),
        ('fs',          c_uint16),
        ('count',       c_uint16),
        ('msg_type',    c_uint8),
        ('img_origin_width', c_uint16),
        ('img_origin_height', c_uint16),
        ('img_resize_width', c_uint16),
        ('img_resize_height', c_uint16)
    ]


class frame_header_infos_vp_statistics(Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   frame_header_infos_vp_statistics_struct),
        ('total',   c_uint8 * 1024)
    ]

    
## 单个目标的数据结构
class obj_struct(Structure) : 
    _pack_ = 1
    _fields_ = [    
        ('num',         c_uint16),      # 计数编号，从0开始
        ('track_id',    c_uint32),      # 航迹编号
        ('x',           c_int16),       # 目标位置x，float，单位：m
        ('y',           c_int16),       # 目标位置y，float，单位：m
        ('z',           c_int16),       # 目标位置z，float，单位：m
        ('vx',          c_uint16),      # 目标速度Vx，float，单位：m/s
        ('vy',          c_uint16),      # 目标速度Vy，float，单位：m/s
        ('vz',          c_uint16),      # 目标速度Vz，float，单位：m/s
        ('length',      c_uint16),      # 目标长度，float， 单位：m
        ('width',       c_uint16),      # 目标宽度，float， 单位：m
        ('height',      c_uint16),      # 目标高度，float， 单位：m
        ('azimuth',     c_uint16),      # 目标航向角，目标当前位置与正北方向的夹角，float，单位：度
        ('img_x',       c_uint16),      # 目标像素坐标x, uint16，单位：pixel, modified by zzk, 2022.02.10
        ('img_y',       c_uint16),      # 目标像素坐标y, uint16，单位：pixel, modified by zzk, 2022.02.10
        ('img_len',     c_uint16),      # 目标像素长度，uint16， 单位：pixel, modified by zzk, 2022.02.10
        ('img_wid',     c_uint16),      # 目标像素宽度，uint16， 单位：pixel, modified by zzk, 2022.02.10
        ('img_hig',     c_uint16),      # 目标像素高度，uint16， 单位：pixel, modified by zzk, 2022.02.10
        ('img_len_ang', c_uint16),      # 目标像素长度方向，float， 单位：度，精确到0.01, modified by zzk, 2022.02.10
        ('img_wid_ang', c_uint16),      # 目标像素宽度方向，float， 单位：度，精确到0.01, modified by zzk, 2022.02.10
        ('img_hig_ang', c_uint16),      # 目标像素高度方向，float， 单位：度，精确到0.01, modified by zzk, 2022.02.10
        ('type',        c_uint8),       # 目标类型
        ('confidence',  c_uint8),       # 目标置信度，int，单位：%
        ('lic',         c_char * 12),   # 车辆车牌号，字符串类型，长度12字节
        ('lane_id',     c_uint8)        # 车辆所在车道编号
    ]
class obj_union (Union) :
    _pack_ = 1
    _fields_ = [
        ('total', c_char * 64),         # 保留64位
        ('infos', obj_struct)           # 目标结构体
    ]
    
    def __init__ (self) :
        self.targets_list = b''
        self.num = 0
    
    def add (self, track_id, x, y, z, vx, vy, vz, length, width, height, azimuth, img_x, img_y, img_len, img_wid, img_hig, img_len_ang, img_wid_ang, img_hig_ang, type, confidence, lic, lane_id=1):
        obj = obj_union()
        obj.infos.num            = self.num
        obj.infos.track_id       = track_id   
        obj.infos.x              = x          
        obj.infos.y              = y          
        obj.infos.z              = z          
        obj.infos.vx             = vx         
        obj.infos.vy             = vy         
        obj.infos.vz             = vz         
        obj.infos.length         = length     
        obj.infos.width          = width      
        obj.infos.height         = height     
        obj.infos.azimuth        = azimuth    
        obj.infos.img_x          = img_x      
        obj.infos.img_y          = img_y      
        obj.infos.img_len        = img_len    
        obj.infos.img_wid        = img_wid    
        obj.infos.img_hig        = img_hig    
        obj.infos.img_len_ang    = img_len_ang
        obj.infos.img_wid_ang    = img_wid_ang
        obj.infos.img_hig_ang    = img_hig_ang
        obj.infos.type           = type       
        obj.infos.confidence     = confidence 
        if len(lic.encode('utf-8')) > 12 :
            print ("car plane error: ", lic, "len: ", len(lic.encode('utf-8')))
            lic                  = 'AAAAAAAAA'
        obj.infos.lic            = lic.encode('utf-8') 
        obj.infos.lane_id        = lane_id

        self.targets_list += bytes(obj)
        self.num += 1
    
    

## 目标统计信息结构体
## 断面统计信息
## 断面统计帧头
class statistics_fracture_header_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('period',  c_uint16),
        ('len_a',   c_uint8),
        ('len_b',   c_uint8),
        ('len_c',   c_uint8),
        ('lane_num',c_uint8)
    ]
class statistics_fracture_header(Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   statistics_fracture_header_struct),
        ('total',   c_uint8*16)
    ]
    
    def __init__ (self, period, len_a, len_b, len_c, lane_num) :
        self.infos.period   = period
        self.infos.len_a    = len_a   
        self.infos.len_b    = len_b
        self.infos.len_c    = len_c
        self.infos.lane_num = lane_num
    
    def bytes(self):
        return bytes(self.total)
    
## 断面统计信息单个车道结构
class statistics_fracture_lane_infos_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('lane_id',             c_uint16),
        ('car_num',             c_uint16),
        ('car_a_count',         c_uint16), 
        ('car_b_count',         c_uint16),
        ('car_c_count',         c_uint16),
        ('occupacy',            c_uint16),
        ('avg_speed',           c_uint16),
        ('avg_car_len',         c_uint8),
        ('avg_car_head_time',   c_uint8),
        ('avg_car_body_time',   c_uint8)
    ]
class statistics_fracture_lane_infos (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   statistics_fracture_lane_infos_struct),
        ('total',   c_uint8*24)
    ]
    
    def __init__ (self) :
        self.targets_list = b''
    
    def add (self, lane_id, car_num, car_a_count, car_b_count, car_c_count, occupacy, avg_speed, avg_car_len, avg_car_head_time, avg_car_body_time) :
        obj = statistics_fracture_lane_infos()
        obj.infos.lane_id               = lane_id
        obj.infos.car_num               = car_num
        obj.infos.car_a_count           = car_a_count
        obj.infos.car_b_count           = car_b_count
        obj.infos.car_c_count           = car_c_count
        obj.infos.occupacy              = occupacy
        obj.infos.avg_speed             = avg_speed
        obj.infos.avg_car_len           = avg_car_len
        obj.infos.avg_car_head_time     = avg_car_head_time
        obj.infos.avg_car_body_time     = avg_car_body_time
        
        # print ("fracture", 
        #     obj.infos.lane_id,
        #     obj.infos.car_num,
        #     obj.infos.car_a_count,
        #     obj.infos.car_b_count,
        #     obj.infos.car_c_count,
        #     obj.infos.occupacy,
        #     obj.infos.avg_speed,
        #     obj.infos.avg_car_len,
        #     obj.infos.avg_car_head_time,
        #     obj.infos.avg_car_body_time
        # )
        # print ("fracture", bytes(obj))            
        self.targets_list += bytes(obj)
        
    def bytes(self):
        return bytes(self.total)
    

## 触发统计帧头信息
class statistics_trigger_header_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('trigger_num', c_uint8),
    ]
class statistics_trigger_header (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   statistics_trigger_header_struct),
        ('total',   c_uint8 * 8)
    ]
    
    def __init__ (self, trigger_num):
        self.infos.trigger_num = trigger_num
        
    def bytes(self):
        return bytes(self.total)

## 触发统计单个车道信息
class statistics_trigger_lane_infos_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('obj_id',                  c_uint16),
        ('lane_id',                 c_uint16),
        ('trigger_lane_position',   c_uint16),
        ('speed',                   c_uint16),
        ('trigger_status',          c_uint8)
    ]
class statistics_trigger_lane_infos (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   statistics_trigger_lane_infos_struct),
        ('total',   c_uint8*16)
    ]
    
    def __init__(self) :
        self.targets_list = b''
    
    def add (self, obj_id, lane_id, trigger_lane_position, speed, trigger_status) :
        obj = statistics_trigger_lane_infos()
        obj.infos.obj_id                = obj_id
        obj.infos.lane_id               = lane_id
        obj.infos.trigger_lane_position = trigger_lane_position
        obj.infos.speed                 = speed
        obj.infos.trigger_status        = trigger_status
        # print ("trigger", 
        #     obj.infos.obj_id               ,
        #     obj.infos.lane_id              ,
        #     obj.infos.trigger_lane_position,
        #     obj.infos.speed                ,
        #     obj.infos.trigger_status       
        # )
        self.targets_list += bytes(obj)


## 区域统计帧头结构体
class statistics_area_header_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('period',  c_uint16),
        ('near_pos',c_uint16),
        ('far_pos', c_uint16),
        ('lane_num',c_uint8)
    ]
class statistics_area_header (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos', statistics_area_header_struct),
        ('total', c_uint8 * 16)
    ]
    
    def __init__(self, period, near_pos, far_pos, lane_num) :
        self.infos.period    = period
        self.infos.near_pos  = near_pos
        self.infos.far_pos   = far_pos
        self.infos.lane_num  = lane_num
        
    def bytes(self):
        return bytes(self.total)

## 区域统计单个车道信息结构体
class statistics_area_lane_infos_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('lane_id',         c_uint16),
        ('car_num',         c_uint16),
        ('occupacy',        c_uint16),
        ('avg_speed',       c_uint16),
        ('distribute',      c_uint16),
        ('head_car_pos',    c_uint16),
        ('head_car_speed',  c_uint16),
        ('tail_car_pos',    c_uint16),
        ('tail_car_speed',  c_uint16)
    ]
    
class statistics_area_lane_infos (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos', statistics_area_lane_infos_struct),
        ('total', c_uint8 * 24)
    ]
    def __init__(self) :
        self.targets_list = b''
    
    def add (self, lane_id, car_num, occupacy, avg_speed, distribute, head_car_pos, head_car_speed, tail_car_pos, tail_car_speed) :
        obj = statistics_area_lane_infos()
        obj.infos.lane_id           = lane_id       
        obj.infos.car_num           = car_num       
        obj.infos.occupacy          = occupacy      
        obj.infos.avg_speed         = avg_speed     
        obj.infos.distribute        = distribute    
        obj.infos.head_car_pos      = head_car_pos  
        obj.infos.head_car_speed    = head_car_speed
        obj.infos.tail_car_pos      = tail_car_pos  
        obj.infos.tail_car_speed    = tail_car_speed
        
        # print ("area", 
        #     obj.infos.lane_id       ,
        #     obj.infos.car_num       ,
        #     obj.infos.occupacy      ,
        #     obj.infos.avg_speed     ,
        #     obj.infos.distribute    ,
        #     obj.infos.head_car_pos  ,
        #     obj.infos.head_car_speed,
        #     obj.infos.tail_car_pos  ,
        #     obj.infos.tail_car_speed
        # )
        
        self.targets_list += bytes(obj)


## 排队统计信息帧头信息结构体
class statistics_queue_header_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('period',              c_uint16),
        ('dis_threshhold',      c_uint8),
        ('speed_threshhold',    c_uint8),
        ('lane_num',            c_uint8)
    ]

class statistics_queue_header (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos', statistics_queue_header_struct),
        ('total', c_uint8 * 12)
    ]
    
    def __init__ (self, period, dis_threshhold, speed_threshhold, lane_num) :
        self.infos.period            = period
        self.infos.dis_threshhold    = dis_threshhold
        self.infos.speed_threshhold  = speed_threshhold
        self.infos.lane_num          = lane_num
        
    def bytes(self):
        return bytes(self.total)   
    
    

## 排队统计数据单个车道信息
class statistics_queue_lane_infos_struct (Structure) :
    _pack_ = 1
    _fields_ = [
        ('lane_id',         c_uint16),
        ('queue_length',    c_uint16),
        ('head_car_pos',    c_uint16),
        ('tail_car_pos',    c_uint16),
        ('queue_num',       c_uint16)
    ]
    

class statistics_queue_lane_infos (Union) :
    _pack_ = 1
    _fields_ = [
        ('infos',   statistics_queue_lane_infos_struct),
        ('total',   c_uint8 * 16)
    ]
    
    def __init__ (self) :
        self.targets_list = b''
        
    def add(self, lane_id, queue_length, head_car_pos, tail_car_pos, queue_num) :
        obj = statistics_queue_lane_infos()
        obj.infos.lane_id       = lane_id
        obj.infos.queue_length  = queue_length
        obj.infos.head_car_pos  = head_car_pos
        obj.infos.tail_car_pos  = tail_car_pos
        obj.infos.queue_num     = queue_num
        
        # print ("queue", 
        #     obj.infos.lane_id     ,
        #     obj.infos.queue_length,
        #     obj.infos.head_car_pos,
        #     obj.infos.tail_car_pos,
        #     obj.infos.queue_num   
        # )
        
        self.targets_list += bytes(obj)

        
 
      
# ## 发送vp发送目标信息
# class target_infos_per:
    
#     def __init__(self):
#         self.targets_list = []

#     # msg 发送的数据结构
#     ## modified by zzk, 2022.02.10, 增加“img_x, img_y, img_len, img_wid, img_hig, img_len_ang, img_wid_ang, img_hig_ang”
#     ## modified by zzk, 2022.05.09, 增加对空车牌的判定，必须占住对应位置，设置默认的lic号为“AAAAAAAAA”
#     def add(self, track_id, x, y, z, vx, vy, vz, length, width, height, azimuth, img_x, img_y, img_len, img_wid, img_hig, img_len_ang, img_wid_ang, img_hig_ang, type, confidence, lic):
#         obj = obj_union()
#         obj.infos.track_id       = track_id   
#         obj.infos.x              = x          
#         obj.infos.y              = y          
#         obj.infos.z              = z          
#         obj.infos.vx             = vx         
#         obj.infos.vy             = vy         
#         obj.infos.vz             = vz         
#         obj.infos.length         = length     
#         obj.infos.width          = width      
#         obj.infos.height         = height     
#         obj.infos.azimuth        = azimuth    
#         obj.infos.img_x          = img_x      
#         obj.infos.img_y          = img_y      
#         obj.infos.img_len        = img_len    
#         obj.infos.img_wid        = img_wid    
#         obj.infos.img_hig        = img_hig    
#         obj.infos.img_len_ang    = img_len_ang
#         obj.infos.img_wid_ang    = img_wid_ang
#         obj.infos.img_hig_ang    = img_hig_ang
#         obj.infos.type           = type       
#         obj.infos.confidence     = confidence 
#         obj.infos.lic            = lic.encode() 

#         self.targets_list.append(obj)
#         return self.targets_list 


class vp_common_pyapi:
    
    default_lib_path = "./liblinux_ipc_for_python_share.so"
    default_socket_path = "/tmp/lowcost_vc2vp.socket"
    default_msg_id = 1234
    dev_sn = 12345678
    sensor_sn = 23456789
    ver_main = 0x00
    ver_sub = 0x00
    ver_fixed = 0x01
    ## V0.1.alpha_7_V0.1.3 版本说明：2022.05.09，增加对车牌的支持，处理空车牌字符串
    ## V0.1.release_4_V0.01.00版本说明： 2022.02.11, 增加sensor_sn
    ## V0.1.release_3_V0.01.01版本说明： 2022.02.10， 增加目标数据内容，增加三维像素信息,修改struct.pack Bug，打包时需要使用“<”单字节对齐
    ## V0.3.realease_1_V0.0.1版本说明：2022.07.26， 增加输出统计信息，支持内部协议版本V0.3.1

    pyapi_video_process_ver = "V0.3.release_1_V%d.%d.%d" %(ver_main, ver_sub, ver_fixed)

    img_width = 2448
    img_height = 2048
    img_rgb_data = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    img_header_infos = frame_header_infos()

    # 定义输入的目标信息的二进制排布顺序
    ## 2022.02.10 modified by zzk， 增加“目标像素位置x， 目标像素位置y， 目标三维长度， 目标三维宽度， 目标三维高度， 目标三维长度方向， 目标三维宽度方向，目标三维高度方向”， 修改"HI10H2B" --> "<HI18H2B"
    # [计数，跟踪的航迹ID，目标位置x， 目标位置y, 目标位置z, 目标速度Vx， 目标速度Vy， 目标速度Vz， 目标长度， 目标宽度， 目标高度， 目标航向角， 目标像素位置x， 目标像素位置y， 目标三维长度， 目标三维宽度， 目标三维高度， 目标三维长度方向， 目标三维宽度方向，目标三维高度方向， 目标类型，目标置信度]
    # 2022.05.07 modified by zzk, 增加车牌号信息，修改"<HI18H2B" --> "<HI18H2Bp"
    # 2022.05.09 modified by zzk, 更新车牌增加方式，修改"<HI18H2Bp" --> "<HI18H2B"
    struct_targets_infs_bin_infos = "<HI18H2B"

    # 初始化函数
    def __init__(self, lib_path = default_lib_path):
        # TODO： 需要读取配置文件中的参数，从而获取相关配置
        self.library = cdll.LoadLibrary(lib_path)
        
    ## socket初始化函数，阻塞式等待连接，只有连接上才会退出    
    def socket_init(self):
        self.library.socket_rcv_listen.argtypes = [c_char_p,]
        self.library.socket_rcv_listen.restype = c_int32

        socket_path_str = create_string_buffer(self.default_socket_path.encode('utf-8'))
        self.socket_fd = self.library.socket_rcv_listen(socket_path_str)
    
    
    ## sokcet 断开连接函数
    def socket_close(self):
        self.library.linux_ipc_socket_disconnected.argtypes = [c_int32,]
        self.library.linux_ipc_socket_disconnected.restype = c_int32
        
        self.library.linux_ipc_socket_disconnected(c_int32(self.socket_fd))
    
    ## msg初始化函数
    def msg_init(self,input_msg_id = default_msg_id):
        self.library.linux_ipc_msg_connect.argtypes = [c_uint32,]
        self.library.linux_ipc_msg_connect.restype = c_int32

        self.msg_fd = self.library.linux_ipc_msg_connect((c_uint32(self.default_msg_id)))

    ## 接收图像数据
    # img_data 为numpy数组，大小为图像的 长*宽*3*sizeof(char)
    # 返回值：
    #       flag: >= 0, 成功，<0: 失败
    #       img_header_infos: 帧头信息，参见class frame_header_infos
    def get_img_data(self):
        # self.library.vp_img_data_recv.argtypes = [
        #     c_uint32, 
        #     np.ctypeslib.ndpointer(dtype=np.uint8, flags="C_CONTIGUOUS"), 
        #     c_void_p]
        # self.library.vp_img_data_recv.restype = c_int32
        # recv img header
        self.library.vp_img_data_recv_header.argtypes = [
            c_uint32, 
            c_void_p]
        self.library.vp_img_data_recv_header.restype = c_int32

        self.library.vp_img_data_recv_img.argtypes = [
            c_uint32, 
            np.ctypeslib.ndpointer(dtype=np.uint8, flags="C_CONTIGUOUS"), 
            c_void_p]
        self.library.vp_img_data_recv_img.restype = c_int32
        # 先获取图像数据大小，再申请数据空间，再接收数据
        while True: 
            flag = self.library.vp_img_data_recv_header(c_uint32(self.socket_fd), addressof(self.img_header_infos));
            if (flag < 0) :
                print ("failed to get video header")
                # self.socket_init()
                break;
            # 判定是否与现有空间一致，如果不一致，则重新申请空间
            if (self.img_header_infos.infos.img_width != self.img_width) or (self.img_header_infos.infos.img_height != self.img_height) :
                self.img_width = self.img_header_infos.infos.img_width
                self.img_height = self.img_header_infos.infos.img_height
                self.img_rgb_data = np.zeros ((self.img_height, self.img_width, 3), dtype=np.uint8)
                print ("now image size is: ", self.img_width, self.img_height)

            # 获取图像
            flag = self.library.vp_img_data_recv_img(c_uint32(self.socket_fd), self.img_rgb_data, addressof(self.img_header_infos))
            if (flag < 0) :
                print ("failed to get video img")
                # self.socket_init()
                break;
            else :
                break
        return (flag,self.img_header_infos)
        
    
    ## 发送图像处理结果
    # 输入参数：
    #       targets_infos， 单个数据信息，targets_list的值
    #       frame_header， 帧头信息，get_img_data返回的第二个参数值
    #       statistics_header， 统计数据帧头，当输出目标数据时无效
    #       msg_type， 说明数据类型，分别为
    #               “objs”                  : 目标数据，
    #               “statistics_fracture”   : 断面统计
    #               “statistics_trigger”    : 触发统计
    #               “statistics_area”       : 区域统计
    #               “statistics_queue”      : 排队统计
    #               “statistics_event”      : 事件信息
    # 返回值：
    #   0  : 成功
    #   <0 : 失败
    def send_vp_rst(self, targets_infos, frame_header, statistics_header="null", msg_type="objs"): 
        self.library.vp_img_process_send.argtypes = [c_int32, c_void_p, c_void_p, c_uint32]
        self.library.vp_img_process_send.restype = c_int32

        header_infos = frame_header_infos_vp_statistics()
        header_infos.infos.header               = 0x5A5A5A5A
        header_infos.infos.data_type            = 2
        header_infos.infos.protocol_ver         = frame_header.infos.protocol_ver
        header_infos.infos.dev_sn               = frame_header.infos.dev_sn
        header_infos.infos.sensor_sn            = frame_header.infos.sensor_sn
        header_infos.infos.dev_lon              = frame_header.infos.dev_lon
        header_infos.infos.dev_lat              = frame_header.infos.dev_lat
        header_infos.infos.dev_alt              = frame_header.infos.dev_alt
        header_infos.infos.dev_azimuth          = frame_header.infos.dev_azimuth
        header_infos.infos.enu_lon              = frame_header.infos.enu_lon
        header_infos.infos.enu_lat              = frame_header.infos.enu_lat
        header_infos.infos.enu_alt              = frame_header.infos.enu_alt
        header_infos.infos.pixel2enu            = frame_header.infos.pixel2enu
        header_infos.infos.enu2pixel            = frame_header.infos.enu2pixel
        header_infos.infos.frame_count          = frame_header.infos.frame_count
        header_infos.infos.timestamp            = frame_header.infos.timestamp
        header_infos.infos.fs                   = frame_header.infos.fs
        header_infos.infos.img_origin_width     = frame_header.infos.img_width
        header_infos.infos.img_origin_height    = frame_header.infos.img_height
        header_infos.infos.img_resize_width     = frame_header.infos.img_resize_width
        header_infos.infos.img_resize_height    = frame_header.infos.img_resize_height

        # print (frame_header.pixel2enu)
           
        
        # 需要将输入的数据打包成struct的结构，需要定义输入的数据的结构
        target_infos_struct = b''
        target_count = 0
        if msg_type != "objs":
            statistics_header = bytes(statistics_header)
        
        if msg_type == "objs":
            # VP中的检测跟踪结果
            # for target in targets_infos:
                # target.infos.num = target_count
                # target_infos_struct += bytes(target)
                # target_count += 1
            target_count = int(len(targets_infos) / sizeof(obj_union))
            target_infos_struct += targets_infos
            # if target_count == 0:
            #     print ("input targets is zero")
            #     return -1
            header_infos.infos.msg_type = 0x65
            
            
        elif msg_type == "statistics_fracture" :
            # VP中的断面统计结果    
            ## 增加断面统计数据中的帧头部分
            target_infos_struct += statistics_header
            ## 增加断面统计数据中的每个车道的信息
            target_infos_struct += targets_infos
            
            # 将数据发送出去
            header_infos.infos.msg_type = 0x80
            
        elif msg_type == "statistics_trigger" :
            # VP中的触发统计结果
            ## 增加触发统计数据中的帧头部分
            target_infos_struct += statistics_header
            ## 增加触发统计数据中的每个车道的信息
            target_infos_struct += targets_infos
            
            header_infos.infos.msg_type = 0x81
            
        elif msg_type == "statistics_area" :
            # VP中的区域统计结果
            ## 增加区域统计数据中的帧头部分
            target_infos_struct += statistics_header
            ## 增加区域统计数据中的每个车道的信息
            target_infos_struct += targets_infos
            header_infos.infos.msg_type = 0x82
            
        elif msg_type == "statistics_queue" :
            # VP中的排队统计结果
            ## 增加排队统计数据中的帧头部分
            target_infos_struct += statistics_header
            ## 增加排队统计数据中的每个车道的信息
            target_infos_struct += targets_infos
            header_infos.infos.msg_type = 0x83
            
        elif msg_type == "statistics_event" :
            # VP中的事件信息
            ## 增加事件数据中的帧头部分
            target_infos_struct += statistics_header
            ## 增加事件数据中的每个车道的信息
            target_infos_struct += targets_infos
            header_infos.infos.msg_type = 0x84
        
        # print (header_infos.infos)
        ## 发送目标数据
        ret = self.library.vp_img_process_send(self.msg_fd, addressof(header_infos), target_infos_struct, target_count)
        return ret

