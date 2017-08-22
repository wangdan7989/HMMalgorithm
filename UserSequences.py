# coding=utf-8
'''
Created on 2017-04-9

@author: Wangdan
'''

import SingleSequence
import CSVFile
import Employees
import csv
from dateutil.relativedelta import relativedelta
import datetime
import dateutil.relativedelta

from pylab import *
from matplotlib.ticker import MultipleLocator

def GetUserSequences(employee,start_date,finish_date):
#def GetUserSequences(employee):
    #list=SingleSequence.GetUserSingleSequence(employee,start_date,finish_date)
    list = SingleSequence.GetUserSingleSequence(employee,start_date,finish_date)
    user = employee
    #k=6 #用户一条行为序列的长度
    k=4
    UserSequence = []

    for i in (range(len(list) - k)):
        sequ = ''
        state = ''
        for j in range(k):
            sequ = sequ+list[i+j][1]+'-'
            state = state+str(list[i+j][1])[0:2]

        tem = [sequ, state]
        UserSequence.append(tem)
    filename = './data/allusers/'+user+'UserSequence.csv'
    SingleSequence.Writecsvtofile(filename,UserSequence)

    '''
    with open('./data/allusers/UserSequence.csv', 'wb') as csvsequen:
        spamwriter = csv.writer(csvsequen, dialect='excel')
        for item in UserSequence:
            spamwriter.writerow(item)


    f = open('./data/UserSequence.txt', 'w')
    for i in range(len(UserSequence)):
        f.write(UserSequence[i][0])
        f.write(':')
        f.write(UserSequence[i][1])
        f.write('\n')
        #print UserSequence[i]
    f.close()
    '''
    return UserSequence


def GetStandeSequence(user,start_date,finish_date):
    StandSequence = {}
    '''
    #标准用户画像由多个正常用户一起刻画
    for user in user_list:
        usersequence = GetUserSequences(user,start_date,finish_date)
        for i in range(len(usersequence)):
            state = usersequence[i][1]
            if state not in StandSequence.keys():
                StandSequence[state] = 1
            else:
                StandSequence[state] += 1
    '''

    usersequence = GetUserSequences(user,start_date,finish_date)
    for i in range(len(usersequence)):
        state = usersequence[i][1]
        if state not in StandSequence.keys():
            StandSequence[state] = 1
        else:
            StandSequence[state] += 1

    #统计有多少种状态，以出现次数的多少来决定，value表示出现的次数，状态为value大于某个值的行为
    standefilename = './data/allusers/'+user+'StandeSequence.csv'
    with open(standefilename, 'wb') as csvsequenst:
        spamwriter = csv.writer(csvsequenst, dialect='excel')
        for key, value in StandSequence.items():
            if value > 0:
                spamwriter.writerow([value,key])

    '''
    f = open('./data/StandeSequence.txt', 'w')
    for key, value in StandSequence.items():
        if value > 0:
            value = str(value)
            f.write(value)
            f.write(':')
            f.write(key)
            f.write('\n')
            #print key, value
    f.close()
    '''
    return StandSequence
#if __name__  == '__main__':
    '''
    #user = 'WAB0143'
    user = 'JLM0364'
    #user = ['WAB0143']
    #user_list = ['RSC0089']
    start_date = '2009-12-01'
    finish_date = '2010-11-31'
    GetUserSequences(user,start_date, finish_date)
    #GetStandeSequence(user, start_date, finish_date)
    '''
