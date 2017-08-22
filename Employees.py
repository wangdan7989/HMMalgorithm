# coding=utf-8
'''
Created on 2016-12-28

@author: LuDan
'''
from util import MySQLUtil
import csv
import CSVFile



def queryLeaveEmployees():     #统计离职员工
    sql="SELECT employee_id,leave_date,state FROM threat_4_2.threat_basic_employee where service_state=0;"
    db=MySQLUtil.ITDB()
    employees=db.querytl(sql)
    return employees

def queryLeaveTimebyEmployee(employeeid):    #查询离职员工离职时间
    sql="select leave_date from threat_4_2.threat_basic_employee where employee_id='"+employeeid+"';"
    db=MySQLUtil.ITDB()
    leavedate=db.querytl(sql)
    return leavedate
def queryEmployees():
    sql="SELECT employee_id,state FROM threat_4_2.threat_basic_employee;"
    db=MySQLUtil.ITDB()
    employees=db.querytl(sql)
    return employees
def querylastdate_Employees():     #统计全部员工以及他们最后一个行为的时间
    employees = []
    sql="SELECT employee_id ,state FROM threat_4_2.threat_basic_employee;"
    db=MySQLUtil.ITDB()
    employee=db.querytl(sql)
    with open("./data/allusers/employees_lastdate.csv", "wb") as csvsequen:
        spamwriter = csv.writer(csvsequen, dialect='excel')
        for item in employee:
            maxtime = []
            userinfo = []
            user = item[0]
            state = item[1]
            logonsql = "select max(a.date) from threat_4_2.threat_action_logon a where a.user='"+user+"';"
            devicesql = "select max(a.date) from threat_4_2.threat_action_device a where a.user='" + user + "';"
            filesql = "select max(a.date) from threat_4_2.threat_action_file a where a.user='" + user + "';"
            httpsql = "select max(a.date) from threat_4_2.threat_action_http a where a.user='" + user + "';"
            emailsql = "select max(a.date) from threat_4_2.threat_action_email a where a.user='" + user + "';"
            for i in range(5):
                if i==0:
                    sql  = logonsql
                elif i == 1:
                    sql = devicesql
                elif i ==2:
                    sql = filesql
                elif i == 3:
                    sql = httpsql
                else:
                    sql = emailsql
                #print sql
                maxtimeresult = db.querytl(sql)
                #print maxtimeresult[0][0]
                if maxtimeresult[0][0] is None:
                    pass
                else :
                    maxtime.append(maxtimeresult[0][0])
                print maxtime
            userinfo.append(user)
            userinfo.append(max(maxtime))
            userinfo.append(state)
            spamwriter.writerow(userinfo)
        #employees.append(userinfo)
        #print employees





    #return employees
if __name__ =='__main__':
    emplyoees = queryEmployees()
    filename = "./data/allusers/Allusers.csv"
    CSVFile.Writecsvtofile(filename,emplyoees)

