# -*- coding: utf-8 -*-
import GetHMMresult
import CSVFile
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

#归一化
def  Normalization(nlist):
    nlist = [float(i) for i in nlist]
    sumn = sum(nlist)
    newlist = []
    for item in nlist:
        tem = float(item)/sumn
        newlist.append(tem)
    return newlist

def GetweekconnectUser():
    connectuser = CSVFile.loadCSVfile1('./data/deviceConnect.csv')
    #weekuser = CSVFile.loadCSVfile1('./data/allusers/weekdayvar.csv')
    #weekuser = CSVFile.loadCSVfile1('./data/allusers/weekpro.csv')
    weekuser = CSVFile.loadCSVfile1('./data/allusers/MM_week_result.csv')

    userinfo = []
    for citem in connectuser:
            cuser = citem[0]
            for witem in weekuser:
                wuser = witem[0]
                if cuser != wuser:
                    continue
                userinfo.append(witem)
    print len(userinfo)
    print userinfo
    #CSVFile.Writecsvtofile('./data/allusers/MM_connect_week.csv',userinfo)

    FTPR = []
    TPR = []
    FPR = []
    thr = 0
    a = 0
    b = 1
    userinfo = weekuser
    for i in range(6000):
    #for i in range(15000):
        tp = 0
        fp = 0
        tn = 0
        fn = 0
        for item in userinfo:
            state = int(item[1])
            # print state
            prestate = float(item[2])
            # print prestate

            if state == 0:
                # normalavg.append(prestate)
                if prestate > thr:
                    tn = tn + 1
                    #fp = fp + 1

                else:
                    fp = fp + 1
                    #tn = tn + 1
            if state == 1:
                # abnormalavg.append(prestate)
                if prestate > thr:
                    fn = fn + 1
                    #tp = tp + 1
                else:
                    tp = tp + 1
                    #fn = fn + 1
        if (tp + fn) == 0 or (fp + tn) == 0:
            thr = thr + 0.1
            continue
        tpr = float(tp) / (float(tp) + float(fn))
        fpr = float(fp) / (float(fp) + float(tn))
        print fpr,tpr

        TPR.append(tpr)
        FPR.append(fpr)
        thr = thr+0.1
        '''
        if i<10:
            i = 0.1*i
        if i < 100 and i>10:
            thr = i
        if i >= 100 and i <= 10000:
            thr = i * 100
        if i > 10000  and i<40000:
            thr = i * 1000
            # thr=i*100
        if i > 40000:
            thr = i * 100000
        '''

    '''
    p = float(tp)/(float(tp)+float(fp))
    frp = float(fp)/(float(fp)+float(tn))
    r = float(tp)/(float(tp)+float(fn))
    print"tp:",tp,"fp:",fp,"tn:",tn,"fn:",fn
    print "p:",p,"frp:",frp,"r:",r
    '''
    # list.sort(normalavg)
    # list.sort(abnormalavg)
    #CSVFile.Writecsvtofile('./data/allusers/weekconnetproFT.CSV',)
    data = pd.DataFrame({'FPR':TPR,
                         'TPR':FPR})
    data.to_csv('./data/allusers/result/ROC_data/MM_weekconnectpro.csv')

    plt.figure()
    plt.plot(TPR, FPR, 'r')
    x = [0, 1]
    y = x
    plt.plot(x, y, 'b')
    plt.show()
    #GetHMMresult.PloROC(userinfo,100,10000)
    #CSVFile.Writecsvtofile('./data/allusers/weekconnetpro.csv',userinfo)
#GetweekconnectUser()

def GetiForest_MM_scores():
    iforestdata = CSVFile.loadCSVfile1('./data/allusers/iForestdata/outallfeatures.csv')
    mmdata = CSVFile.loadCSVfile1('./data/allusers/weekdayavg.csv')
    userinfo = []
    users = []
    states = []
    iscores = []
    mscores = []

    for fitem in iforestdata:
        fuser = fitem[0]
        for mitem in mmdata:
            muser = mitem[0]
            if fuser !=muser:
                continue
            tem = float(fitem[3])+0.3
            users.append(muser)
            states.append(mitem[1])
            mscores.append(mitem[2])
            iscores.append(tem)
            #score = -math.log(tem)
            #print score
            userinfo.append([muser,mitem[1],mitem[2],tem])
    #CSVFile.Writecsvtofile('./data/allusers/iForestdata/iforest_mmweekdayavg_data.csv',userinfo)
    print userinfo
    mscores = Normalization(mscores)
    iscores = Normalization(iscores)
    data = {}
    print users
    data = pd.DataFrame()
    data['users'] = users
    data['states'] = states
    data['mscores'] = mscores
    data['iscores'] = iscores
    print data

    print data.values
    data.to_csv('./data/allusers/iForestdata/iforest_mmweekdayavg_normalizedata.csv',index=False)

