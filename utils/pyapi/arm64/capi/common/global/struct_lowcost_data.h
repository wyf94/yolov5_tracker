/*
 * struct_lowcost_data.h
 *
 *  Created on: Dec 27, 2021
 *      Author: noven_zhang
 *      Brief : 定义低成本一体机软件中使用到的数据结构定义
 *      Vers  : V0.1.alpha_6
 */

#ifndef STRUCT_LOWCOST_DATA_H_
#define STRUCT_LOWCOST_DATA_H_

#include <stdint.h>

#pragma pack(1)

/**
 * @brief: 定义版本信息
 */
#define PROTOCOL_VERSION	(0X00010400)


/** 定义帧头保留长度 **/
#define FRAME_SIZE	1024

/** 定义雷达目标包头长度 **/
#define STRUCT_RADAR_PARAM_OBJECT_HEAD_LENGTH					(26)
/** 定义雷达目标信息长度 **/
#define STRUCT_RADAR_PARAM_OBJECT_INFOS_LENGTH					(48)

/** 定义断面统计信息包头长度 **/
#define STRUCT_RADAR_STASTIC_FRACTURE_HEAD_LENGTH				(16)
/** 定义断面统计信息数据包长度 **/
#define STRUCT_RADAR_STASTIC_FRACTURE_INFOS_LENGTH				(24)
/** 定义触发统计信息包头长度 **/
#define STRUCT_RADAR_STASTIC_TRIGGER_HEAD_LENGTH				(8)
/** 定义触发统计信息数据包长度 **/
#define STRUCT_RADAR_STASTIC_TRIGGER_INFOS_LENGTH				(16)
/** 定义区域统计信息包头长度 **/
#define STRUCT_RADAR_STASTIC_AREA_HEAD_LENGTH					(16)
/** 定义区域统计信息数据包长度 **/
#define STRUCT_RADAR_STASTIC_AREA_INFOS_LENGTH					(24)
/** 定义排队统计信息包头长度 **/
#define STRUCT_RADAR_STASTIC_QUEUE_HEAD_LENGTH					(12)
/** 定义排队统计信息数据包长度 **/
#define STRUCT_RADAR_STASTIC_QUEUE_INFOS_LENGTH					(16)

/**
 * \enum enmu_data_type
 * @brief 数据类型
 */
typedef enum enmu_data_type
{
	UNKNOW				= 0X00,	///< 未知
	LC_VIDEO_CAPTURE 	= 0X01,	///< 视频原始数据
	LC_VIDEO_PROCESS 	= 0X02,	///< 视频处理结果
	LC_RADAR_CAPTURE 	= 0X10,	///< 雷达捕获的目标数据
	LC_FUSION_PROCESS 	= 0X20,	///< 融合结果数据
}ENUM_DATA_TYPE;

/**
 * \enmu enum_target_types
 * @brief 检测到的目标类型
 */
typedef enum enum_target_types
{
	LC_TARGET_TYPE_UNKNOWN 			= 0x00,	///< 无效
	LC_TARGET_TYPE_PERSON			= 0X01,	///< 人
	LC_TARGET_TYPE_BICYCLE			= 0X02,	///< 自行车
	LC_TARGET_TYPE_CAR				= 0X03,	///< 小车
	LC_TARGET_TYPE_MOTORBIKE		= 0X04,	///< 摩托车
	LC_TARGET_TYPE_BUS				= 0X06,	///< 公交车
	LC_TARGET_TYPE_TRUCK			= 0X08,	///< 卡车
	LC_TARGET_TYPE_TRAFFIC_LIGHT	= 0X0A,	///< 交通灯
}ENUM_TARGET_TYPE;

/****** V0.1.release_5 新增设备信息 ******/
/**
 * \enum _IMG_FORMAT_ENUM_
 * @brief 说明图片的具体格式
 */
typedef enum _IMG_FORMAT_ENUM_
{
	UNKNOWN				= 0,		///< 无效
	IMG_FORMAT_MPEG		= 0x03,		///< mjpeg
	IMG_FORMAT_JPEG		= 0x04,		///< jpeg
	IMG_FORMAT_YUYV422	= 0x06,		///< YUYV:4:2:2
	IMG_FORMAT_BAYER_RG	= 0x07,		///< Bayer_RG
	IMG_FORMAT_BAYER_GR	= 0x08,		///< Bayer_GR
	IMG_FORMAT_BAYER_BG	= 0x09,		///< Bayer_BG
	IMG_FORMAT_BAYER_GB	= 0x0A,		///< Bayer_GB
}ENUM_IMG_FORMAT;
/****** end of V0.1.release_5 新增设备信息 ******/

