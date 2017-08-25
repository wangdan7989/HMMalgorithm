# -*- coding: utf-8 -*-
'''
<<<<<<< HEAD:main.py
得到用户最红概率序列的平均值
=======
Created on 2017-04-25

@author: Wangan

说明
得到用户的状态转移概率
'''
#>>>>>>> 34c6dfe6197febd37f54b0a34e607135f3d0d8e2:GetHMMresult.py


import preProcess
from HMM import *
from dateutil.relativedelta import relativedelta
import Employees
import time
import csv
import CSVFile
import UserSequences
import numpy
import math

#算协方差
def GetCov(nlist):
    covnum = cov(nlist)
    return covnum

#算均值
def average(list):
    return sum(list) / len(list)

#算方差
def GetVar(nlist):
    n = sum(nlist)
    mean = average(nlist)
    summ = 0
    for i in range(len(nlist)):
        tem = (nlist[i]-mean)**2
        summ = summ +tem
    var = float(summ)/float(n)
    return var

#<<<<<<< HEAD:main.py
def GetResult():
    k=4
    UserSequences.Gettraintestdata(k)
    #employees = Employees.queryEmployees()
    employees = CSVFile.loadCSVfile1("./data/allusers/validusers.csv")
    #employees = CSVFile.loadCSVfile1("./data/allusers/Allusers_state.csv")
    resultlist = []
    avgresult = []

    for item in employees:
        user = item[0]
        state = item[1]
        preProcess.GetTransiMatrix(user)

        H = HMM(user)
        result = H.hmm(user)
        print user, result

        #resultlist.append([user,result])
        avgresultpro = average(result)
        avgresult.append([user,avgresultpro,state])

        print "average:",average(result), state
        result.insert(0, user)
        resultlist.append(result)
#=======
    t1 = time.time()
    start_date = '2009-12-01'
    employees = Employees.queryLeaveEmployees()
    #f = open('./data/Result.txt', 'w')
    f = open('./data/ProSquenceResult.txt', 'w')
    #for user in employees:
#>>>>>>> 34c6dfe6197febd37f54b0a34e607135f3d0d8e2:GetHMMresult.py
        #print user
    resultfile = './data/allusers/'+k+'ResultPro974.csv'
    avgresultfile = './data/allusers/'+k+'AvgResultPro974.csv'
    CSVFile.Writecsvtofile(resultfile,resultlist)
    CSVFile.Writecsvtofile(avgresultfile,avgresult)



def plotresult():
    avgresult = CSVFile.loadCSVfile1('./data/allusers/AvgResultPro974.csv')
    resultpro = CSVFile.loadCSVfile1('./data/allusers/ResultPro974.csv')
    normalavg =[]
    abnormalavg = []
    normalcov =[]
    abnormalcov = []

    for item in avgresult:
        state = int(item[2])
        #print state
        prestate = float(item[1])
        #print prestate
        if state == 0:
            normalavg.append(prestate)
        if state == 1:
            abnormalavg.append(prestate)

    list.sort(normalavg)
    list.sort(abnormalavg)

    for item in resultpro:

        state = int(item[1])
        prolist = []
        for number in item[2:]:
            if len(number)>0:
                prolist.append(float(number))
                #print float(number)
        prestate = float(cov(prolist))
        print prestate
        if state == 0:
            normalcov.append(prestate)
        if state == 1:
            abnormalcov.append(prestate)


#<<<<<<< HEAD:main.py
    print normalcov
    print abnormalcov
#=======
 #       result = H.hmm(usersequence)
  #      print employee,average(result),user[2]
  #      prosqu = str(result)
#>>>>>>> 34c6dfe6197febd37f54b0a34e607135f3d0d8e2:GetHMMresult.py

    list.sort(normalcov)
    list.sort(abnormalcov)


    plt.figure()
    x1 = range(len(normalcov))
    x2 = range(len(abnormalcov))
    #y = result[:1000]
    #x = [0,1]
    plt.ylim(0, 0.3)
    # print x
    # y=[0.1,0.2,0.3,0.4,0.5]
    plt.plot(x2,abnormalcov,'r')
    plt.plot(x1, normalcov, 'b')
    # plt.plot(x, result)
    #plt.legend()
    plt.show()

    '''

    t1 = time.time()
    start_date = '2009-12-01'
    #employees = Employees.queryLeaveEmployees()
    employees = Employees.querylastdate_Employees()
    filenameresult = './data/allusers/ResultPro.csv'
    filenameavgresult = './data/allusers/AvgResultPro.csv'
    with open(filenameresult, 'wb') as csvresult:
        Resspamwriter = csv.writer(csvresult, dialect='excel')
        with open(filenameavgresult, 'wb') as csvavg:
            Avgspamwriter = csv.writer(csvavg, dialect='excel')

            for user in employees:
                #print user
                end_date = user[1] + relativedelta(days=1)
                middle_date = end_date - relativedelta(months=2)
                employee = str(user[0])
                middle_date = str(middle_date)
                end_date = str(end_date)

                if len(UserSequences.GetStandeSequence(employee, start_date, middle_date)) < 1:
                    continue

                preProcess.GetTransiMatrix(employee)
                usersequence = UserSequences.GetUserSequences(employee, middle_date, end_date)

                H = HMM(employee)

                result = H.hmm(usersequence)
                print employee,average(result),user[2]
                Resspamwriter([user[0], result])
                prosqu = str(average(result))
                Avgspamwriter([user[0],prosqu],user[2])

        t2 = time.time()


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
    plt.show() '''
