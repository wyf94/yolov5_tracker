/*
 * lowcost_err.h
 *
 *  Created on: Dec 29, 2021
 *      Author: racobit
 */

#ifndef LOWCOST_ERR_H_
#define LOWCOST_ERR_H_

#include <stdio.h>
#include <errno.h>

#ifdef __cplusplus
extern "C"{
#endif

#define ERR_PRINT(return_code, errmsg, ...)	{fprintf(stderr, "at %s, line: %d, error: %s, "errmsg"\n", __func__, __LINE__, strerror(errno), ##__VA_ARGS__); return return_code;}

#ifdef __cplusplus
}
#endif

#endif /* LOWCOST_ERR_H_ */