/****** V0.1.release_6 雷达数据增加多个类型 ******/
typedef enum _rc_msg_data_type_ {
	RC_MSG_TYPE_UNKNOWN			= 0,		///< 无效
	RC_MSG_TYPE_OBJS			= 0X65,		///< 目标数据
	RC_MSG_TYPE_FRACTURE		= 0X80,		///< 断面统计信息
	RC_MSG_TYPE_TRIGGER			= 0X81,		///< 触发统计信息
	RC_MSG_TYPE_AREA			= 0X82,		///< 区域统计信息
	RC_MSG_TYPE_QUEUE			= 0X83,		///< 排队统计信息
	RC_MSG_TYPE_EVENT			= 0X84		///< 事件统计信息
}RC_MSG_DATA_TYPE_ENUM;
/****** end of V0.1.release_5 雷达数据增加多个类型 ******/

/**
 * \struct struct_video_capture_data
 * @brief LC_VIDEO_CAPTURE对应的数据结构
 */

typedef struct struct_video_capture_data
{
	union{
		unsigned char reserved_total[FRAME_SIZE];
		struct {
			unsigned int	header;			///< 帧头
			unsigned int 	data_len;		///< 数据长度
			unsigned char	data_type;		///< 数据类型，参考ENUM_DATA_TYPE
			unsigned int	protocol_ver;	///< 协议版本
			unsigned int	dev_sn;			///< 设备编号
			/****** V0.1.release_4 新增设备信息 ******/
			unsigned int	sensor_sn;		///< 传感器编号
			/****** end of V0.1.release_4 新增设备信息 ******/
			/****** V0.1.release_3 新增设备信息 ******/
			double			dev_lon;		///< 设备安装经度
			double			dev_lat;		///< 设备安装纬度
			float			dev_alt;		///< 设备安装海拔
			float			dev_azimuth;	///< 设备安装偏北角，与正北方向的夹角，范围：[-360,360]
			double			enu_lon;		///< 东北天原点的经度
			double			enu_lat;		///< 东北天原点的纬度
			float			enu_alt;		///< 东北天原点的海拔
			double			pixel2enu[9];	///< 像素坐标转东北天的转换矩阵
			double			enu2pixel[9];	///< 东北天转像素坐标的转换矩阵
			/****** end of V0.1.release_3 新增设备信息 ******/
			unsigned int	frame_count;	///< 帧计数
			double			timestamp;		///< 时间戳
			unsigned short	fs;				///< 帧率
			unsigned short	img_width;		///< 图像宽度
			unsigned short 	img_height;		///< 图像高度
			/****** V0.1.release_5 新增设备信息 ******/
			unsigned short 	img_format;		///< 图片格式，参见ENUM_IMG_FORMAT
			/****** end of V0.1.release_5 新增设备信息 ******/
			unsigned int	img_size;		///< 图像数据大小
		}struct_infos;
	}union_frame_head_infos;
	void*			img_data_addr;	///< 图像数据存放地址
	unsigned int	crc_sum;		///< 校验位
	unsigned int	tail;			///< 帧尾
}VC_STRUCT;


/**
 * \struct struct_radar_capture_data_per
 * @brief 单个雷达目标点的信息
 */

typedef union struct_radar_capture_data_per
{
	char total[STRUCT_RADAR_PARAM_OBJECT_INFOS_LENGTH];
	struct {
	unsigned short	count;			///< 计数
	unsigned int	track_id;		///< 跟踪的航迹编号
	unsigned short	x;				///< 雷达目标位置x
	unsigned short	y;				///< 雷达目标位置y
	unsigned short	z;				///< 雷达目标位置z
	unsigned short	vx;				///< 雷达目标x方向速度vx
	unsigned short 	vy;				///< 雷达目标y方向速度vy
	unsigned short	vz;				///< 雷达目标z方向速度vz
	unsigned short	length;			///< 目标长度
	unsigned short	width;			///< 目标宽度
	unsigned short	height;			///< 目标高度
	unsigned short	azimuth;		///< 目标航向角
	unsigned char	confidence;		///< 目标置信度
	}infos;
}RADAR_PER_OBJS_INFO;

