import csv

def loadCSVfile1(filename):
    list_file = []
    with open(filename,'rb') as csv_file:
        all_lines=csv.reader(csv_file)
        for one_line in all_lines:
            list_file.append(one_line)
    return list_file

def Writecsvtofile(filename,list):
    with open(filename, 'wb') as csvsequen:
        spamwriter = csv.writer(csvsequen, dialect='excel')
        for item in list:
            spamwriter.writerow(item)