#根据MM得到每个用户60天的概率
def GetUserpro():
    employees = CSVFile.loadCSVfile1("./data/allusers/validusers.csv")
    userpro=[]
    for item in employees:
        proresult =[]
        user = item[0]
        state = item[1]
        testsequence = UserSequences.GettraintestdataV2(user)
        if testsequence==0:
            continue
        proresult.append(user)
        proresult.append(state)
        preProcess.GetTransiMatrixV2(user)
        H = HMM(user)
        for sequence in testsequence:
            result = H.hmmV2(sequence)
            proresult.append(result)

        userpro.append(proresult)

    filename= "./data/allusers/userpro.csv"
    CSVFile.Writecsvtofile(filename,userpro)
    print userpro

#画list的ROC曲线，list必须是第一列是user，第二列是state，第三列是需要阈值划分的值
def PloROC(list,r,times):

    TPR = []
    FPR = []
    thr = 0

    for i in range(times):
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        for item in list:
            state = int(item[1])
            # print state
            prestate = float(item[2])
            # print prestate

            if state == 0:
                if prestate > thr:
                    fp = fp + 1
                else:
                    tn = tn + 1
            if state == 1:
                if prestate > thr:
                    tp = tp + 1
                else:
                    fn = fn + 1

            if (tp + fn) == 0 or (fp + tn) == 0:
                continue
        tpr = float(tp) / (float(tp) + float(fn))
        fpr = float(fp) / (float(fp) + float(tn))
        print tpr, fpr
        TPR.append(tpr)
        FPR.append(fpr)
        thr = i*r


    plt.figure()
    plt.plot(FPR, TPR, 'r')
    x = [0, 1]
    y = x
    plt.plot(x, y, 'b')
    plt.show()


def GetuserproROC():
    '''
    userpro = CSVFile.loadCSVfile1("./data/allusers/userpro.csv")
    weekpro = []
    zeronumber = 0
    for item in userpro:
        user = item[0]
        state = item[1]
        pro =0.0
        productpro = 1.0
        userinfo = []

        for i in range(8):
            if i ==1 or i==0 or len(item[i])<1:
                continue
            pro = float(item[i])
            if (pro<=0):

                zeronumber  = zeronumber+1
                print "*******************************************************************************Error!!"
                continue
            print "pro:",pro
            productpro = (-math.log(pro))*productpro
            print "productpro:",productpro

        userinfo .append(user)
        userinfo.append(state)
        userinfo.append(productpro)
        weekpro.append(userinfo)
    print "zeronumber:",zeronumber
    print weekpro
    CSVFile.Writecsvtofile("./data/allusers/weekpro.csv",weekpro)
    normalavg = []
    abnormalavg = []
    '''
    weekpro = CSVFile.loadCSVfile1("./data/allusers/weekpro.csv")
    TPR = []
    FPR = []
    thr=0
    a =0
    b =1
    for i in range(11000):
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        for item in weekpro:
            state = int(item[1])
            # print state
            prestate = float(item[2])
            # print prestate

            if state == 0:
                #normalavg.append(prestate)
                if prestate>thr:
                    fp = fp +1
                else:
                    tn = tn+1
            if state == 1:
                #abnormalavg.append(prestate)
                if prestate>thr:
                    tp = tp+1
                else:
                    fn = fn+1

            if (tp+fn)==0 or (fp+tn)==0:
                continue
            tpr = float(tp)/(float(tp)+float(fn))
            fpr = float(fp)/(float(fp)+float(tn))
            print tpr,fpr
        TPR.append(tpr)
        FPR.append(fpr)
        if i<100:
            thr = i
        if i>=100 and i<=10000:
            thr = i*100
        if i>10000:
            thr = i*1000
        #thr=i*100



    '''
    p = float(tp)/(float(tp)+float(fp))
    frp = float(fp)/(float(fp)+float(tn))
    r = float(tp)/(float(tp)+float(fn))
    print"tp:",tp,"fp:",fp,"tn:",tn,"fn:",fn
    print "p:",p,"frp:",frp,"r:",r
    '''
    #list.sort(normalavg)
    #list.sort(abnormalavg)

    plt.figure()
    plt.plot(FPR, TPR, 'r')
    x=[0,1]
    y=x
    plt.plot(x,y,'r')
    plt.show()

if __name__ == '__main__':
    #userpro = CSVFile.loadCSVfile1("./data/allusers/ResultPro974.csv")
    userpro = CSVFile.loadCSVfile1("./data/allusers/userpro1.csv")
    userinfo = []
    for item in userpro:
        user = item[0]
        state = item[1]
        #print state
        sumpro =[]
        for pro in item[2:42]:
            if len(pro)>0 and float(pro)>0:
                #print pro
                pro = -math.log(float(pro))
                sumpro.append(pro)
        avgpro = sum(sumpro)/len(sumpro)
        #avgpro = GetVar(sumpro)
        avgpro = GetCov(sumpro)
        #userinfo.append([user,state,avgpro])
    #CSVFile.Writecsvtofile("./data/allusers/40daysdayavg.csv",userinfo)


    print userinfo
    #PloROC(userinfo,0.01,4000)#weekdayvar
    PloROC(userinfo, 0.1, 500)  # 40daysavg
    #nlist = [1,2,3,4,5,3,4,5,6]
    #print GetVar(nlist)