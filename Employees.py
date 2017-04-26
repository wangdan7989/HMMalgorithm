# coding=utf-8
'''
Created on 2016-12-28

@author: LuDan
'''
from util import MySQLUtil



def queryLeaveEmployees():     #统计离职员工
    sql="SELECT employee_id,leave_date,state FROM threat_4_2.threat_basic_employee where service_state=0 limit 10;"
    db=MySQLUtil.ITDB()
    employees=db.querytl(sql)
    return employees

def queryLeaveTimebyEmployee(employeeid):    #查询离职员工离职时间
    sql="select leave_date from threat_4_2.threat_basic_employee where employee_id='"+employeeid+"';"
    db=MySQLUtil.ITDB()
    leavedate=db.querytl(sql)
    return leavedate

