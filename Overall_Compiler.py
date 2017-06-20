import json
import csv
import pprint
import time
from time import strptime, mktime
filelist={'FTC1':['C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170531.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170601.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170602.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170604.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170605.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170606.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170607.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170608.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170609.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1log20170614.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1/FCT1log20170615.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT1log20170617.csv'
                  ],
           'FTC2':['C:/Users/Michael/Dropbox/logs/FCT2/FCT2log20170601.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT2/FCT2log20170604.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT2/FCT2log20170607.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT2/FCT2log20170608.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT2/FCT2log20170609.csv',
                   'C:/Users/Michael/Dropbox/logs/FCT2/FCT2log20170616.csv'],
           'AOITop':'C:/Users/Michael/Documents/HJR-安朗杰-TOP-AOI.csv',
           'AOIBottom':'C:/Users/Michael/Documents/HJR-安朗杰-BOT-AOI.csv',
           'ITC':'C:/Users/Michael/Downloads/211700167 - ICT',
           'PreSMT':'C:/Users/Michael/Documents/SMTlog20170523.csv',
           'SMT':'C:/Users/Michael/Documents/SMTlog20170523.csv',
           'PCB Log':'C:/Users/Michael/Documents/AOIlog20170523.csv'}
fullList=[]
def PCBfinder(x,y,z):
    with open(filelist['PCB Log']) as csvfile:
            spamreader=csv.reader(csvfile)
            for row in spamreader:
                if row[2]==str(x) and row[3]==str(y):
                    return row[1]
def ITCLookup(filepath):
    fileobj=open(str(filepath),'r')
    fileobj2=open(str(filepath),'r')
    count=0
    count2=0
    failList=[]
    fails=[]
    total=[]
    for row in fileobj:
        if row[0]=='@':
            count+=1
            total.append({'SN':row[24:33],'ITCScan':'Pass'})
        if row[0]=='F':
            failList.append(count)
    for row in fileobj2:
        if row[0]=='@':
            count2+=1
        for y in failList:
            if count2==y and row[21:23]=='SN':
                failDict={'SN':row[24:33],'ITCScan':'Fail'}
                fails.append(failDict)
    for x in total:
        for y in fails:
            if x['SN']==y['SN']:
                x['ITCScan']='Fail'
    for x in total:
        for y in total:
            if x['SN']==y['SN']:
                total.remove(y)
    return total
def AOIBotSearch(filepath):
    alist=[]
    with open(str(filepath), 'r', encoding='utf-8') as csvfile:
        obj=csv.reader(csvfile)
        for row in obj:
                alist.append({'MAC':row[3][:12],'AOIScan':row[1]})         
    return alist
def AOITopSearch(filepath):
    blist=[]
    with open(str(filepath), 'r', encoding='utf-8') as csvfile:
        obj=csv.reader(csvfile)
        for row in obj:
                blist.append({'PCB':row[3],'AOIScan':row[1]})         
    return blist
def preSMT(filepath):
    clist=[]
    newdict={}
    with open(filepath) as csvfile:
        spamreader=csv.reader(csvfile)
        for row in spamreader:
            clist.append({'SN':row[3],'PreSMT':row[0]})
        for f in clist:
            c=str(f['PreSMT'])
            try:
                d=time.strptime(c,'%Y-%m-%d %H:%M:%S')
            except ValueError:
                d=time.strptime(c,'%m/%d/%Y %H:%M')
            t=time.mktime(d)
            f['PreSMTScan']=t
    return clist
def SMT(filepath):
    dlist=[]
    newdict={}
    with open(filepath) as csvfile:
        spamreader=csv.reader(csvfile)
        for row in spamreader:
            dlist.append({'SN':row[3],'SMT':row[0]})
        for f in dlist:
            c=str(f['SMT'])
            try:
                d=time.strptime(c,'%Y-%m-%d %H:%M:%S')
            except ValueError:
                d=time.strptime(c,'%m/%d/%Y %H:%M')
            t=time.mktime(d)
            f['SMTScan']=t
    return dlist
