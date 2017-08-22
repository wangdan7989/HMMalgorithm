# coding=utf-8
'''
Created on 2017-04-9

@author: Wangan
'''
from util import MySQLUtil
import datetime
import csv
import Employees

def Writecsvtofile(filename,list):
    with open(filename, 'wb') as csvsequen:
        spamwriter = csv.writer(csvsequen, dialect='excel')
        for item in list:
            spamwriter.writerow(item)
    '''
    csvsequen = open(filename,'wb')
    spamwriter = csv.writer(csvsequen, dialect='excel')
    for item in list:
        spamwriter.writerow(item)
    csvsequen.close()
    '''
def GetUserSingleSequence(employee,start_date,finish_date):
#def GetUserSingleSequence(employee):
    db = MySQLUtil.ITDB()
    #user='CEL0561'
    k=5  #用户一条行为序列的长度
    user = employee
    Squencedevice= {}
    Squencelogon = {}
    Squencefile = {}
    Squenceemail = {}
    Squencehttp = {}

    #统计对象为离职员工

    sql_device = "SELECT user,activity,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_device a where a.user='" + user + "' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_logon = "SELECT user,activity,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_logon a where a.user='"+user+"' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_file = "SELECT user,filename,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_file a where a.user='"+user+"' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_email = "SELECT user,to_user,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_email a where a.user='" + user + "' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    sql_http = "SELECT user,url,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_http a where a.user='" + user + "' and date >'"+start_date+"' and date <'"+finish_date+"' ;"
    '''
    sql_device = "SELECT user,activity,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_device a where a.user='" + user +"' ;"
    sql_logon = "SELECT user,activity,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_logon a where a.user='" + user +"' ;"
    sql_file = "SELECT user,filename,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_file a where a.user='" + user + "' ;"
    sql_email = "SELECT user,to_user,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_email a where a.user='" + user +"' ;"
    sql_http = "SELECT user,url,date_format(date,'%Y %j %T') as b FROM threat_4_2.threat_action_http a where a.user='" + user + "' ;"
    '''
    action=''
    count = 0
    for i in (range(5)):
        if i == 0:
            sql = sql_device
        elif i == 1:
            sql = sql_logon
        elif i == 2:
            sql = sql_file
        elif i == 3:
            sql = sql_http
        elif i == 4:
            sql = sql_email

        #print i, sql

        result = db.querytl(sql)
        #print result
        Squence = {}
        for j in (range(len(result))):
            count = count +1
            #print result[j][2]
            time = int(result[j][2][8:11])
            #print time
            #if count ==9:print sql

            if i == 3:
                if time >= 0 and time < 6:
                    Squence[result[j][2]] = 'AUrl'
                elif time >= 6 and time < 12:
                    Squence[result[j][2]] = 'BUrl'
                elif time >= 12 and time < 18:
                    Squence[result[j][2]] = 'CUrl'
                elif time >= 18:
                    Squence[result[j][2]] = 'DUrl'
                else:
                    print "**************time:",time
            elif i == 4:
                if time >= 0 and time < 6:
                    Squence[result[j][2]] = 'ASendEmail'
                elif time >= 6 and time < 12:
                    Squence[result[j][2]] = 'BSendEmail'
                elif time >= 12 and time < 18:
                    Squence[result[j][2]] = 'CSendEmail'
                elif time >= 18:
                    Squence[result[j][2]] = 'DSendEmail'
                else:
                    print "**************time:", time
            elif i == 2:
                if time >= 0 and time < 6:
                    Squence[result[j][2]] = 'AFileCopy'
                elif time >= 6 and time < 12:
                    Squence[result[j][2]] = 'BFileCopy'
                elif time >= 12 and time < 18:
                    Squence[result[j][2]] = 'CFileCopy'
                elif time >= 18:
                    Squence[result[j][2]] = 'DFileCopy'
                else:
                    print "**************time:", time
            elif i == 1:
                if(result[j][1]=='Logoff'):
                    if time >= 0 and time < 6:
                        Squence[result[j][2]] = 'ANologon'
                    elif time >= 6 and time < 12:
                        Squence[result[j][2]] = 'BNologon'
                    elif time >= 12 and time < 18:
                        Squence[result[j][2]] = 'CNologon'
                    elif time >= 18:
                        Squence[result[j][2]] = 'DNologon'
                    else:
                        print "**************time:", time
                else:
                    if time >= 0 and time < 6:
                        Squence[result[j][2]] = 'Alogon'
                    elif time >= 6 and time < 12:
                        Squence[result[j][2]] = 'Blogon'
                    elif time >= 12 and time < 18:
                        Squence[result[j][2]] = 'Clogon'
                    elif time >= 18:
                        Squence[result[j][2]] = 'Dlogon'
                    else:
                        print "**************time:", time
            elif i == 0:
                if (result[j][1] == 'Connect'):
                    if time >= 0 and time < 6:
                        Squence[result[j][2]] = 'AConnect'
                    elif time >= 6 and time < 12:
                        Squence[result[j][2]] = 'BConnect'
                    elif time >= 12 and time < 18:
                        Squence[result[j][2]] = 'CConnect'
                    elif time >= 18:
                        Squence[result[j][2]] = 'DConnect'
                    else:
                        print "**************time:", time
                else:
                    if time >= 0 and time < 6:
                        Squence[result[j][2]] = 'ADisconnect'
                    elif time >= 6 and time < 12:
                        Squence[result[j][2]] = 'BDisconnect'
                    elif time >= 12 and time < 18:
                        Squence[result[j][2]] = 'CDisconnect'
                    elif time >= 18:
                        Squence[result[j][2]] = 'DDisconnect'
                    else:
                        print "**************time:", time
            else:
                print "ERROR"
            #print 'count:',count,'len squence:',len(Squence)
        print 'action:',i,'count:',count,'len sequence:',len(Squence),'len result:',len(result)
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

    #print "squencemerge:",SquenceMerge
    print "count:",count,"squencemerge:",len(SquenceMerge)
    list=sorted(SquenceMerge.items(),key=lambda item:item[0])
    #print "list:",list
    j = 0
    #print len(list)
    if len(list) > 0:
        while True:
            if (list[j][1] == 'AUrl' and list[j + 1][1] == 'AUrl') or (list[j][1] == 'BUrl' and list[j + 1][1] == 'BUrl') or (list[j][1] == 'CUrl' and list[j + 1][1] == 'CUrl') or (list[j][1] == 'DUrl' and list[j + 1][1] == 'DUrl'):
              del list[j + 1]
              count = count -1
            else:
                j = j+1

            if j >= len(list) - 2:
                break
        #print len(list),'****',i

    #filename = './data/allusers/SingleSequence/'+user+'.csv'
    filename = './data/allusers/'+user+'SingleSequence.csv'
    Writecsvtofile(filename,list)
    #print file

    print "count:",count
    print "list len:",len(list)

    '''
    f=open('./data/SingleSequence.txt','w')
    for i in range(len(list)):
        f.write(list[i][0])
        f.write(':')
        f.write(list[i][1])
        f.write('\n')
        #print list[i]
    f.close()
    '''
    return list


if __name__ == '__main__':

    employees = Employees.queryEmployees()
    ii = 0
    for item in employees:
        employee = item[0]
        ii = ii+1
        print "*******************************"
        print ii,':',employee
        GetUserSingleSequence(employee)
