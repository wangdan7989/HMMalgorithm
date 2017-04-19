# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''

import UserSequences

def GetStandeSequence(user_list):
    StandSequence = {}
    for user in user_list:
        usersequence = UserSequences.GetUserSequences(user)
        for i in range(len(usersequence)):
            state = usersequence[i][1]
            if state not in StandSequence.keys():
                StandSequence[state] = 1
            else:
                StandSequence[state] += 1

    f = open('./data/StandeSequence.txt', 'w')
    for key, value in StandSequence.items():
        f.write(key)
        f.write(':')
        value = str(value)
        f.write(value)
        f.write('\n')
        print key, value
    f.close()

    return StandSequence

if __name__  == '__main__':
    user_list = ['CEL0561']
    GetStandeSequence(user_list)
