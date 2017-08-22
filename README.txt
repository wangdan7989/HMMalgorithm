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


hmm文件主要是构建hmm类的，可以进行单个用户的测试
gethmmresult文件是得到144个用户的状态序列，并写入文件ProSquenceResult.txt
decision：操作ProSquenceResult.txt中的数据，通过计算每个用户的状态转移概率的平均值来判断是否是威胁用户，
			如果平均值大于0.8则是则是正常用户，反之则是威胁用户
BNNmodel：用神经网络来对ProSquenceResult.txt中的数据进行分类

NewProSquenceResult.txt:对原来的格式进行改变为：标签+特征+换行  便于基于linux下有一个基于tenserflow的前馈神经网络代码的输入