def filewrite(filepath):
    with open(filepath) as csvfile:
        spamreader=csv.reader(csvfile)
        for row in spamreader:
            if row[0]=='Count' or row[3]=='N/A':
                pass
            else:
                MAC=row[3]
                SN=row[4]
                ProgCode=row[5]
                file2={}
                file={'MAC':MAC,'SN':SN,'ProgCode':ProgCode}
                file['PCB Number']=PCBfinder(MAC,SN,ProgCode)
                if row[6]!='N/A':
                    file2['MCU FW rev']=row[6]
                if row[7]!='N/A':
                    file2['MCU P/F']=row[7]
                if row[8]!='N/A':
                    file2['BLE FW rev']=row[8]
                if row[8]!='N/A':
                    file2['BLE P/F']=row[9]
                if row[10]!='N/A':
                    file2['WiFi SNR']=row[10] 
                if row[11]!='N/A':
                    file2['WiFi P/F']=row[11]
                if row[12]!='N/A':
                    file2['BLE Trim Val']=row[12]
                if row[13]!='N/A':
                    file2['BLE Freq']=row[13]
                if row[14]!='N/A':
                    file2['BLE Freq P/F']=row[14]
                if row[15]!='N/A':
                    file2['BLE Power']=row[15]
                if row[16]!='N/A':
                    file2['BLE Power P/F']=row[16]
                if row[17]!='N/A':
                    file2['BLE Press P/F']=row[17]
                if row[18]!='N/A':
                    file2['LED1 Color']=row[18]
                if row[19]!='N/A':
                     file2['LED1 Color P/F']=row[19]
                if row[20]!='N/A':
                    file2['LED1 Intensity']=row[20]
                if row[21]!='N/A':
                    file2['LED1 Intensity P/F']=row[21]
                if row[22]!='N/A':
                    file2['LED2 Color']=row[22]
                if row[23]!='N/A':
                    file2['LED2 Color P/F']=row[23]
                if row[24]!='N/A':
                    file2['LED2 Intensity']=row[24]
                if row[25]!='N/A':
                    file2['LED2 Intensity P/F']=row[25]
                if row[26]!='N/A':
                    file2['LED3 Color']=row[26]
                if row[27]!='N/A':
                    file2['LED3 Color P/F']=row[27]
                if row[28]!='N/A':
                    file2['LED3 Intensity']=row[28]
                if row[29]!='N/A':
                    file2['LED3 Intensity P/F']=row[29]
                if row[30]!='N/A':
                    file2['BLE Beacon P/F']=row[30]
                if row[31]!='N/A':
                    file2['DUT Final P/F']=row[31]
                file['FTC1 Results']=file2
                fullList.append(file)
    for x in fullList:
        a=AOIBotSearch(filelist['AOIBottom'])
        for y in a:
            if x["MAC"]==y['MAC']:
                x['AOIScan']=y['AOIScan']
    for v in fullList:
        b=AOITopSearch(filelist['AOITop'])
        for w in b:
            if v["PCB Number"]==w['PCB']:
                v['AOIScan']=w['AOIScan']
    for s in fullList:
        c=ITCLookup(filelist['ITC'])
        for t in c:
            if s['PCB Number']==t['SN']:
                s['ITCScan']=t['ITCScan']
    for q in fullList:
        d=preSMT(filelist['PreSMT'])
        for z in d:
            if q['SN']==z['SN']:
                q['PreSMTScan']=z['PreSMTScan']
   
    for g in fullList:
        e=SMT(filelist['SMT'])
        for a in e:
            if g['SN']==a['SN']:
                g['SMTScan']=a['SMTScan']
fullList2=[]
def filewrite2(filepath):
        with open(filepath) as csvfile:
            spamreader=csv.reader(csvfile)
            for row in spamreader:
                if row[0]=='Count' or row[3]=='N/A':
                    pass
                else:
                    SN=row[3]
                    file={'SN':SN}
                    file2={}
                    if row[4]!='N/A':
                        file2['Btn Press P/F']=row[4]
                    if row[5]!='N/A':
                        file2['LED1 Color']=row[5]
                    if row[6]!='N/A':
                        file2['LED1 Color P/F']=row[6]
                    if row[7]!='N/A':
                        file2['LED2 Color']=row[7]
                    if row[8]!='N/A':
                        file2['LED2 Color P/F']=row[8]
                    if row[9]!='N/A':
                        file2['LED3 Color']=row[9]
                    if row[10]!='N/A':
                        file2['LED3 Color P/F']=row[10]
                    if row[11]!='N/A':
                        file2['Factory Test P/F']=[row[11],row[12],row[13]]
                    file['FTC2 Results']=file2
                    fullList2.append(file)

for files in filelist['FTC1']:
    filewrite(files)
for morefiles in filelist['FTC2']:
    filewrite2(morefiles)
for f in fullList:
    for e in fullList2:
        if f['SN']==e['SN']:
            f['FTC2 Results']=e['FTC2 Results']
for x in fullList:
    if fullList.index(x)%10==0:
        pp=pprint.PrettyPrinter(indent=4)
        pp.pprint(x)
j=json.dumps(fullList)
with open('C:/Users/Michael/Documents/test_output1.json','w') as f:
    f.write(j)
print('compile finished')
