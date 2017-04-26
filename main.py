# -*- coding: utf-8 -*-

import preProcess
from HMM import *
from dateutil.relativedelta import relativedelta
import Employees

def average(list):
    return sum(list) / len(list)
if __name__ == '__main__':
    start_date = '2009-12-01'
    employees = Employees.queryLeaveEmployees()
    f = open('./data/Result.txt', 'w')
    for user in employees:
        end_date = user[1] + relativedelta(days=1)
        middle_date = end_date - relativedelta(months=2)
        user = str(user[0])
        middle_date = str(middle_date)
        end_date = str(end_date)

        UserSequences.GetStandeSequence(user, start_date, middle_date)
        preProcess.GetTransiMatrix()
        usersequence = UserSequences.GetUserSequences(user, middle_date, end_date)

        H = HMM()
        import time
        t1 = time.time()
        result = H.hmm(usersequence)
        t2 = time.time()

        print average(result)
        prosqu = average(result)

        f.write(user[0],': ',prosqu,'',user[2],'\n')

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
