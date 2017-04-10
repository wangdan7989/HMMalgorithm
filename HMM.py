# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''


import string
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import UserSequences


def load_file(file_name):
    """
    读取文件，按列返回列表
    :param file_name: 文件路径
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
        print self.cixin_map
        del vocab_list
        print '初始化完毕'

    def hmm(self, usersequences):
        """
        :param usersequences: 用户的行为序列
        :return: 对应用户行为序列的转移概率序列
        """
        state_seq = []
        usersequences = usersequences
        state = ''
        pre_state = usersequences[0][1]+'\n'
        prob = 0
        for i in range(len(usersequences)):
            state = usersequences[i][1]
            state = state+'\n'
            #print state
            #print self.cixin_map['SNSSS\n']
            #print self.cixin_map[state], '****',self.cixin_map[pre_state]
            try:
                if self.cixin_map.has_key(state):
                    #print self.cixin_map[state], self.cixin_map[pre_state]
                    prob = self.trans_pro_matrix[self.cixin_map[state]][self.cixin_map[pre_state]]
                else:
                    #print state,"没有在cixin_map里"
                    state_seq.append(0)
                    #print i,state_seq[i]
                    continue

            except KeyError:
                pass
            state_seq.append(prob)
            pre_state = state

        result_state = state_seq
        return result_state

if __name__ == '__main__':

    H = HMM()
    import time
    t1 = time.time()
    user = UserSequences.GetUserSequences('MAR0955')
    result = H.hmm(user)
    #for i in range(len(result)):
     #   print i,result[i]
    t2 = time.time()

    xmajorLocator = MultipleLocator(100)

    ymajorLocator = MultipleLocator(2)
    fig = plt.figure()
    ax = subplot(111)
    y = result[:1500]
    x=range(len(y))
    plt.ylim(-3,3)
    #print x
    #y=[0.1,0.2,0.3,0.4,0.5]
    #plt.plot(x,result,'--r*')
    plt.plot(x,y)
    #plt.plot(x, result)
    #plt.legend()
    plt.show()