/**
 * @brief : 0x65 雷达目标信息格式
 */
typedef struct _struct_radar_capture_objs_data_ {
	union {
		char total[STRUCT_RADAR_PARAM_OBJECT_HEAD_LENGTH];
		struct {
			uint16_t	objs_num;			///< 目标个数
			uint8_t		lane_num;			///< 车道数
			int32_t		lon;				///< 雷达经度
			int32_t		lat;				///< 雷达纬度
			int16_t		alt;				///< 雷达海拔高度
			uint16_t	azimuth;			///< 雷达安装偏北角
			uint32_t	frame_id;			///< 帧号
			int16_t		angle;				///< 安装偏转角，雷达安装角度与车道方向的角度
			uint8_t 	radar_ip_3rd;		///< 雷达IP第3段
			uint8_t		radar_ip_4th;		///< 雷达IP第4段
		}infos;
	}head;
	RADAR_PER_OBJS_INFO objs[];			///< 雷达目标信息
}RADAR_CAPTURE_OBJS_INFOS;


/**
 * @brief : 0x80断面统计信息，单车道统计信息
 */

typedef union _struct_radar_fracture_per_lane_infos_ {
	unsigned char 	total[STRUCT_RADAR_STASTIC_FRACTURE_INFOS_LENGTH];
	struct {
		unsigned short	lane_id;				///< 检测通道编号
		unsigned short	car_num;				///< 车辆总数
		unsigned short	car_a_count;			///< A类车流量
		unsigned short	car_b_count;			///< B类车流量
		unsigned short	car_c_count;			///< C类车流量
		unsigned short	occupacy;				///< 占有率，单位：0.1%
		unsigned short	avg_speed;				///< 平均车速，单位：0.1米/秒
		unsigned char	avg_car_len;			///< 平均车长，单位：0.1米
		unsigned char	avg_car_head_time;		///< 平均车头时距，单位：秒
		unsigned char	avg_car_body_time;		///< 平均车身时距，单位：秒
	}infos;
}STRUCT_RADAR_FRACTURE_PER_LANE_INFOS;

/**
 * @brief : 0x80 断面统计信息消息体
 */

typedef struct _struct_radar_fracture_infos_ {
	union {
		unsigned char	total[STRUCT_RADAR_STASTIC_FRACTURE_HEAD_LENGTH];
		struct {
			unsigned short	period;				///< 统计周期，单位： 秒
			unsigned char	len_a;				///< A类车车长，单位：0.1米
			unsigned char	len_b;				///< B类车车长，单位：0.1米
			unsigned char	len_c;				///< C类车车长，单位：0.1米
			unsigned char	lane_num;			///< 检测车道数
		}infos;
	}head;
	STRUCT_RADAR_FRACTURE_PER_LANE_INFOS lane_infos[];	///< 断面统计信息单个车道信息
}STRUCT_RADAR_FRACTURE_INFOS;


/**
 * @brief : 0x81 触发信息数据单个目标信息
 */

typedef union _struct_radar_stastic_trigger_per_obj_infos_ {
	unsigned char	total[STRUCT_RADAR_STASTIC_TRIGGER_INFOS_LENGTH];
	struct {
		unsigned short	obj_id;						///< 目标ID
		unsigned short	lane_id;					///< 检测通道ID
		unsigned short	trigger_line_position;		///< 触发线位置，单位：0.1米
		signed short	speed;						///< 速度，单位：0.1米/秒
		unsigned char	trigger_status;				///< 触发状态
	}infos;
}STRUCT_RADAR_STASTIC_TRIGGER_PER_OBJ_INFOS;

/**
 * @brief : 0x81 触发统计信息消息体
 */

typedef struct _struct_radar_stastic_trigger_infos_ {
	union {
		unsigned char	total[STRUCT_RADAR_STASTIC_TRIGGER_HEAD_LENGTH];
		struct {
			unsigned char	trigger_num;			///< 触发的目标个数
		}infos;
	}head;
	STRUCT_RADAR_STASTIC_TRIGGER_PER_OBJ_INFOS trigger_infos[];
}STRUCT_RADAR_STASTIC_TRIGGER_INFOS;


