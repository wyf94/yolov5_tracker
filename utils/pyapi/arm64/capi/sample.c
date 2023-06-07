/*
 * main.c
 *
 *  Created on: Jan 13, 2022
 *      Author: racobit
 */


#include "include/video_process_shared_lib.h"


int main()
{

	int socket_fd = socket_rcv_listen("/tmp/lowcost_vc2vp.socket");

	char* img_data = (char*)malloc(2448*2048*3);
	unsigned int frame_count = 0;
	double timestamp;

	VC_STRUCT img_data_struct = {0};


	while(1)
	{
		vp_img_data_recv(socket_fd, img_data, &img_data_struct.union_frame_head_infos.struct_infos.dev_sn);
	}



	free(img_data);

	return 0;
}




