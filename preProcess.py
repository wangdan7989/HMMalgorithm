# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan

说明
从 199801文档中 统计转移概率和发射概率 并分别导出转移矩阵和发射矩阵.

运行完毕后
共生成5个txt
cixin_map.txt:  词性列表 用来获得每个词性映射在矩阵中对应的索引
A.txt:  转移矩阵
cixin_pro.txt:  词性概率列表 每个词性对应出现的概率
vocab_map.txt:  词列表 用来获得每个词映射在矩阵中对应的索引
B.txt:  发射矩阵
'''
import numpy as np


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


def row_normalization(X):
    """
    按行归一化
    :param X: 矩阵
    :return: 归一化后的矩阵
    """
    print X
    X.dtype = 'float'
    try:
        X.shape[1]
    except IndexError:
        Max = np.max(X)
        Min = np.min(X)
        X = (X - Min) / (Max - Min)
        return X

    for l in range(X.shape[0]):
        Max = np.max(X[l])
        Min = np.min(X[l])
        if (Max-Min) == 0:
            X[l] = np.zeros(X[l].shape)
            continue
        X[l] = (X[l] - Min) / (Max - Min)
    return X


if __name__ == '__main__':
    lines = load_file("./data/UserSequence.txt")

    # 统计多少种词性
    cixin_set = set()
    for line in lines:
        words = line.split(':')
        #print words[1]
        cixin_set.add(words[1])

    cixin_num = cixin_set.__len__()
    print cixin_num
    cixin_map = dict(zip(list(cixin_set), range(cixin_num)))  # cixin_map['j']表示该词性在词性表对应的索引位置

    trans_pro_matrix = np.zeros((cixin_num, cixin_num))  # 转移矩阵
    cixin_pro = np.zeros(cixin_num, dtype=float)  # 每个词性出现的概率
    pre_cixin = ''
    cixin = ''
    for line in lines:
        words = line.split(':')
        cixin = (words[1])
        cixin_pro[cixin_map[cixin]] += 1
        try:
            trans_pro_matrix[cixin_map[cixin]][cixin_map[pre_cixin]] += 1
        except KeyError:
            pass
        pre_cixin = cixin

    trans_pro_matrix = row_normalization(trans_pro_matrix)  # 按行标准化后得转移概率矩阵

    cixin_pro = row_normalization(cixin_pro)
    np.savetxt('./data/A.txt', trans_pro_matrix)  # 保存转移矩阵为A.txt
    np.savetxt('./data/state_pro.txt', cixin_pro)  # 保存词性概率列表为cixin_pro.txt
    f = open('./data/state_map.txt', 'w')
    for i in cixin_set:
        f.write(i)
        f.write('\n')
    f.close()
"""
    vocab_lines = load_file("./data/chineseDic.txt", 'GBK')
    vocab_list = []
    for vocab_line in vocab_lines:
        vocab_list.append(vocab_line.split(',')[0])
    vocab_map = dict(zip(vocab_list, range(vocab_list.__len__())))
    emitter_pro_matrix = np.zeros((vocab_list.__len__(), 44))
    for line in lines:
        words = line.split()
        for word in words:
            vocab, cixin = word.split('/')
            try:
                emitter_pro_matrix[vocab_map[vocab]][cixin_map[cixin]] += 1
            except KeyError:
                # print vocab, '不在词库内 忽略不计'
                pass

    emitter_pro_matrix = row_normalization(emitter_pro_matrix)
    np.savetxt('./data/B.txt', emitter_pro_matrix)  # 保存发射矩阵为B.txt
    f = open('./data/vocab_map.txt', 'w')
    for vocab in list(vocab_list):
        f.write(vocab.encode('utf-8'))
        f.write('\n')
    f.close()
"""