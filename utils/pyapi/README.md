
# 版本说明

## V0.2.alpha_0_V0.0.20

> 时间：2022.10.18
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 更新bbox选点位置计算放放，比例参数从数据帧头中获取，可以根据具体设备，领过配置不同的比例参数

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      config.yaml                           # 配置文件
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │          config.yaml                   # 配置文件
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```


## V0.2.alpha_0_V0.0.19

> 时间：2022.10.18
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 更新lib库和pyapi，更新bonding box选点位置计算方法， 目前参数适合亦庄avp 地面3号杆一体机设备，其余设备未做测试

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      config.yaml                           # 配置文件
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │          config.yaml                   # 配置文件
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```



## V0.2.alpha_0_V0.0.18

> 时间：2022.10.18
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 更新lib库和pyapi，修复vc头文件空间占用bug
>   2. 更新bin中0_video_capture 和 4_output_adapter以及config.yaml

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      config.yaml                           # 配置文件
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │          config.yaml                   # 配置文件
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```

## V0.2.alpha_0_V0.0.17

> 时间：2022.10.14
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改lib库，修改pyapi，增加在vp结果上标识图像resize后的值
>   2. 更新bin目录下程序，增加配置文件

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      config.yaml                           # 配置文件
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  ├─opencv4.1
    │      │  │      0_video_capture
    │      │  │      config.yaml                    # 配置文件
    │      │  │
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │          config.yaml                   # 配置文件
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```

## V0.2.alpha_0_V0.0.16

> 时间：2022.09.21
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改车辆车牌号数字长度，增加车牌号长度判定，出去差异性
>   2. 增加像素坐标位置转换，将像素坐标转换为东北天坐标
>   3. 修复若干BUG

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  ├─opencv4.1
    │      │  │      0_video_capture
    │      │  │
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```

## V0.2.alpha_0_V0.0.4

> 时间：2022.08.30
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改接口，适配内部协议V0.3.2, 在VP中增加目标所在车道编号信息

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  ├─opencv4.1
    │      │  │      0_video_capture
    │      │  │
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```

## V0.2.alpha_0_V0.0.3

> 时间：2022.08.26
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 增加VC对V4l2 相机的支持,生成新Video Capture: 0_vc_v4l2_cam，目前固定支持中彩500w USB相机，测试在Agx上运行效果：14fps，Tx2nx 上运行效果：11fps

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │      │  ├─opencv4.1
    │      │  │      0_video_capture
    │      │  │
    │      │  └─opencv4.5
    │      │          0_video_capture
    │      │
    │      └─V4l2_Cam                               # V4l2 相机图片获取程序
    │              0_vc_v4l2_cam
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```


## V0.2.alpha_0_V0.0.2

> 时间：2022.07.28
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 调整文档目录结构
>   2. 增加output adapter执行程序，用于接收输出结果
>   3. 修改pyapi中目标数据输出的兼容性

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─bin
    │  ├─output_adapture
    │  │      4_output_adapter                      # 接收内部协议，转换为STD格式的程序
    │  │      README.md                             # 使用说明
    │  │
    │  └─video_capture                              # 获取图像数据的软件
    │      └─Daheng_USB                             # 大恒USB相机数据获取软件，分别基于不同的opencv的版本
    │          ├─opencv4.1
    │          │      0_video_capture
    │          │
    │          └─opencv4.5
    │                 0_video_capture
    │
    ├─capi                                         
    │  │  sample.c                                   # 简单的示例程序 
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Libs                                          # Debug版本的动态库
    │  ├─opencv4.1
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5
    │          lib2_video_process_share_lib.so
    │
    └─pyapi                                         # Python API 文件夹
            vp_comm_lib_pyapi.py                    # Python API
            vp_pyapi_sample.py                      # Python API使用示例
```

## V0.2.alpha_0_V0.0.1

> 时间：2022.07.27
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 增加发送图像统计数据的接口， 复用当前接口，增加统计数据使用示例

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```


## V0.1.alpha_7_V0.1.7
> 时间：2022.05.11
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改VC发送帧头长度bug
>   2. 修改header接收赋值bug
>   3. 修改img接收数据长度bug
>   4. 修改pyapi ctypes list append bug，明确python中class的append后也是同一个空间的数据
>   5. 修改struct union使用bug

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

# 版本说明
## V0.1.alpha_7_V0.1.6
> 时间：2022.05.11
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改vp发送时帧头未使用的bug

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```


# 版本说明
## V0.1.alpha_7_V0.1.5
> 时间：2022.05.11
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改msg send函数bug，修改sample函数使用bug

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

# 版本说明
## V0.1.alpha_7_V0.1.4
> 时间：2022.05.11
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改Pyapi接口，实现将接收到的帧头传输到发送端
>   2. 简化发送端接口，修改数据格式，实现ctypes Union方式，实现新版本目标数据64字节对齐的需求
>   3. 修改图像接收函数，帧头和图像数据分开接收和发送

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

## V0.1.alpha_7_V0.1.3
> 时间：2022.05.09
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改PyApi接口，修正当车牌输入为空时的bug，增加判定
>   2. 修改pack函数，修改pack车牌的方式

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

## V0.1.alpha_7_V0.1.2
> 时间：2022.05.09
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改opencv 4.1库bug

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

## V0.1.alpha_7_V0.1.1
> 时间：2022.05.09
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改Python中stuct pack时输入为字符串类型转换问题
>   2. 修改库文件中输入数据长度判定错误问题

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

## V0.1.alpha_7_V0.1.0
> 时间：2022.05.07
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改整体的数据长度，修改目标信息格式，增加车牌输出
>   2. 目录结构增加opencv4.1 和opencv4.5两个版本的软件和库的支持

文档结构：