#GetiForest_MM_scores()
def GetFusioniForest_MM():
    data = pd.read_csv('./data/allusers/iForestdata/iforest_mmweekdayavg_normalizedata.csv',index_col='users')
    w1 = 0


    for i in range(11):
        w2 = 1 - w1
        newscores = []
        for item in data.values:
            newscore = float(item[1])*w1 + float(item[2])*w2
            #print item[2]
            #print newscore
            newscores.append(newscore)
        w1 = w1+0.1
        newclum = 'newscore'+str(i)
        print newclum
        data[newclum] = newscores
    print data
    data.to_csv('./data/allusers/iForestdata/iforest_mmweekdayavg_normalize_newscaores_data.csv',index_col='users')

def GetnewscoresROC_XY():
    data = pd.read_csv('./data/allusers/iForestdata/iforest_mmweekdayavg_normalize_newscaores_data.csv', index_col='users')
    states = data['states']
    rocXY = pd.DataFrame
    plt.figure()
    for i in range(11):
        tem = 'newscore'+str(i)
        newscores = data[tem]
        TPR = []
        FPR = []
        thr = 0
        r=0.0001
        for k in range(11000):
            tp = 0
            fp = 0
            tn = 0
            fn = 0
            for j in range(len(states)):
                state = states[j]
                prestate = newscores[j]
                if state == 0:
                    if prestate < thr:
                        fp = fp + 1
                    else:
                        tn = tn + 1
                if state == 1:
                    if prestate < thr:
                        tp = tp + 1
                    else:
                        fn = fn + 1

                if (tp + fn) == 0 or (fp + tn) == 0:
                    continue
            tpr = float(tp) / (float(tp) + float(fn))
            fpr = float(fp) / (float(fp) + float(tn))
            #print tpr, fpr
            TPR.append(tpr)
            FPR.append(fpr)
            thr = thr+ r


        plt.plot(FPR, TPR, 'r')

        x = [0, 1]
        y = x
        plt.plot(x, y, 'b')
        mmroc = pd.read_csv('./data/allusers/result/ROC_data/weekdayconnectavg.CSV',index_col='id')
        mx = mmroc['FPR']
        my = mmroc['TPR']
        plt.plot(mx, my, 'c')
        iforoc = pd.read_csv('./data/allusers/iForestdata/pcarocXY.CSV',index_col='id')
        ix = iforoc['FPR']
        iy = iforoc['TPR']
        plt.plot(ix, iy, 'y')
        plt.show()

def GetMMweekdayacv_PR_XY():
    weekpro = CSVFile.loadCSVfile1('./data/allusers/connect_weekdayvar.csv')
    TPR = []
    FPR = []
    TRP = []
    RECALL = []
    thr = 0
    trp = 0
    recall = 0
    r = 0.001
    for i in range(9000):
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
                # normalavg.append(prestate)
                if prestate < thr:
                    fp = fp + 1
                else:
                    tn = tn + 1
            if state == 1:
                # abnormalavg.append(prestate)
                if prestate < thr:
                    tp = tp + 1
                else:
                    fn = fn + 1

        #if (tp + fn) == 0 or (fp + tn) == 0:
        if (tp + fp) == 0 or (fp + tn) == 0:
            if i < 4000:
                thr = thr + r
            if i >= 4000:
                thr = thr + 0.01
            print "*******************"
            continue
        #tpr = float(tp) / (float(tp) + float(fn))
        #fpr = float(fp) / (float(fp) + float(tn))
        trp = float(tp) / (float(tp) + float(fp))
        recall = float(tp) / (float(tp) + float(fn))
        #print "trp:",trp,"recall:",recall
        #print tpr, fpr
        #TPR.append(tpr)
        #FPR.append(fpr)
        TRP.append(trp)
        RECALL.append(recall)

        if i < 4000:
            thr = thr + r
        if i >= 4000:
            thr = thr+0.01

    data = pd.DataFrame()
    data['RECALL'] = RECALL
    data['TRP'] =TRP
    data.to_csv('./data/allusers/result/PR_data/connectweekday_avg_pr.csv')
    plt.figure()
    #plt.plot(FPR, TPR, 'r')
    plt.plot(RECALL, TRP, 'r')
    x = [0, 1]
    y = [1,0]
    plt.plot(x, y, 'b')
    plt.show()

