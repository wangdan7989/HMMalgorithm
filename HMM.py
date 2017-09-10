# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
构造hmm类，训练部分的算法在preProcess中，包括转移矩阵和发射矩阵的构建，该文件主要是根据前面的矩阵进行模型的预测功能，得到相应的状态序列
'''


import preProcess
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import UserSequences
import CSVFile


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
    def __init__(self,user):
        """
        初始化
        :return:
        """
        AFile = './data/allusers/Amatrix/' + user + 'A.txt'
        state_mapFile = './data/allusers/Statemap/' + user + 'state_map.txt'

        self.state_list = load_file(state_mapFile)#'./data/allusers/state_map.txt'
        self.state_map = dict(zip(self.state_list, range(self.state_list.__len__())))  # 词性映射哈希表
        self.trans_pro_matrix = np.loadtxt(AFile) # 转移概率矩阵 './data/allusers/A.txt'
        vocab_list = load_file(state_mapFile)#'./data/allusers/state_map.txt'
        self.vocab_map = dict(zip(vocab_list, range(vocab_list.__len__())))  # 词语映射哈希表
        del vocab_list
        #print '初始化完毕'

    def hmm(self, user):
        """
        :param usersequences: 用户的行为序列
        :return: 对应用户行为序列的转移概率序列
        """

        state_seq = []

        #usersequences = usersequences
        usertestfile = "./data/allusers/Test/" + user + ".csv"
        usersequences = CSVFile.loadCSVfile1(usertestfile)
        state = ''
        pre_state = usersequences[0][1]+'\n'
        prob = 0
        for i in range(len(usersequences)):
            state = usersequences[i][1]
            state = state+'\n'

            try:
                if self.state_map.has_key(state) == False:
                    state = 'other\n'
                prob = self.trans_pro_matrix[self.state_map[state]][self.state_map[pre_state]]

            except KeyError:
                pass
            state_seq.append(prob)
            pre_state = state

        result_state = state_seq
        return result_state

    def hmmV2(self, usersequences):
        """
        :param usersequences: 用户的行为序列
        :return: 对应用户行为序列的转移概率序列
        """

        state_seq = []

        usersequences = usersequences
        #usertestfile = "./data/allusers/Test/" + user + ".csv"
        #usersequences = CSVFile.loadCSVfile1(usertestfile)
        state = ''
        pre_state = usersequences[0] + '\n'
        prob = 0
        for i in range(len(usersequences)):
            state = usersequences[i]
            state = state + '\n'

            try:
                if self.state_map.has_key(state) == False:
                    state = 'other\n'
                prob = self.trans_pro_matrix[self.state_map[state]][self.state_map[pre_state]]

            except KeyError:
                pass
            state_seq.append(prob)
            pre_state = state

        result_state = state_seq
        del(result_state[0])
        #每天的概率相乘
        #result = Getproduct(result_state)
        # 每天的概率相加（MM）
        result = Getsum(result_state)
        #print (Getproduct(result_state))
        return result

def Getproduct(list):
    num = 1
    for i in list:
        num *= i
    return num

def Getsum(list):
    num = 1
    for i in list:
        num += i
    return num

if __name__ == '__main__':
    user = 'DLM0051'
    start_date = '2010-1-01'
    finish_date = '2011-1-28'


    if len(UserSequences.GetStandeSequence(user, start_date, finish_date)) <1:
    #if len(UserSequences.GetUserSequences(user, start_date, finish_date)) < 1:
        print 1111
    preProcess.GetTransiMatrix(user)
    start_date = '2011-1-28'
    finish_date = '2011-4-30'
    usersequence = UserSequences.GetUserSequences(user, start_date, finish_date)
    H = HMM(user)
    result = H.hmm(usersequence)
    print "result:",result
    print average(result)


    xmajorLocator = MultipleLocator(100)

    ymajorLocator = MultipleLocator(2)
    fig = plt.figure()
    ax = subplot(111)
    y = result[:1000]
    #y = result
    x=range(len(y))
    plt.ylim(-3,3)
    #print x
    #y=[0.1,0.2,0.3,0.4,0.5]
    #plt.plot(x,result,'--r*')
    plt.plot(x,y)
    #plt.plot(x, result)
    #plt.legend()
    plt.show()

