# -*- coding: utf-8 -*-
import GetHMMresult
import CSVFile
import matplotlib.pyplot as plt
import pandas as pd
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
    weekuser = CSVFile.loadCSVfile1('./data/allusers/weekpro.csv')

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
    #CSVFile.Writecsvtofile('./data/allusers/connect_weekdayvar.csv',userinfo)

    FTPR = []
    TPR = []
    FPR = []
    thr = 0
    a = 0
    b = 1
    userinfo = weekuser
    for i in range(90000):
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
            continue
        tpr = float(tp) / (float(tp) + float(fn))
        fpr = float(fp) / (float(fp) + float(tn))
        print fpr,tpr

        TPR.append(tpr)
        FPR.append(fpr)
        #thr = 0.001*i

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
    #data.to_csv('./data/allusers/result/ROC_data/weekconnectpro.csv')

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
        tem = 'newscore'+str(i)
        newscores = data[tem]
        TPR = []
        FPR = []
        TRP = []
        RECALL = []
        thr = 0
        trp = 0
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
            thr = thr+ r


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

#GetnewscoresROC_XY()
#GetMMweekdayacv_PR_XY()
GetnewscoresPR_XY()