/**
 * @brief : 0x82 区域统计信息单个车道信息
 */
typedef union _struct_radar_stastic_area_per_lane_infos_ {
	unsigned char	total[STRUCT_RADAR_STASTIC_AREA_INFOS_LENGTH];
	struct {
		unsigned short	lane_id;				///< 车道编号
		unsigned short	car_num;				///< 车辆数量
		unsigned short	occupacy;				///< 占有率，单位：0.1%
		unsigned short	avg_speed;				///< 平均车速，单位：0.1米/秒
		unsigned short	distribute;				///< 分布情况，单位：0.1米
		unsigned short	head_car_pos;			///< 头车位置，单位：0.1米
		signed short	head_car_speed;			///< 头车速度，单位：0.1米/秒
		unsigned short	tail_car_pos;			///< 尾车位置，单位：0.1米
		signed short	tail_car_speed;			///< 尾车速度，单位：0.1米/秒
	}infos;
}STRUCT_RADAR_STASTIC_AREA_PER_LANE_INFOS;

/**
 * @brief : 0x82 区域统计信息
 */

typedef struct _struct_radar_stastic_area_infos {
	union {
		unsigned char	total[STRUCT_RADAR_STASTIC_AREA_HEAD_LENGTH];
		struct {
			unsigned short	period;		///< 区域统计周期，单位：0.1秒
			unsigned short	near_pos;	///< 检测区域近端位置，单位：0.1米
			unsigned short	far_pos;	///< 检测区域远端位置，单位：0.1米
			unsigned char	lane_num;	///< 检测车道数
		}infos;
	}head;
	STRUCT_RADAR_STASTIC_AREA_PER_LANE_INFOS lane_infos[];
}STRUCT_RADAR_STASTIC_AREA_INFOS;


/**
 * @brief : 0x83 排队长度详细信息说明
 */
typedef union _struct_radar_stastic_queue_per_infos_ {
	unsigned char	total[STRUCT_RADAR_STASTIC_QUEUE_INFOS_LENGTH];
	struct {
		unsigned short	lane_id;			///< 检测通道编号
		unsigned short	queue_length;		///< 排队长度，单位：0.1米
		unsigned short	head_car_pos;		///< 头车位置，单位：0.1米
		unsigned short	tail_car_pos;		///< 尾车位置，单位：0.1米
		unsigned short	queue_num;			///< 排队数量，单位：辆
	}infos;
}STRUCT_RADAR_STASTIC_QUEUE_PER_INFOS;


/**
 * @brief : 0x83 排队统计信息消息体
 */

typedef struct _struct_radar_stastic_queue_infos_ {
	union {
		unsigned char	total[STRUCT_RADAR_STASTIC_QUEUE_HEAD_LENGTH];
		struct {
			unsigned short	period;					///< 排队长度统计周期，单位：0.1秒
			unsigned char	dis_threshhold;			///< 距离间隔门限，单位：0.1米
			unsigned char	speed_threshhold;		///< 速度门限，单位：0.1米/秒
			unsigned char	lane_num;				///< 检测的车道数
		}infos;
	}head;
	STRUCT_RADAR_STASTIC_QUEUE_PER_INFOS	lane_infos[];
}STRUCT_RADAR_STASTIC_QUEUE_INFOS;


/**
 * \struct struct_radar_capture_data
 * @brief 获取到的雷达目标的信息
 */

