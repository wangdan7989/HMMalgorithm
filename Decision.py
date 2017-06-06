# -*- coding: utf-8 -*-
'''
Created on 2017-04-25

@author: Wangan

说明
通过计算每个用户的状态转移概率的平均值来判断是否是威胁用户，
如果平均值大于0.8则是则是正常用户，反之则是威胁用户，
结果：
正常用户测试准确率：0.797297297297
normal_P=判断正确的正常用户/总的正常用户


威胁用户测试准确率：0.928571428571
abnormal_P=判断正确的异常用户/总的异常用户


总的正确率：0.861111111111
'''
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
def Decision():
    normal_pro = []
    abnormal_pro = []
    f = open('./data/Result.txt')
    line = f.readline()
    while line:
        words = line.split(':')
        #print len(words[2])

        if words[2] == ' 1\n':
            abnormal_pro.append(float(words[1]))
        elif words[2] == ' 0\n':
            normal_pro.append(float(words[1]))

        line = f.readline()
    print abnormal_pro
    print '*****************************'
    print normal_pro

    f.close()

    normal_num = 0
    abnormal_num = 0
    normal_P = 0
    normal_R = 0
    abnormal_P = 0
    abnormal_R = 0
    A = 0

    for item in normal_pro:
        if item >0.8:
            normal_num +=1

    for item in abnormal_pro:
        if item <0.8:
            abnormal_num +=1

    normal_P = float(normal_num)/float(len(normal_pro))
    abnormal_P = float(abnormal_num) / float(len(abnormal_pro))

    A = float((normal_num+abnormal_num))/float((len(normal_pro)+len(abnormal_pro)))
    print 'normal_P:',normal_P
    print 'abnormal_P:', abnormal_P
    print 'A:', A

    xmajorLocator = MultipleLocator(100)

    ymajorLocator = MultipleLocator(2)
    fig = plt.figure()
    ax = subplot(111)
    y1 = normal_pro
    x1=range(len(y1))
    y2 = abnormal_pro
    x2=range(len(y2))
    #plt.ylim(-1,1)
    #print x
    #y=[0.1,0.2,0.3,0.4,0.5]
    #plt.plot(x,result,'--r*')
    plt.plot(x1,y1,'-b*')
    plt.plot(x2, y2, '-r*')
    #plt.plot(x, result)
    #plt.legend()
    plt.show()

if __name__ == '__main__':
    Decision()