#k为连续序列的长度，middletime以前的是训练数据，以后的是测试数据，训练数据和测试数据均是一个序列的csv，
def Gettraintestdata(sequenlen):
    k=sequenlen
    #k = 4
    employees = Employees.queryEmployees()
    count = 0
    result = []
    count = 0
    validusers = []
    invalidusers = []
    for item in employees:
        user = item[0]
        singleFile = "./data/allusers/SingleSequence/"+user+".csv"
        list = CSVFile.loadCSVfile1(singleFile)
        maxtime= list[-1][0]
        mintime = list[0][0]
        maxtime = datetime.datetime.strptime(maxtime,'%Y %j %H:%M:%S')
        mintime = datetime.datetime.strptime(mintime, '%Y %j %H:%M:%S')
        middletime = maxtime-relativedelta(months=2)


        if mintime > (middletime- relativedelta(months = 3)):
            invalidusers.append(user)
            continue
            #if mintime > (maxtime - relativedelta(months = 1)):
             #   middletime  = mintime+relativedelta(days =20)
            #else:
             #   middletime = mintime + relativedelta(months=1)


        TrainUserSequence = []
        TestUserSequence = []
        for i in (range(len(list) - k)):
            sequ = ''
            state = ''
            time = datetime.datetime.strptime(list[i][0],'%Y %j %H:%M:%S')

            if time<middletime:
                for j in range(k):
                    sequ = sequ + list[i + j][1] + '-'
                    state = state + str(list[i + j][1])[0:2]
                tem = [sequ, state]
                TrainUserSequence.append(tem)
                print "time<middletime",time<middletime,"TrainUserSequence"
            if time >= middletime:
                for j in range(k):
                    sequ = sequ + list[i + j][1] + '-'
                    state = state + str(list[i + j][1])[0:2]
                tem = [sequ, state]
                TestUserSequence.append(tem)
                print "time>middletime", time >= middletime, "TestUserSequence"
        #validusers.append(user)
        print count, user
        count = count + 1
        trainFile = "./data/allusers/Train/"+user+".csv"
        testFile = "./data/allusers/Test/" + user + ".csv"
        CSVFile.Writecsvtofile(trainFile,TrainUserSequence)
        CSVFile.Writecsvtofile(testFile, TestUserSequence)

    allusers = CSVFile.loadCSVfile1("./data/allusers/Allusers_state.csv")
    resultlist = []
    for invalid in invalidusers:
        for i in range(len(allusers)):
            if invalid == allusers[i][0]:
                del(allusers[i])
                break

    CSVFile.Writecsvtofile("./data/allusers/validusers.csv", allusers)

#得到从starttime 到finishtime的用户单行为序列
def GetperiodSequence(employee,starttime,finishtime):
    user = employee
    singleFile = "./data/allusers/SingleSequence/" + user + ".csv"
    sequences=[]
    list = CSVFile.loadCSVfile1(singleFile)
    for i in range(len(list)):
        currenttime = datetime.datetime.strptime(list[i][0], '%Y %j %H:%M:%S').date()
        #print currenttime
        if starttime<= currenttime and currenttime<finishtime:
            #print "currenttime:",currenttime
            sequences.append(list[i][1])
    return sequences

#得到用户最后行为时间的60天以前的单序列作为训练数据，后60天的行为作为测试数据，训练数据写入csv文件。返回测试数据的list
def GettraintestdataV2(employee):
    user = employee
    singleFile = "./data/allusers/SingleSequence/" + user + ".csv"
    list = CSVFile.loadCSVfile1(singleFile)
    maxtime = list[-1][0]
    mintime = list[0][0]
    maxtime = datetime.datetime.strptime(maxtime, '%Y %j %H:%M:%S').date()
    mintime = datetime.datetime.strptime(mintime, '%Y %j %H:%M:%S').date()
    middletime = maxtime - relativedelta(days=60)

    if mintime > (middletime - relativedelta(days=90)):
        return 0

    TrainUserSequence = []
    TestUserSequence = []
    for i in (range(len(list))):
        time = datetime.datetime.strptime(list[i][0], '%Y %j %H:%M:%S').date()
        if time < middletime:
            TrainUserSequence.append([list[i][1]])
            #print "time<middletime", time < middletime, "TrainUserSequence"

    currenttime = middletime
    while(currenttime<maxtime):
        finishtime = currenttime+relativedelta(days=1)
        daysequenc = GetperiodSequence(user,currenttime,finishtime)
        if len(daysequenc)>1:
            TestUserSequence.append(daysequenc)
        currenttime = finishtime

    trainFile = "./data/allusers/Train/" + user + ".csv"
    CSVFile.Writecsvtofile(trainFile, TrainUserSequence)
    print TestUserSequence
    print "TestUserSequence",len(TestUserSequence)
    return TestUserSequence



if __name__  == '__main__':
    GettraintestdataV2('WAB0143')