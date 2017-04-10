这是基于隐马尔科夫模型实现的用户时间行为序列异常检测
Url:U
FileCopy:F
Connect:C
DIsconnect:D
Sendmail:S
Logon:L
Nologon:N

方式：
首先去掉UserSequences中的写入文件的注释，找一个当做生成用户标准的用户运行，得到标准的训练数据文件UserSequence.txt
如果需要改K值，也就是自定义的用户行为序列的命令个数也是在上面的方式下修改
然后注释掉写入文件
运行preProcess，得到状态转换矩阵，以及其他的状态映射表
最后运行HMM，输入需要测试的用户的user
