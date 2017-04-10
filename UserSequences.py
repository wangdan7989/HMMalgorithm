# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''

import SingleSequence

def GetUserSequences(employee):
    list=SingleSequence.GetUserSingleSequence(employee)
    k=4
    StandSequence = {}
    UserSequence = []
    sequ = ''
    state = ''
    for i in (range(len(list) - 4)):
        #for j in k:
          #  sequ=sequ+'-'+list[i+k][1]
        sequ = list[i][1] + '-' + list[i + 1][1] + '-' + list[i + 2][1] + '-' + list[i + 3][1] + '-' + list[i + 4][1]
        state = str(list[i][1])[0] + str(list[i + 1][1])[0] + str(list[i + 2][1])[0] + str(list[i + 3][1])[0] + \
                str(list[i + 4][1])[0]
        #print sequ, state
        tem = [sequ, state]
        if state not in StandSequence.keys():
            StandSequence[state] = sequ
        UserSequence.append(tem)
    return UserSequence
"""
    f = open('./data/UserSequence.txt', 'w')
    for i in range(len(UserSequence)):
        f.write(UserSequence[i][0])
        f.write(':')
        f.write(UserSequence[i][1])
        f.write('\n')
        print UserSequence[i]
    f.close()

    f = open('./data/StandeSequence.txt', 'w')
    for key, value in StandSequence.items():
        f.write(key)
        f.write(':')
        f.write(value)
        f.write('\n')
    f.close()
"""
if __name__ =='__main__':
    GetUserSequences('w')