def GetnewscoresPR_XY():
    data = pd.read_csv('./data/allusers/iForestdata/iforest_mmweekdayavg_normalize_newscaores_data.csv', index_col='users')
    states = data['states']
    rocXY = pd.DataFrame
    plt.figure()
    for i in range(11):
        data1 = pd.DataFrame()
        tem = 'newscore'+str(i)
        newscores = data[tem]
        TPR = []
        FPR = []
        TRP = []
        RECALL = []
        thr = 0
        trp = 0
        thr = 0
        thred = []
        r=0.0001
        for k in range(11000):
            tp = 0
            fp = 0
            tn = 0
            fn = 0
            for j in range(len(states)):
                state = states[j]
                prestate = newscores[j]
                if state == 0:
                    if prestate < thr:
                        fp = fp + 1
                    else:
                        tn = tn + 1
                if state == 1:
                    if prestate < thr:
                        tp = tp + 1
                    else:
                        fn = fn + 1

            #if (tp + fn) == 0 or (fp + tn) == 0:
            if (tp + fn) == 0 or (fp + tp) == 0:
                thr = thr + r
                continue
            #tpr = float(tp) / (float(tp) + float(fn))
            #fpr = float(fp) / (float(fp) + float(tn))

            recall = float(tp) / (float(tp) + float(fn))
            trp = float(tp) / (float(tp) + float(fp))
            #print tpr, fpr
            #TPR.append(tpr)
            #FPR.append(fpr)
            TRP.append(trp)
            RECALL.append(recall)
            thred.append(thr)
            thr = thr+ r

        print i
        data1['threshold'] = thred
        data1['percision'] = TRP
        data1['recall'] = RECALL
        filename = './data/allusers/iForestdata/Different_weight_precision/'+str(i)+'.csv'
        data1.to_csv(filename)
        '''
        #plt.plot(FPR, TPR, 'r')
        plt.plot(RECALL, TRP, 'r')
        x = [0, 1]
        y = [1, 0]
        plt.plot(x, y, 'b')
        mmroc = pd.read_csv('./data/allusers/result/PR_data/connectweekday_avg_pr.CSV',index_col='id')
        mx = mmroc['RECALL']
        my = mmroc['TRP']
        plt.plot(mx, my, 'c')
        iforoc = pd.read_csv('./data/allusers/result/PR_data/pcaPRXY.CSV',index_col='id')
        ix = iforoc['RECALL']
        iy = iforoc['PRE']
        plt.plot(ix, iy, 'y')
        plt.show()
        '''
