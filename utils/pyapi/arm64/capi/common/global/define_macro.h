/*
 * define_macro.h
 *
 *  Created on: Dec 29, 2021
 *      Author: racobit
 */

#ifndef DEFINE_MACRO_H_
#define DEFINE_MACRO_H_

/**
 * \enum dev_type_enum
 * @brief 配置设备sn时使用到的设备类型信息
 */
enum dev_type_enum
{
	DEV_UNKNOWN 			= 0,	///< 未知设备
	DEV_CAM 				= 1,	///< 摄像头
	DEV_MICROWAVE_RADAR 	= 2,	///< 毫米波雷达
	DEV_EDGE_COMPUTE_MODE 	= 3, 	///< 边缘计算设备
};



#define SET_DEVICE_SN(YEAR, MON, DAY, DEV_TYPE, DEV_NUM) ((YEAR << 20) + (MON << 16) + (DAY << 11) + (DEV_TYPE << 8) + DEV_NUM)
#define SET_PROC_VER(MAIN, SUB, FIXED) ((MAIN << 24) + (SUB << 16) + (FIXED << 8) + 0x00)



#endif /* DEFINE_MACRO_H_ */