``` shell
│  README.md                                        # 本文件
│
└─arm64                                             # ARM64架构下的库文件和应用程序
    ├─capi                                          
    │  │  sample.c                                  # 简单的示例程序           
    │  │
    │  ├─common                                     # 使用lib库需要使用到的头文件
    │  │  ├─err                                     
    │  │  │      lowcost_err.h
    │  │  │
    │  │  ├─global
    │  │  │      define_macro.h
    │  │  │      struct_lowcost_data.h
    │  │  │
    │  │  └─socket
    │  │          lowcost_socket.h
    │  │
    │  └─include
    │          video_process_shared_lib.h           # 头文件
    │
    ├─Debug                                         # Debug版本的动态库
    │  ├─opencv4.1                                  # 基于opencv 4.1版本
    │  │      lib2_video_process_share_lib.so
    │  │
    │  └─opencv4.5                                  # 基于opencv 4.5版本
    │          lib2_video_process_share_lib.so
    │
    ├─pyapi                                         # Python API 文件夹
    │      vp_comm_lib_pyapi.py                     # Python API
    │      vp_pyapi_sample.py                       # Python API使用示例
    │
    └─video_capture                                 # 大恒相机数据获取软件
        ├─opencv4.1                                 # 基于opencv4.1版本
        │      0_video_capture
        │
        └─opencv4.5                                 # 基于opencv4.5版本
                0_video_capture

```

## V0.1.alpha_6_V0.1.0

无

## V0.1.alpha_5_V0.1.1

> 时间：2022.03.25
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 增加C API接口头文件和说明，并提供简单示例

文档结构：

``` shell
./
│  README.md                                # 本文件
│
└─arm64                                     # ARM64架构下的库文件和应用程序
    ├─capi
    │  │  sample.c                          # 简单的示例程序
    │  │  video_process_shared_lib.h        # 示例使用的头文件
    │  │
    │  ├─common                             # 通用的头文件
    │  │  ├─global
    │  │  │      define_macro.h             # 宏定义头文件
    │  │  │      struct_lowcost_data.h      # 数据结构体头文件
    │  │  │
    │  │  └─socket                  
    │  │          lowcost_socket.h          # socket头文件
    │
    ├─Debug                                 # DEBUG版本
    │      lib2_video_process_share_lib.so  # 库文件
    │
    ├─pyapi                                 # python API 文件夹
    │      vp_comm_lib_pyapi.py             # python API 文件
    │      vp_pyapi_sample.py               # 调用PyAPI的示例程序
    │
    └─video_capture                         # 配套的获取摄像头数据的程序文件夹
            0_video_capture                 # 可执行程序, -h显示使用说明
```

## V0.1.alpha_5_V0.1.0

> 时间：2022.03.22
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改数据接口保留项，保留到1024位，保证所有数据统一
>   2. 增加原始数据输出协议的图片格式字段

文档结构：

``` shell
./
│  README.md                                # 本文件
│
└─arm64                                     # ARM64架构下的库文件和应用程序
    ├─Debug                                 # DEBUG版本
    │      lib2_video_process_share_lib.so  # 库文件
    │
    ├─pyapi                                 # python API 文件夹
    │      vp_comm_lib_pyapi.py             # python API 文件
    │      vp_pyapi_sample.py               # 调用PyAPI的示例程序
    │
    └─video_capture                         # 配套的获取摄像头数据的程序文件夹
            0_video_capture                 # 可执行程序
```

## V0.1.alpha_4_V0.1.0

> 时间：2022.02.11
>
> 修改人：张振康
>
> 修改说明：
>
>   1. API中增加sensor_sn,传感器编号和设备编号区分

文档结构：

``` shell
./
│  README.md                                # 本文件
│
└─arm64                                     # ARM64架构下的库文件和应用程序
    ├─Debug                                 # DEBUG版本
    │      lib2_video_process_share_lib.so  # 库文件
    │
    ├─pyapi                                 # python API 文件夹
    │      vp_comm_lib_pyapi.py             # python API 文件
    │      vp_pyapi_sample.py               # 调用PyAPI的示例程序
    │
    └─video_capture                         # 配套的获取摄像头数据的程序文件夹
            0_video_capture                 # 可执行程序
```

## V0.1.alpha_3_V0.1.1

> 时间：2022.02.10
>
> 修改人：张振康
>
> 修改说明：
>
>   1. 修改vp_pyapi_sample.py中关于msg测试的问题
>   2. 修改vp_comm_lib_pyapi.py中vp处理结果信息的结构体内容
>   3. 修改二进制数据打包是字节对齐bug

文档结构：

``` shell
./
│  README.md                                # 本文件
│
└─arm64                                     # ARM64架构下的库文件和应用程序
    ├─Debug                                 # DEBUG版本
    │      lib2_video_process_share_lib.so  # 库文件
    │
    ├─pyapi                                 # python API 文件夹
    │      vp_comm_lib_pyapi.py             # python API 文件
    │      vp_pyapi_sample.py               # 调用PyAPI的示例程序
    │
    └─video_capture                         # 配套的获取摄像头数据的程序文件夹
            0_video_capture                 # 可执行程序
```

## V0.1.alpha_3_V0.1.0

``` shell
./
│  README.md                                # 本文件
│
└─arm64                                     # ARM64架构下的库文件和应用程序
    ├─Debug                                 # DEBUG版本
    │      lib2_video_process_share_lib.so  # 库文件
    │
    ├─pyapi                                 # python API 文件夹
    │      vp_comm_lib_pyapi.py             # python API 文件
    │      vp_pyapi_sample.py               # 调用PyAPI的示例程序
    │
    └─video_capture                         # 配套的获取摄像头数据的程序文件夹
            0_video_capture                 # 可执行程序
```