#GetnewscoresROC_XY()
#GetMMweekdayacv_PR_XY()
#GetnewscoresPR_XY()
#GetweekconnectUser()
'''
#画用户的异常分数图
data = pd.read_csv('./data/allusers/iForestdata/vaild_fusion_logscore.csv',index_col='id')
state = data['states']
scores = data['logscore']
abnormalx = []
abnormaly = []
for i in range(len(state)):
    if state[i] ==1:
        abnormalx.append(i)
        abnormaly.append(scores[i])

x = range(len(scores))
fig= plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlabel('Users')
ax.set_ylabel('Anormaly_Score')


l1,=ax.plot(x,scores,'*b',label = 'normal_users')
l2,=ax.plot(abnormalx,abnormaly,'*r',label = 'abnormal_uaers')


sin_legend = ax.legend(handles=[l1], loc='lower right')
ax.add_artist(sin_legend)
sin_legend = ax.legend(handles=[l2], loc='lower right')
ax.add_artist(sin_legend)
y1=[1.3,1.3]
x1=[0,250]
ax.plot(x1,y1,'-m',label = 'Threshold')

ax.legend(loc='lower right')
ax.grid(True)

ax.plot(x,scores,'-b')
ax.set_ylim(-0.3,2.8)
plt.savefig('./data/allusers/result/figure/figure2.eps',dpi = 1000,bbox_inches='tight')
plt.show()
'''
'''
#mm 和impro_mm的ROC对比
data1 = pd.read_csv('./data/allusers/result/ROC_data/weekdayconnectavg.csv',index_col='id')
data2 = pd.read_csv('./data/allusers/result/ROC_data/weekconnectpro.csv',index_col='id')
data3 = pd.read_csv('./data/allusers/result/ROC_data/MM_weekconnectpro.csv',index_col='id')
FPR1 = data1['FPR']
TPR1 =data1['TPR']
FPR2 = data2['FPR']
TPR2 =data2['TPR']
FPR3 = data3['FPR']
TPR3 =data3['TPR']

fig= plt.figure()
ax = fig.add_subplot(1,1,1)
l1, = ax.plot(FPR1,TPR1,'-m',label = 'iT')
l2, = ax.plot(FPR2,TPR2,'-y',label = 'iP')
l3, = ax.plot(FPR3,TPR3,'-c',label = 'MM')
sin_legend = ax.legend(handles=[l1], loc='lower right')
ax.add_artist(sin_legend)
sin_legend = ax.legend(handles=[l2], loc='lower right')
ax.add_artist(sin_legend)
sin_legend = ax.legend(handles=[l3], loc='lower right')
ax.add_artist(sin_legend)
#plt.legend(l1,('week_normalscore',),loc='lower right')
#plt.legend(l2,('week_avgnormalscore',),loc='upper right')
#plt.style.use('mystyle')

ax.legend(loc='lower right')
ax.grid(True)
#plt.show()
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width , box.height* 0.8])
#ax.legend(loc='center left', bbox_to_anchor=(0.2, 1.12),ncol=2)

ax.set_xlabel('False Positive %')
ax.set_ylabel('Insiders Identified %')

y1=[0,1]
x1=[0,1]
ax.plot(x1,y1,'-b')
plt.savefig('./data/allusers/result/figure/figure1.eps',dpi = 1000,bbox_inches='tight')
plt.show()'''
'''
x = np.arange(10)
fig = plt.figure()
ax = plt.subplot(111)
for i in xrange(5):
    ax.plot(x, i * x, label='$y = %ix$'%i)
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position()
# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()

'''

#one hour 用户的行为统计
data = pd.read_csv('./data/allusers/iForestdata/onehour/connect/newavg.csv',index_col='id')
#print data
normalmode = data['normamode'][:24]
abnormalmode = data['abnormalmode'][:24]
normalmax = data['normalmax'][:24]
abnormalmax = data['abnormalmax'][:24]
print normalmode
print abnormalmode
print normalmax
print abnormalmax
times=['00:00:00','01:00:00','02:00:00','03:00:00','04:00:00','05:00:00','06:00:00','07:00:00','08:00:00','09:00:00','10:00:00','11:00:00','12:00:00','13:00:00','14:00:00','15:00:00','16:00:00','17:00:00','18:00:00','19:00:00','20:00:00','21:00:00','22:00:00','23:00:00']
x=range(len(times))
fig= plt.figure()

ax = fig.add_subplot(1,1,1)

ax.set_xlabel('time')
ax.set_ylabel('count')

plt.xticks(x, times, rotation=90)
plt.margins(0.08)
plt.subplots_adjust(bottom=0.15)

l1,=ax.plot(x,normalmode,'-b',label = 'normalmode')
l2,=ax.plot(x,abnormalmode,'-r',label = 'abnormalmode')
l3,=ax.plot(x,normalmax,'-c',label = 'normalmax')
l4,=ax.plot(x,abnormalmax,'-m',label = 'abnormalmax')



sin_legend = ax.legend(handles=[l1])
ax.add_artist(sin_legend)
sin_legend = ax.legend(handles=[l2])
ax.add_artist(sin_legend)
sin_legend = ax.legend(handles=[l3])
ax.add_artist(sin_legend)
sin_legend = ax.legend(handles=[l4])

#box=ax.get_position()
#ax.set_position()
#ax.legend(loc='upper left',bbox_to_anchor=(1.0,0.5))

ax.set_title('USB connect')
ax.legend(loc='upper right')
#ax.legend(loc='upper center', bbox_to_anchor=(0.6,0.95),ncol=3,fancybox=True,shadow=True)
ax.grid(True)



plt.savefig('./data/allusers/result/figure/figure51.eps',dpi = 1000,bbox_inches='tight')
plt.show()
