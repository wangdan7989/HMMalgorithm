# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''
from util import MySQLUtil
import datetime


def GetUserSingleSequence(employee,start_date,finish_date):
    db = MySQLUtil.ITDB()
    #user='CEL0561'
    k=5  #用户一条行为序列的长度
    user = employee
    Squencedevice= {}
    Squencelogon = {}
    Squencefile = {}
    Squenceemail = {}
    Squencehttp = {}

    sql_device = "SELECT user,activity,date_format(date,'%j %T') as a FROM threat_4_2.threat_action_device a where a.user='" + user + "' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_logon = "SELECT user,activity,date_format(date,'%j %T') as a FROM threat_4_2.threat_action_logon a where a.user='"+user+"' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_file = "SELECT user,filename,date_format(date,'%j %T') as a FROM threat_4_2.threat_action_file a where a.user='"+user+"' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_email = "SELECT user,to_user,date_format(date,'%j %T') as a FROM threat_4_2.threat_action_email a where a.user='" + user + "' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_http = "SELECT user,url,date_format(date,'%j %T') as a FROM threat_4_2.threat_action_http a where a.user='" + user + "' and date >'"+start_date+"' and date <'"+finish_date+"' ;"

    action=''
    for i in (range(5)):
        if i==0:
            sql=sql_device
        elif i==1:
            sql = sql_logon
        elif i==2:
            sql = sql_file
        elif i == 3:
            sql = sql_http
        elif i == 4:
            sql = sql_email

        #print i, sql
        result = db.querytl(sql)
        Squence = {}
        for j in (range(len(result))):
            if i==3:
                Squence[result[j][2]] = 'Url'
            elif i==4:
                Squence[result[j][2]] = 'SendEmail'
            elif i==2:
                Squence[result[j][2]] = 'FileCopy'
            elif i==1:
                if(result[j][1]=='Logoff'):
                    Squence[result[j][2]] = 'Nologon'
            else:
                Squence[result[j][2]] = result[j][1]

        #print Squence
        if i==0:
            Squencedevice=Squence
        elif i==1:
            Squencelogon=Squence
        elif i==2:
            Squencefile=Squence
        elif i == 3:
            Squencehttp=Squence
        elif i == 4:
            Squenceemail = Squence

    SquenceMerge = Squencelogon.copy()
    SquenceMerge.update(Squencedevice)
    SquenceMerge.update(Squencefile)
    SquenceMerge.update(Squencehttp)
    SquenceMerge.update(Squenceemail)


    list=sorted(SquenceMerge.items(),key=lambda item:item[0])

    i = 0
    #print len(list)
    if len(list) > 0:
        while True:
            if list[i][1] == 'Url' and list[i + 1][1] == 'Url':
              del list[i + 1]
            else:
                i = i+1

            if i >= len(list) - 2:
                break
        #print len(list),'****',i


    f=open('./data/SingleSequence.txt','w')

    for i in range(len(list)):
        f.write(list[i][0])
        f.write(':')
        f.write(list[i][1])
        f.write('\n')
        #print list[i]
    f.close()

    return list


if __name__ == '__main__':
    GetUserSingleSequence('MAR0955','2009-12-01','2011-01-31')