typedef struct struct_radar_capture_data
{
	union{
		unsigned char reserved_total[FRAME_SIZE];
		struct {
			unsigned int				header;			///< 帧头
			unsigned int 				data_len;		///< 数据长度
			unsigned char				data_type;		///< 数据类型，参考ENUM_DATA_TYPE
			unsigned int				protocol_ver;	///< 协议版本
			unsigned int				dev_sn;			///< 设备编号
			/****** V0.1.release_4 新增设备信息 ******/
			unsigned int				sensor_sn;		///< 传感器编号
			/****** end of V0.1.release_4 新增设备信息 ******/
			/****** V0.1.release_3 新增设备信息 ******/
			double						dev_lon;		///< 设备安装经度
			double						dev_lat;		///< 设备安装纬度
			float						dev_alt;		///< 设备安装海拔
			float						dev_azimuth;	///< 设备安装偏北角，与正北方向的夹角，范围：[-360,360]
			double						enu_lon;		///< 东北天原点的经度
			double						enu_lat;		///< 东北天原点的纬度
			float						enu_alt;		///< 东北天原点的海拔
			double						radar2enu[9];	///< 雷达坐标转东北天的转换矩阵
			double						enu2radar[9];	///< 东北天转雷达坐标的转换矩阵
			/****** end of V0.1.release_3 新增设备信息 ******/
			unsigned int				frame_count;	///< 帧计数
			double						timestamp;		///< 时间戳
			unsigned short				fs;				///< 帧率
			/****** V0.1.release_6 增加类型说明 ******/
//			unsigned short				target_count;	///< 目标个数
			unsigned char				msg_type;		///< 数据类型，详见 RC_MSG_DATA_TYPE_ENUM
			/****** end of V0.1.release_6 增加类型说明 ******/
		}struct_infos;
	}union_frame_head_infos;
	/****** V0.1.release_6 增加类型说明 ******/
	union {
		RADAR_CAPTURE_OBJS_INFOS			targets_infos;	///< 0x65 目标信息
		STRUCT_RADAR_FRACTURE_INFOS			fracture_infos;	///< 0x80 断面统计信息
		STRUCT_RADAR_STASTIC_TRIGGER_INFOS	trigger_infos;	///< 0x81 触发统计信息
		STRUCT_RADAR_STASTIC_AREA_INFOS		area_infos;		///< 0x82 区域统计信息
		STRUCT_RADAR_STASTIC_QUEUE_INFOS 	queue_infos;	///< 0x83 排队统计信息
	}msg_data;
	/****** end of V0.1.release_6 增加类型 ******/
	unsigned int				crc_sum;		///< 校验位
	unsigned int				tail;			///< 帧尾
}RADAR_TARGETS_INFOS;


/**
 * \struct struct_video_pertarget_info
 * @brief 图像检测到的单个目标的信息的结构体
 */

typedef struct struct_video_pertarget_info
{
	unsigned short	count;				///< 计数
	unsigned int	track_id;			///< 跟踪的航迹编号
	unsigned short	x;					///< 图像目标位置x
	unsigned short	y;					///< 图像目标位置y
	unsigned short	z;					///< 图像目标位置z
	unsigned short	vx;					///< 图像目标x方向速度vx
	unsigned short 	vy;					///< 图像目标y方向速度vy
	unsigned short	vz;					///< 图像目标z方向速度vz
	unsigned short	length;				///< 目标长度
	unsigned short	width;				///< 目标宽度
	unsigned short	height;				///< 目标高度
	unsigned short	azimuth;			///< 目标航向角
	/****** V0.1.release_3 新增目标三维信息 ******/
	unsigned short	pixel_x;			///< 目标位置，单位：像素
	unsigned short	pixel_y;			///< 目标位置，单位：像素
	unsigned short	pixel_length;		///< 目标三维长度，单位：像素
	unsigned short	pixel_width;		///< 目标三维宽度，单位：像素
	unsigned short	pixel_heigth;		///< 目标三维高度，单位：像素
	short			pixel_length_angle;	///< 目标三维长度方向，单位：0.01度
	short			pixel_width_angle;	///< 目标三维宽度方向，单位：0.01度
	short			pixel_height_angle;	///< 目标三维高度方向，单位：0.01度
	/****** end of V0.1.release_3 新增目标三维信息 ******/
	unsigned char	types;				///< 目标类型，参见ENUM_TARGET_TYPE
	unsigned char	confidence;			///< 目标置信度
	/****** V0.1.release_7 ******/
	char			lic[9];				///< 增加车牌信息
	/****** end of V0.1.release_7 ******/
}VIDEO_PER_TARGET_INFO, *VIDEO_PER_TARGET_INFO_LIST;


/**
 * \struct struct_video_process_data
 * @brief 图像检测到的所有目标的信息
 */

