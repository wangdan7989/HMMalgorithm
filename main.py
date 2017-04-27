# -*- coding: utf-8 -*-

import preProcess
from HMM import *
from dateutil.relativedelta import relativedelta
import Employees
import time

def average(list):
    return sum(list) / len(list)

if __name__ == '__main__':

    t1 = time.time()
    start_date = '2009-12-01'
    employees = Employees.queryLeaveEmployees()
    f = open('./data/Result.txt', 'w')
    for user in employees:
        #print user
        end_date = user[1] + relativedelta(days=1)
        middle_date = end_date - relativedelta(months=2)
        employee = str(user[0])
        middle_date = str(middle_date)
        end_date = str(end_date)

        if len(UserSequences.GetStandeSequence(employee, start_date, middle_date)) < 1:
            continue

        preProcess.GetTransiMatrix()
        usersequence = UserSequences.GetUserSequences(employee, middle_date, end_date)

        H = HMM()

        result = H.hmm(usersequence)
        print employee,average(result),user[2]
        prosqu = str(average(result))

        f.write(user[0])
        f.write(': ')
        f.write(prosqu)
        f.write(': ')
        f.write(str(user[2]))
        f.write('\n')

    t2 = time.time()
    #print t2-t1
    f.close()

    '''
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
