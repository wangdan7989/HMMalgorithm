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

    for i in (range(len(list) - k)):
        sequ = ''
        state = ''
        for j in range(k):

            sequ = sequ+list[i+j][1]+'-'
            state = state+str(list[i+j][1])[0]
        #sequ = list[i][1] + '-' + list[i + 1][1] + '-' + list[i + 2][1] + '-' + list[i + 3][1] + '-' + list[i + 4][1]
        #state = str(list[i][1])[0] + str(list[i + 1][1])[0] + str(list[i + 2][1])[0] + str(list[i + 3][1])[0] + \
         #       str(list[i + 4][1])[0]
        #print sequ, state
        tem = [sequ, state]
        if state not in StandSequence.keys():
            StandSequence[state] = sequ
        UserSequence.append(tem)

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
    return UserSequence

if __name__  == '__main__':
    GetUserSequences('CEL0561')
