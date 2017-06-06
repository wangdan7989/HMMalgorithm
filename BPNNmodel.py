# -*- coding: utf8 -*-
'''
Created on 2017-04-25

@author: Wangan

说明
为前馈神经网络，对前面的隐马尔科夫状态序列进行分类，正确率在60左右，linux下有一个基于tenserflow的前馈神经网络代码，精度在82
输入为用户的状态转移概率序列，输出为正常和威胁两个值
'''
import random
import math
import matplotlib.pyplot as plt
import copy
import time

import pickle

def rand(a, b):
    ''' 生成[a,b)内的随机数 '''
    return (b - a)*random.random() + a

def makeMatrix(I, J, fill=0.0):
    ''' 生成 I*J 大小的矩阵 '''
    return [[fill]*J for i in range(I)]

def sigmoid(x):
    ''' 激活函数 '''
    #return math.tanh(x)
    #return 1.0/(1 + math.exp(-x))
    return 0.5 * (1 + math.tanh(0.5 * x))

class Neuron:
    def __init__(self, ni, nh, no, A = 0.5, B = 0.1):
        ''' 输入层，隐层，输出层的初始化 '''
        # 网络学习率和动量因子设定
        self.A = A
        self.B = B
        # 考虑到神经元阈值，输入层+1，且应初始化为 1
        self.ni = ni + 1
        self.nh = nh
        self.no = no
        # 设置各层的存储向量
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no
        # 最后建立动量因子矩阵
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)
        # 设置权值矩阵
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # 初始化权值矩阵
        for i in range(self.ni):
            for j in range(self.nh):
                for k in range(self.no):
                    self.wi[i][j] = rand(-0.2, 0.2)
                    self.wo[j][k] = rand(-2.0, 2.0)

    def runfront(self, inputs):
        ''' 正向传播，inputs为单个训练样本输入'''
        if len(inputs) != self.ni - 1:
            raise ValueError("输入节点数错误")
        # 计算输入层输出
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]
        # 计算隐层输出
        for j in range(self.nh):
            self.ah[j] = sigmoid(sum([self.ai[i]*self.wi[i][j]  for i in range(self.ni)]))
        # 计算输入层输出
        for k in range(self.no):
            self.ao[k] = sigmoid(sum([self.ah[j]*self.wo[j][k] for j in range(self.nh)]))
        return self.ao

    def runback(self, outputs):
        ''' 反向传播, outputs为训练样本期望输出 '''
        Error = 0.0   # 网络误差
        if len(outputs) != self.no:
            raise ValueError('输出节点数错误')
        # 计算输出层误差
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            reo = self.ao[k]   # 实际输出
            wano = outputs[k]  # 期望输出
            output_deltas[k] = (wano - reo) * (1 - reo**2)
            Error += 0.5 * (wano - reo)**2   # 计算整体网络误差
        # 计算隐层误差
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            reo = self.ah[j]
            error = 0.0
            for k in range(self.no):
                error +=  output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = (1 - reo**2) * error
        # 更新输出层权值
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += self.A * change + self.B * self.co[j][k]
                self.co[j][k] = change
        # 更新隐层权重
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] += self.A * change  + self.B * self.ci[i][j]
                self.ci[i][j] = change
        return Error

    def train(self, dataSet, iteration):
        ''' 训练网络，打印训练样本的整体误差 '''
        Logger = []  # 记录迭代中的误差变化
        for i in range(iteration):
            All_Error = 0.0
            for data in dataSet:
                self.runfront(data[0])
                All_Error += self.runback(data[1])
            Logger.append(All_Error)
            if i%100 == 0:
                print i, "Iter's error: ", All_Error

        print "样本已完成%d次迭代训练"%iteration,"下面开始测试\n"
        return Logger

def ConstructNN():

    # 构造神经网络
    N_In = 2412  # 输入层神经元数量 25 2412
    N_Out = 2    # 输出层神经元数量 3 2
    N_Hidden = 8   # 隐层神经元数量 8 55
    N_Train = 1000    # 训练次数 1000
    Alpha = 0.8    # 学习常数 0.8
    Belta = 0.5   # 动量因子 0.5
    NN = Neuron(N_In, N_Hidden, N_Out, Alpha, Belta)

    Train_Set = GetTrain_Set()[:100]
    print Train_Set
    # 训练
    Logger = NN.train(Train_Set, N_Train)

    # 画误随迭代次数差变化图
    plt.plot(Logger)
    plt.xlim(0,150)
    plt.xlabel("Iteration-Count")
    plt.ylabel("Error")

    plt.show()
    return NN





def GetTrain_Set():
    # 2412个输入（序列概率(最大2412，最小98)） 标准输出有2个 [1,0] 正常/异常    一共144个用户
    # 从文件中获取训练数据
    Train_File = open('./data/ProSquenceResult.txt', 'r')
    Train_Set = []
    #N_Out = 10
    line = Train_File.readline()
    lennumber = []
    tem = []
    state = []  # state有两个数，第一个位置表示正常，第二个位置表示异常，符合的话为1，不符合的为0
    while line:
        line = line.split(':')
        line[1] = line[1].replace('[', '')
        line[1] = line[1].replace(']', '')

        words = str(line[1]).split(',')
        sta = float(line[2].replace('\n', ''))
        words = [float(item) for item in words]
        if sta == 1.0:
            state.append(0.0)
            state.append(1.0)
        else:
            state.append(1.0)
            state.append(0.0)

        lennumber.append(len(words))
        tem.append(words)
        tem.append(state)
        Train_Set.append(copy.deepcopy(tem))

        del tem[:2]
        del state[:2]
        line = Train_File.readline()

    Train_File.close()

    maxlen = max(lennumber)

    for i in range(len(Train_Set)):
        item = Train_Set[i]
        while len(item[0]) < maxlen:
            item[0].append(0.0)
        Train_Set[i] = item
    '''
    Train_Set = [
        [[1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1], [1, 0, 0]],  # 燕子图案
        [[1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1], [0, 1, 0]],  # 箭头
        [[1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1], [0, 0, 1]]  # 方块
    ]
    '''
    return Train_Set


# 测试
def test(n, NN,Train_Set):
    res = NN.runfront(Train_Set[n][0])
    ide = Train_Set[n][1]
    print 'res ide:',len(Train_Set[0][0])
    print "  -实际输出 => [", ", ".join(["%.3f"%d for d in res ]), "]"
    print "  -理想输出 => [", ", ".join(["%.3f"%d for d in ide ]), "]"
    print


if __name__  == '__main__':
    t1 = time.time()

    NN = ConstructNN()
    Train_Set = GetTrain_Set()
    '''
    #将原来的格式按照 标签+特征+换行  写入新的文件NewProSquenceResult

    f = open('./data/NewProSquenceResult.txt', 'w')
    for item in Train_Set:
        if item[1][0] == 1:
            f.write('1,')
        else:
            f.write('2,')
        for w in item[0]:
            f.write(str(w)+',')
        f.write('\n')
        #print item
    '''
    t2 = time.time()

    print 'time:',t2-t1
    count = 100
    while count < 144:
        test(count, NN, Train_Set)
        count += 1











