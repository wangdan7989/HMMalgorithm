import GetHMMresult
import CSVFile
def GetweekconnectUser():
    connectuser = CSVFile.loadCSVfile1('./data/deviceConnect.csv')
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

GetweekconnectUser()