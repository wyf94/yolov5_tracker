/*
 * video_process_shared_lib.h
 *
 *  Created on: Jan 10, 2022
 *      Author: racobit
 */

#ifndef VIDEO_PROCESS_SHARED_LIB_H_
#define VIDEO_PROCESS_SHARED_LIB_H_


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "common/socket/lowcost_socket.h"
#include "common/global/struct_lowcost_data.h"

#ifdef __cplusplus
	extern "C" {
#endif

/**
 * @brief: 接收图像数据，格式为RGB
 * @param[in]: socekt_fd 接收数据使用的socket id
 * @param[in][out]: ret_img_data_addr 图像数据存放的地址
 * @param[in][out]: frame_count_addr 帧计数存放地址
 * @param[in][out]: timestamp 时间戳存放地址
 * @return: int
 * 	@retval >=0: 成功
 * 	@retval -1: 失败，输入参数错误
 */
extern int vp_img_data_recv(int socekt_fd, void* ret_img_data_addr, void *ret_frame_header_infso);

/**
 * @brief : vp部分发送结构化数据的结果
 * @param[in] msg_fd: 消息队列flag
 * @param[in] dev_sn: 设备序列号
 * @param[in] sensor_sn: 传感器序列号
 * @param[in] frame_count: 帧计数
 * @param[in] ver_main: 协议版本编号，主编号
 * @param[in] ver_sub: 协议版本编号，次编号
 * @param[in] ver_fixed: 协议版本编号，修正编号
 * @param[in] targets_infos_addr: 结构化目标信息数组，具体参见VIDEO_PER_TARGET_INFO
 * @param[in] targets_count: 目标个数
 * return int
 *  @retval  0: 成功
 *  @retval -1: 失败，输入参数错误
 */
int vp_img_process_send(int msg_fd, void* frame_header, void* targets_infos_addr, unsigned int targets_count);

#ifdef __cplusplus
	};
#endif


#endif /* VIDEO_PROCESS_SHARED_LIB_H_ */