typedef struct struct_video_process_data
{
	union{
		unsigned char reserved_total[FRAME_SIZE];
		struct {
			unsigned int				header;			///< 帧头
			unsigned int 				data_len;		///< 数据长度
			unsigned char				data_type;		///< 数据类型，参考ENUM_DATA_TYPE
			unsigned int				protocol_ver;	///< 协议版本
			unsigned int				dev_sn;			///< 设备编号
			/****** V0.1.release_4 新增设备信息 ******/
			unsigned int	sensor_sn;		///< 传感器编号
			/****** end of V0.1.release_4 新增设备信息 ******/
			/****** V0.1.release_3 新增设备信息 ******/
			double						dev_lon;		///< 设备安装经度
			double						dev_lat;		///< 设备安装纬度
			float						dev_alt;		///< 设备安装海拔
			float						dev_azimuth;	///< 设备安装偏北角，与正北方向的夹角，范围：[-360,360]
			double						enu_lon;		///< 东北天原点的经度
			double						enu_lat;		///< 东北天原点的纬度
			float						enu_alt;		///< 东北天原点的海拔
			double						pixel2enu[9];	///< 像素坐标转东北天的转换矩阵
			double						enu2pixel[9];	///< 东北天转像素坐标的转换矩阵
			/****** end of V0.1.release_3 新增设备信息 ******/
			unsigned int				frame_count;	///< 帧计数
			double						timestamp;		///< 时间戳
			unsigned short				fs;				///< 帧率
			unsigned short				target_count;	///< 目标个数
		}struct_infos;
	}union_frame_head_infos;
	VIDEO_PER_TARGET_INFO		targets_infos[];	///< 所有目标信息,修改，将指针改为动态数组
//	unsigned int				crc_sum;			///< 校验位
//	unsigned int				tail;				///< 帧尾
}VIDEO_TARGETS_INFOS, *PTR_VIDEO_TARGETS_INFOS;

/**
 * @brief 定义融合结果中每个目标的信息
 */
typedef VIDEO_PER_TARGET_INFO FUSION_PER_TARGET_INFO, *FUSION_PER_TARGET_INFO_LIST;


/**
 * @brief 融合数据源设备信息结构体
 */

typedef struct struct_fusion_dev_origin_infos
{
	unsigned char	dev_count;		///< 数据源计数
	unsigned int	dev_sn;			///< 设备编号
	unsigned int	frame_count;	///< 数据帧计数
	double			dev2enu[9];		///< 设备坐标系转东北天坐标系
	double			enu2dev[9];		///< 东北天坐标系转设备坐标系
}FP_DEV_ORIGIN_INFO, *FP_DEV_ORIGIN_INFOS_LIST;

/**
 * \struct struct_fusion_process_data
 * @brief 融合结果输出信息结构体
 */

typedef struct struct_fusion_process_data
{
	union{
		unsigned char reserved_total[FRAME_SIZE];
		struct {
			unsigned int				header;				///< 帧头
			unsigned int 				data_len;			///< 数据长度
			unsigned char				data_type;			///< 数据类型，参考ENUM_DATA_TYPE
			unsigned int				protocol_ver;		///< 协议版本
			unsigned int				dev_sn;				///< 设备编号
			/****** V0.1.release_4 新增设备信息 ******/
			unsigned int	sensor_sn;		///< 传感器编号
			/****** end of V0.1.release_4 新增设备信息 ******/
			/****** V0.1.release_3 新增设备信息 ******/
			double						dev_lon;			///< 设备安装经度
			double						dev_lat;			///< 设备安装纬度
			float						dev_alt;			///< 设备安装海拔
			/****** end of V0.1.release_3 新增设备信息 ******/
			unsigned int				frame_count;		///< 帧计数
			double						timestamp;			///< 时间戳
			unsigned short				fs;					///< 帧率
			unsigned short				target_count;		///< 目标个数
			/****** V0.1.release_3 新增融合数据数据源信息 ******/
			unsigned char				fusion_dev_num;		///< 融合来自的数据源的个数
			FP_DEV_ORIGIN_INFO			fusion_dev_infos[6];///< 融合信息的数据源的设备信息
			/****** end of V0.1.release_3 新增融合数据数据源信息 ******/
		}struct_infos;
	}union_frame_head_infos;
	FUSION_PER_TARGET_INFO_LIST	targets_infos;		///< 所有目标信息
	unsigned int				crc_sum;			///< 校验位
	unsigned int				tail;				///< 帧尾
}FUSION_TARGETS_INFOS, *PTR_FUSION_TARGETS_INFOS;

#pragma pack()
#endif /* STRUCT_LOWCOST_DATA_H_ */
