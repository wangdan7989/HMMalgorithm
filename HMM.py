# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''


import string
import matplotlib.pyplot as plt
import numpy as np
import UserSequence

def load_file(file_name):
    """
    读取文件，按列返回列表
    :param file_name: 文件路径
    :param charset: 文本内容decode的编码，默认为utf-8
    :return: 文本内容列表
    """
    f1 = open(file_name)
    line = f1.readline()
    line_list = []
    while line:
        line_list.append(line)
        line = f1.readline()
    return line_list
class HMM:
    def __init__(self):
        """
        初始化
        :return:
        """
        self.cixin_list = load_file('./data/state_map.txt')
        self.cixin_map = dict(zip(self.cixin_list, range(self.cixin_list.__len__())))  # 词性映射哈希表
        self.trans_pro_matrix = np.loadtxt('./data/A.txt') # 转移概率矩阵
        vocab_list = load_file('./data/state_map.txt')
        self.vocab_map = dict(zip(vocab_list, range(vocab_list.__len__())))  # 词语映射哈希表
        #self.emitter_pro_matrix = np.loadtxt('./data/B.txt')  # 发射概率矩阵
        #print self.cixin_list
        #print self.cixin_map
        #print vocab_list
        #print self.vocab_map
        del vocab_list
        print '初始化完毕'


def hmm(self, usersequence):
    """
    :param usersequence: 用户的行为序列
    :return: 对应用户行为序列的转移概率序列
    """

    return result_cixin

if __name__=='__main__':
    H = HMM()
    import time
    t1 = time.time()
    print H.hmm([u'结合', u'成', u'分子', u'时'])
    t2 = time.time()
"""
    print 11
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)
    x=[1,2,3,4,5]
    y=[0.1,0.2,0.3,0.4,0.5]
    plt.plot(x,y)
    plt.show()
"""

