# 使用说明

## Version: 0.2.alpha_00.build_001

### 使用说明

1. `./4_output_adapter -h` 可以查看使用说明

``` shell
[Help]
 Usage: [ENV_VAR_SET] ./4_output_adapter [OPTION]

[OPTIONS]:
 -m N                :指定模式，【N】表示选择的模式
                      模式可以从以下列表中选择,'【】'中为模式编号
                     【 1】: 捕获的原始图像信息
                     【 2】: 捕获的雷达信息
                     【 3】: 图像处理结果  
                     【 4】: 融合处理结果  
                     【 5】: STD结果输出     
 -i ip               :服务端IP地址, 【ip】表示服务端IP地址
 -p port             :服务端端口, 【port】表示服务端端口
 -r recv_socket_path :接收的socket的路径, 【recv_socket_path】接收的socket的路径
 -n snd_count        :发送的数据次数，测试使用, 【snd_count】发送的数据次数
 -q msg_queue_id     :消息队列ID, 【msg_queue_id】消息队列ID
 -v                  :查询当前软件版本
 -h                  :打印帮助信息

[ENV_VAR_SET]:
 DEBUG_PRINT_LV      :Debug打印信息等级，不同的等级代表打印不同深度的信息，注意，打印信息会影响性能
                     :0，表示不打印信息
                     :1，表示打印所有信息

```

2. 使用注意事项
    当前使用时，模式选择【5】，使用标准输出格式，同时需要指定【ip】【port】，否则会使用默认的IP和端口

3. 使用示例
   
   `./4_output_adapter -m 5 -i 192.168.10.100 -p 9001`

   如果想要查看输出结果，则需要添加`DEBUG_PRINT_LV=1`，例如：`DEBUG_PRINT_LV=1 ./4_output_adapter -m 5 -i 192.168.10.100 -p 9001`则可实现打印输出结果
