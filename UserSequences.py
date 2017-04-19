# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''

import SingleSequence

def GetUserSequences(employee):
    list=SingleSequence.GetUserSingleSequence(employee)
    k=6
    UserSequence = []

    for i in (range(len(list) - k)):
        sequ = ''
        state = ''
        for j in range(k):
            sequ = sequ+list[i+j][1]+'-'
            state = state+str(list[i+j][1])[0]

        tem = [sequ, state]
        UserSequence.append(tem)


    f = open('./data/UserSequence.txt', 'w')
    for i in range(len(UserSequence)):
        f.write(UserSequence[i][0])
        f.write(':')
        f.write(UserSequence[i][1])
        f.write('\n')
        #print UserSequence[i]
    f.close()

    return UserSequence


def GetStandeSequence(user_list):
    StandSequence = {}
    for user in user_list:
        usersequence = GetUserSequences(user)
        for i in range(len(usersequence)):
            state = usersequence[i][1]
            if state not in StandSequence.keys():
                StandSequence[state] = 1
            else:
                StandSequence[state] += 1

    f = open('./data/StandeSequence.txt', 'w')
    for key, value in StandSequence.items():
        if value > 5:
            value = str(value)
            f.write(value)
            f.write(':')
            f.write(key)
            f.write('\n')
            print key, value
    f.close()

    return StandSequence
if __name__  == '__main__':
    #user = 'CEL0561'
    #GetUserSequences(user)

    user_list = ['RSC0089']
    GetStandeSequence(user_list)