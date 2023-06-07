/*
 * lowcost_socket.h
 *
 *  Created on: Dec 27, 2021
 *      Author: noven_zhang
 */

#ifndef LOWCOST_SOCKET_H_
#define LOWCOST_SOCKET_H_


#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/un.h>

//#include <netinet/in.h>
#include <arpa/inet.h>

#include <common/err/lowcost_err.h>

#ifdef __cplusplus
extern "C" {
#endif


/**
 * @brief linux 本地socket通信时连接服务端使用
 * @param[in] socket_path: local socket需要的socket地址
 * @param[in] timeout_s: 超时时间，单位为s
 * @return int
 * 	@retval >0: 链接上的socket值
 * 	@retval -1: 创建socket失败
 * 	@retval -2: 链接超时
 */
extern int linux_ipc_socket_connect(char* socket_path, int timeout_s);

/**
 * @brief socket rcv listen函数，创建listen客户端，接收发送端发送的数据
 * @param socket_path	: socket绑定的file路径和名称
 * @return
 * 	@retval >0 	: 连接上的socket 描述符
 * 	@retval -1	: 输入参数错误
 * 	@retval -2	: 创建socket失败
 * 	@retval -3	: unlink失败
 * 	@retval -4	: bind路径失败
 * 	@retval -5	: listen失败
 * 	@retval -6	: accept失败
 */
extern int socket_rcv_listen(char *socket_path);

/**
 * @brief socket 接收数据
 * @param[in] socket_flag, socket信息，linux_ipc_socket_connect的返回值
 * @param[in] data_addr, 接收数据存放的地址
 * @param[in] data_len，需要接收的数据的长度
 * @return int
 * 	@retval 0： 成功
 * 	@retval -1 ： 失败
 */
extern int linux_ipc_socket_recv(int socket_flag, void* data_addr, unsigned int data_len);

/**
 * @brief socket发送函数
 * @param[in] socket_flag, socket信息，linux_ipc_socket_connect的返回值
 * @param[in] data_addr, 发送的数据的地址
 * @param[in] data_len, 发送的数据的长度，单位: 字节
 * @return int
 * 	@retval -1 : 发送失败，发送失败需要重新链接socket
 * 	@retval >=0 : 发送数据的长度
 */
extern int linux_ipc_socket_send(int socket_flag, const void* data_addr, unsigned int data_len);

/**
 * @brief socket断开链接
 * @param[in] socket_flag, socket信息，linux_ipc_socket_connect的返回值
 * @return int
 * 	@return -1, 失败
 * 	@return 0, 成功
 */
extern int linux_ipc_socket_disconnected(int socket_flag);

/**
 * @brief : 通过udp将数据发送到指定IP和Port
 * @param[in] : ip, 接收端的IP
 * @param[in] : port， 接收端口
 * @param[in] : socket_fd， 初始化函数返回结果
 * @param[in] : addr， 发送的数据的地址
 * @param[in] : data_len， 发送的数据长度，单位：字节
 * @return int32_t
 * 	@retval >=0, 成功
 * 	@retval <0, 失败
 */
extern int32_t linux_ipc_socket_net_udp_send_sendto(char* ip, unsigned int port, int32_t socket_fd, void* addr, uint32_t data_len);

/**
 * @brief : udp初始化函数，创建发送的socket
 * @return int32_t
 * 	@retval >0 : 成功，socket fd
 * 	@retval <0 : 失败
 */
extern int32_t linux_ipc_socket_net_udp_send_init();

/**
 * @brief : linux socket通信创建tcp server，并且监听IP和端口
 * @param[in] : ip， tcp server监听的IP
 * @param[in] : port, tcp server 监听的port
 * @return int32_t
 * 	@retval >0, 成功，返回客户端的socket fd
 * 	@retval <0, 失败
 */
extern int32_t linux_ipc_socket_net_tcp_srv_init(char* ip, uint32_t port, int32_t *socket_srv_addr);


extern int32_t linux_ipc_socket_net_tcp_cli_init(char* ip, uint32_t port);
/**
 * @brief : 关闭socket连接
 * @param[in] : socket_fd, linux_ipc_socket_net_tcp_srv_init的返回值
 */
extern int32_t linux_ipc_socket_net_tcp_srv_close(int32_t socket_fd);

/**
 * @brief : tcp 发送数据函数
 * @param[in] socket_fd, socket fd, linux_ipc_socket_net_tcp_srv_init的返回值
 * @param[in] buf, 发送的数据的地址
 * @param[in] buf_len, 发送的数据长度
 * @return int32_t
 * 	@retval 0, 成功
 * 	@retval <0, 失败
 */
extern int32_t linux_ipc_socket_net_tcp_send(int socket_fd, void* buf, uint32_t buf_len);

/**
 * @brief : tcp 接收数据函数
 * @param[in] socket_fd, linux_ipc_socket_net_tcp_srv_init的返回值
 * @param[in] buf, 接收的数据的地址
 * @param[in] buf_len, 发送的数据长度
 * @return int32_t
 * 	@retval 0, 成功
 * 	@retval <0, 失败
 */
extern int32_t linux_ipc_socket_net_tcp_recv(int32_t socket_fd, void* buf, uint32_t recv_len);

/**
 * @brief socket rcv listen函数，创建listen客户端，接收发送端发送的数据，无accept版本，使用accept需要调用 socket_rcv_accept
 * @param socket_path	: socket绑定的file路径和名称
 * @return
 * 	@retval >0 	: 创建的server的socket 描述符
 * 	@retval -1	: 输入参数错误
 * 	@retval -2	: 创建socket失败
 * 	@retval -3	: unlink失败
 * 	@retval -4	: bind路径失败
 * 	@retval -5	: listen失败
 */
extern int ipc_socket_rcv_listen_no_accept(char *socket_path);

/**
 * @brief : ipc socket的accept 函数
 * @param[in]: srv_fd, 服务端socket
 * @return : int32_t
 * 	@retval: >0， 成功
 * 	@retval: <0, 失败
 */
extern int32_t ipc_socket_rcv_accept (int32_t srv_fd);

/**
 * @brief : linux socket通信创建tcp server，并且监听IP和端口
 * @param[in] : ip， tcp server监听的IP
 * @param[in] : port, tcp server 监听的port
 * @return int32_t
 * 	@retval >0, 成功，返回服务端的socket fd
 * 	@retval <0, 失败
 */
extern int32_t linux_net_socket_tcp_srv_init_no_accept(char* ip, uint32_t port);

/**
 * @brief : net socket链接中的accept函数
 * @param[in]: srv_fd, linux_net_socket_tcp_srv_init_no_accept的返回值，创建的socket信息
 * @return
 * 	@retval: >0, 成功，链接的客户端的socket
 * 	@retval: <0, 失败
 * @note： 当使用完socket或者socket出现异常后，需要调用linux_ipc_socket_net_tcp_srv_close释放资源
 */
extern int32_t linux_net_socket_tcp_accept(int32_t srv_fd);



#ifdef __cplusplus
}
#endif
#endif /* LOWCOST_SOCKET_H_ */
