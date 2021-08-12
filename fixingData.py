# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:47:37 2021

@author: Deimer Ordonez Gomez
"""
from datetime import datetime, date, time,timedelta
class FileFunctions:
    
    
    ## listofRainEvents = [] ##Do Nothing
    def __init__(self, newTextFile, oldDataFile, oldSWMM, newDataFile = r"SWMM Rain Data.dat"):##r"RecentNOAA.txt"
        self.station = "STA01"
        self.minute = "00"
        self.newTextFile = newTextFile
        self.oldDataFile = oldDataFile
        self.oldSWMM = oldSWMM
        self.updatedSWMM=oldSWMM.replace('.', " 0.")
        self.newDataFile = newDataFile
        self.listofRainEvents = []
    def FormatNewFile(self):
    
            # self.newDataFile= r"SWMM Rain Data.dat"
            with open(self.newTextFile, 'r') as rf:
                with open(self.newDataFile, 'w') as wf:
                    #each line is 88 bits
                    count = 245
                    rf.seek(count)
                    chunk_size = 88
                    rf_chunk = rf.read(chunk_size)
                    rf.seek(count)
                    count+=chunk_size
                    while len(rf_chunk)>0:
                        year = rf.read(4)
                        month = rf.read(2)
                        day = rf.read(2)
                        rf.read(1)
                        precipitation = "{:.2f}".format(float(rf.read(3))/24)
                        for ct,i in enumerate(range(24),1):
                            switcher = {1:'01',
                                        2:'02', 
                                        3:'03', 
                                        4:'04', 
                                        5:'05', 
                                        6:'06', 
                                        7:'07', 
                                        8:'08',
                                        9:'09',
                                        10:'10',
                                        11:'11',
                                        12:'12',
                                        13:'13',
                                        14:'14',
                                        15:'15',
                                        16:'16',
                                        17:'17',
                                        18:'18',
                                        19:'19',
                                        20:'20',
                                        21:'21',
                                        22:'22',
                                        23:'23',
                                        24:'24',
                                        }
                            hour = switcher[ct]
                            finalResult = "{}  {}  {}  {}  {}  {}  {}\n".format(self.station, year, month, day, hour, self.minute, precipitation)
                            wf.write(finalResult)
                        rf.seek(count)
                        rf_chunk = rf.read(chunk_size)
                        rf.seek(count)
                        count+=chunk_size
            
    def runSingleData(self):
            with open(self.oldSWMM,'r') as rf:
                with open(self.updatedSWMM,'w') as wf:
                    count = 0
                    wf.seek(0)
                    for line in rf:
                        if("START_DATE" in line):
                            wf.write(line[0:21])
                            wf.write(self.startDate()+"\n")
                        elif("END_DATE" in line):
                            wf.write(line[0:21])
                            wf.write(self.endDate()+"\n")
                        elif("START_TIME" in line):
                            wf.write(line[0:21])
                            wf.write(self.startTime()+"\n")
                        elif("END_TIME" in line):
                            wf.write(line[0:21])
                            wf.write(self.endTime()+"\n")
                        elif("[RAINGAGES]" in line):
                            count+=1
                            wf.write(line)
                        elif(count ==1):
                            count+=1
                            wf.write(line)
                        elif(count ==2):
                            count+=1
                            wf.write(line)
                        elif(count==3):
                            rainGage = line.split('"')
                            for index, i in enumerate(rainGage):
                                if(index==0):
                                    wf.write(i.replace("'", ""))
                                elif(index==1):
                                    wf.write('"'+self.newDataFile+'"')
                                else:
                                    wf.write(i.replace("'",""))
                            count+=1
                        else:
                            wf.write(line)
                            
            with open(self.newDataFile, 'r') as rf:
                precipOfDay = []
                startDay = datetime(1,1,1)
                sumOfPrecip = 0.0
                for line in rf:
                   lenLine = len(line)
                   startDay = datetime(int(line[7:11]),int(line[13:15]),int(line[17:19]),int(line[21:23])-1)
                   if(startDay == datetime(int(line[7:11]),int(line[13:15]),int(line[17:19]), 0)):
                       precipOfDay = [float(line[29:lenLine])]
                       sumOfPrecip = 0.0
                   else:
                       precipOfDay.append(float(line[29:lenLine]))
                   if(startDay == datetime(int(line[7:11]),int(line[13:15]),int(line[17:19]), 23)):
                       for precip in precipOfDay:
                           sumOfPrecip += precip
                   if(sumOfPrecip>0.3):
                       newTime = datetime(int(line[7:11]),int(line[13:15]),int(line[17:19]))
                       rainSet = set(self.listofRainEvents)
                       if(newTime not in rainSet):
                           self.listofRainEvents.append(newTime)
    def runMultipleData(self):
        list1 = []
        list2 = []
        list3 = []
        with open(self.oldDataFile,'r') as rf:
            with open(self.newDataFile,'r+') as wf:
            
                list1 = rf.readlines()
                list2 = wf.readlines()
                for line in list1:
                    list3.append(line)
                    if("\n" not in line):
                        list3.append("\n")
                for line in list2:
                    list3.append(line)
                    
        with open(self.newDataFile, 'w') as wf:
            for line in list3:
                wf.write(line)
    
    def startDate(self):
            startDate = date(3000,12,12)
            with open(self.newDataFile, 'r') as rf:
                for line in rf:
                    tempstartDate = date(int(line[7:11]),int(line[13:15]),int(line[17:19]))
                    if(tempstartDate<startDate):
                        startDate = tempstartDate
                        break
                return startDate.strftime("%m/%d/%Y")
    def endDate(self):
            endDate = date(1,1,1)
            with open(self.newDataFile, 'r') as rf:
                for line in rf:
                    tempendDate = date(int(line[7:11]),int(line[13:15]),int(line[17:19]))
                    if(tempendDate>endDate):
                        endDate = tempendDate
                return endDate.strftime("%m/%d/%Y")
    def startTime(self):
            with open(self.newDataFile,'r') as rf:
                for line in rf:
                    startTime = time(int(line[21:23])-1, 00, 00) ##CANKDSANAD
                    return startTime.strftime("%H:%M:%S")
                    break
                
    def endTime(self):
            with open(self.newDataFile,'r') as rf:
                endTime = time()
                for line in rf:
                    endTime = time(int(line[21:23])-1, 00, 00) ##change back later
                return endTime.strftime("%H:%M:%S")
    def updateLowDepth(self,count, nodeid, fileName, dictionary):
        pump = "Pump("
        pond = "Pond("
        pumpEvent = "MinDepthEventP("
        genPump = "Pump("
        number = ""
        for i in nodeid:
            if(i == '1' or i=='2' or i =='3'):
                pump = pump+ i + ")"
                pond = pond+i + ")"
                pumpEvent = pumpEvent+i + ")"
                number = number+i + ")"
                genPump = genPump + i + ")General"
        oldFile = fileName.replace(str(count),str(count-1))
        fileName = fileName.replace(str(count-1),str(count))
        with open(oldFile,'r') as rf:
            with open(fileName, 'w') as wf:
                for line in rf:
                    lenLine = len(line)
                    number = 0
                    for nodeid in dictionary:
                        if(number == 0 and pump in line and pond in line and genPump in line):
                            newLine = line.replace(genPump, pumpEvent)
                            wf.write(newLine)
                            number+=1
                        elif(number == 0 and nodeid in line and "TABULAR" in line and ("660" in line or "658" in line or "655" in line)):
                                newLine = line[0:37] + "{:.2f}".format(dictionary[nodeid]) + line[41:lenLine]
                                wf.write(newLine)
                                number+=1
                        elif(number == 0 and nodeid in line and ("663" in line or "664" in line or "661" in line or "660" in line or "670" in line or "662" in line or "667" in line or "669" in line or "668" in line or "666" in line or "665" in line) and "Sub" not in line):
                                newLine = line[0:39] + "{:.2f}".format(dictionary[nodeid]) + line[43:lenLine]
                                wf.write(newLine)
                                number+=1
                        elif(number == 0 and nodeid in line and "CIRCULAR" not in line and "YES" not in line and "3228.484" not in line and "BC" not in line and "SURFACE" not in line and "SOIL" not in line and "STORAGE" not in line
                                                                     and "DRAIN" not in line and "Event" not in line and "General" not in line and "14500" not in line and "3983" not in line and "6767" not in line
                                                                     and "11336" not in line and "14533" not in line and "17202" not in line and "15630" not in line and "23266" not in line and "33431" not in line and 
                                                                     "41741" not in line and "48690" not in line and "55193" not in line and "58261" not in line and "61314" not in line and "62567" not in line and "65603"
                                                                     not in line and "7333.795" not in line and "6727.749" not in line and "6710" not in line and "5742" not in line and "5502" not in line and"4094" not in line
                                                                     and "4432" not in line and "3491" not in line and "2772" not in line and "3290" not in line and "2396" not in line and "1799" not in line and"1989"
                                                                     not in line and "1361" not in line and "1472" not in line and "804" not in line and "1007" not in line and "2035" not in line and "1786" not in line
                                                                     and "1260" not in line and "1507" not in line and "1660" not in line and "8206" not in line and "5545" not in line and "2271" not in line and "6966" not in line
                                                                     and "5387" not in line and "2981" not in line and "3067" not in line and "2392" not in line and "1917" not in line and "1933" not in line and "2637" not in line
                                                                     and "Sub" not in line):
                                newLine = line[0:95] + "{:.2f}".format(dictionary[nodeid]) + "\n"
                                wf.write(newLine)
                                number+=1
                    if(number == 0):
                        wf.write(line)
                        
    def updateMaxDepth(self, count, nodeid, fileName, dictionary):
        pump = "Pump("
        pond = "Pond("
        pumpEvent = "MaxDepthEventPump("
        genPump = "Pump("
        number = ""
        for i in nodeid:
            if(i == '1' or i=='2' or i =='3'):
                pump = pump+ i + ")"
                pond = pond+i + ")"
                pumpEvent = pumpEvent+i + ")"
                number = number+i + ")"
                genPump = genPump + i + ")General"
        oldFile = fileName.replace(str(count),str(count-1))
        fileName = fileName.replace(str(count-1),str(count))
        with open(oldFile,'r') as rf:
            with open(fileName, 'w') as wf:
                for line in rf:
                    number = 0
                    lenLine = len(line)
                    for nodeid in dictionary:
                        if(number == 0 and pump in line and pond in line and genPump in line):
                            newLine = line.replace(genPump, pumpEvent)
                            wf.write(newLine)
                            number+=1
                        elif(number == 0 and nodeid in line and "TABULAR" in line and ("660" in line or "658" in line or "655" in line)):
                                newLine = line[0:37] + "{:.2f}".format(dictionary[nodeid]) + line[41:lenLine]
                                wf.write(newLine)
                                number+=1
                        elif(number == 0 and nodeid in line and ("663" in line or "664" in line or "661" in line or "660" in line or "670" in line or "662" in line or "667" in line or "669" in line or "668" in line or "666" in line or "665" in line) and "Sub" not in line):
                                newLine = line[0:39] + "{:.2f}".format(dictionary[nodeid]) + line[43:lenLine]
                                wf.write(newLine)
                                number+=1
                        elif(number == 0 and nodeid in line and "CIRCULAR" not in line and "YES" not in line and "3228.484" not in line and "BC" not in line and "SURFACE" not in line and "SOIL" not in line and "STORAGE" not in line
                                                                     and "DRAIN" not in line and "Event" not in line and "General" not in line and "14500" not in line and "3983" not in line and "6767" not in line
                                                                     and "11336" not in line and "14533" not in line and "17202" not in line and "15630" not in line and "23266" not in line and "33431" not in line and 
                                                                     "41741" not in line and "48690" not in line and "55193" not in line and "58261" not in line and "61314" not in line and "62567" not in line and "65603"
                                                                     not in line and "7333.795" not in line and "6727.749" not in line and "6710" not in line and "5742" not in line and "5502" not in line and"4094" not in line
                                                                     and "4432" not in line and "3491" not in line and "2772" not in line and "3290" not in line and "2396" not in line and "1799" not in line and"1989"
                                                                     not in line and "1361" not in line and "1472" not in line and "804" not in line and "1007" not in line and "2035" not in line and "1786" not in line
                                                                     and "1260" not in line and "1507" not in line and "1660" not in line and "8206" not in line and "5545" not in line and "2271" not in line and "6966" not in line
                                                                     and "5387" not in line and "2981" not in line and "3067" not in line and "2392" not in line and "1917" not in line and "1933" not in line and "2637" not in line
                                                                     and "Sub" not in line):
                                newLine = line[0:95] + "{:.2f}".format(dictionary[nodeid]) +"\n"
                                wf.write(newLine)
                                number+=1
                    if(number == 0):
                            wf.write(line)
                        
    def checkLowDepth(self, depth, nodeid, fileName):
        pump = "Pump("
        pond = "Pond("
        pumpEvent = "MinDepthEventP("
        pondReady = False
        for i in nodeid:
            if(i == '1' or i=='2' or i =='3'):
                pump= pump+i + ")"
                pond=pond+ i + ")"
                pumpEvent =pumpEvent+ i + ")"
        with open(fileName, 'r') as rf:
            for line in rf:
                if(pump in line and pond in line and pumpEvent not in line):
                    pondReady = True
        if (depth<=0.4 and pondReady and pond=="Pond(1)"):
            return True
        elif (depth<=0.4 and pondReady and pond=="Pond(2)"):
            return True
        elif (depth<=2.99 and pondReady and pond=="Pond(3)"):
            return True
        else:
            return False
        
    def checkMaxDepth(self, depth, nodeid, fileName): ## going to be max
        pump = "Pump("
        pond = "Pond("
        pumpEvent = "MaxDepthEventPump("
        pondReady = False
        for i in nodeid:
            if(i == '1' or i=='2' or i =='3'):
                pump = pump+ i + ")"
                pond = pond+ i + ")"
                pumpEvent = pumpEvent+ i + ")"
        with open(fileName, 'r') as rf:
            for line in rf:
                if(pump in line and pond in line and pumpEvent not in line):
                    pondReady = True
        if (depth>=8 and pondReady and pond=="Pond(1)"):
            return True
        elif (depth>=10 and pondReady and pond=="Pond(2)"):
            return True
        elif (depth>=12 and pondReady and pond=="Pond(3)"):
            return True
        else:
            return False
    
    def checkRainEvent(self, dateTime, rainEvent):
        
        if(rainEvent>=25):
            return True
        listEvents = self.listofRainEvents
        currentTime = datetime(dateTime.year, dateTime.month, dateTime.day)

        for dates in listEvents:
            if(dates-currentTime==timedelta(1)):
                return True
        return False
    
    def changeRainEvent(self, fileName, rainEvent):
        if (rainEvent>=26):
            return True
        if(rainEvent==0):
            return False
        pump1 = "Pump(1)"
        pond1 = "Pond(1)"
        pumpEvent = "RainEventFuturePump(1)"
        with open(fileName,'r') as rf:
            for line in rf:
                if(pump1 in line and pond1 in line and pumpEvent not in line):
                    return True
        return False
    def updateRainEvent(self, count, fileName, rainEvent, dictionary):
        pump1 = "Pump(1)"
        pump2 = "Pump(2)"
        pump3 = "Pump(3)"
        pond1 = "Pond(1)"
        pond2 = "Pond(2)"
        pond3 = "Pond(3)"
        pump1Event1 = "MinDepthEventP(1)"
        pump1Event2 = "MaxDepthEventPump(1)"
        pump1Event3 = "Pump(1)General"
        pump2Event1 = "MinDepthEventP(2)"
        pump2Event2 = "MaxDepthEventPump(2)"
        pump2Event3 = "Pump(2)General"
        pump3Event1 = "MinDepthEventP(3)"
        pump3Event2 = "MaxDepthEventPump(3)"
        pump3Event3 = "Pump(3)General"
        
        oldFile = fileName.replace(str(count),str(count-1))
        fileName = fileName.replace(str(count-1),str(count))
        if(rainEvent!=26):
            with open(oldFile,'r') as rf:
                with open(fileName, 'w') as wf:
                    for line in rf:
                        lenLine=len(line)
                        number = 0
                        for nodeid in dictionary:
                            
                            if(number == 0 and pump1 in line and pond1 in line and pump1Event1 in line):
                                newLine = line.replace(pump1Event1, "RainEventFuturePump(1)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump1 in line and pond1 in line and pump1Event2 in line):
                                newLine = line.replace(pump1Event2, "RainEventFuturePump(1)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump1 in line and pond1 in line and pump1Event3 in line):
                                newLine = line.replace(pump1Event3, "RainEventFuturePump(1)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump2 in line and pond2 in line and pump2Event1 in line):
                                newLine = line.replace(pump2Event1, "RainEventFuturePump(2)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump2 in line and pond2 in line and pump2Event2 in line):
                                newLine = line.replace(pump2Event2, "RainEventFuturePump(2)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump2 in line and pond2 in line and pump2Event3 in line):
                                newLine = line.replace(pump2Event3, "RainEventFuturePump(2)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump3 in line and pond3 in line and pump3Event1 in line):
                                newLine = line.replace(pump3Event1, "RainEventFuturePump(3)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump3 in line and pond3 in line and pump3Event2 in line):
                                newLine = line.replace(pump3Event2, "RainEventFuturePump(3)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and pump3 in line and pond3 in line and pump3Event3 in line):
                                newLine = line.replace(pump3Event3, "RainEventFuturePump(3)")
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and nodeid in line and "TABULAR" in line and ("660" in line or "658" in line or "655" in line)):
                                newLine = line[0:37] + "{:.2f}".format(dictionary[nodeid]) + line[41:lenLine]
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and nodeid in line and ("663" in line or "664" in line or "661" in line or "660" in line or "670" in line or "662" in line or "667" in line or "669" in line or "668" in line or "666" in line or "665" in line) and "Sub" not in line):
                                newLine = line[0:39] + "{:.2f}".format(dictionary[nodeid]) + line[43:lenLine]
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and nodeid in line and "CIRCULAR" not in line and "YES" not in line and "3228.484" not in line and "BC" not in line and "SURFACE" not in line and "SOIL" not in line and "STORAGE" not in line
                                                                     and "DRAIN" not in line and "Event" not in line and "General" not in line and "14500" not in line and "3983" not in line and "6767" not in line
                                                                     and "11336" not in line and "14533" not in line and "17202" not in line and "15630" not in line and "23266" not in line and "33431" not in line and 
                                                                     "41741" not in line and "48690" not in line and "55193" not in line and "58261" not in line and "61314" not in line and "62567" not in line and "65603"
                                                                     not in line and "7333.795" not in line and "6727.749" not in line and "6710" not in line and "5742" not in line and "5502" not in line and"4094" not in line
                                                                     and "4432" not in line and "3491" not in line and "2772" not in line and "3290" not in line and "2396" not in line and "1799" not in line and"1989"
                                                                     not in line and "1361" not in line and "1472" not in line and "804" not in line and "1007" not in line and "2035" not in line and "1786" not in line
                                                                     and "1260" not in line and "1507" not in line and "1660" not in line and "8206" not in line and "5545" not in line and "2271" not in line and "6966" not in line
                                                                     and "5387" not in line and "2981" not in line and "3067" not in line and "2392" not in line and "1917" not in line and "1933" not in line and "2637" not in line
                                                                     and "Sub" not in line):
                                newLine = line[0:95] + "{:.2f}".format(dictionary[nodeid]) +"\n"
                                wf.write(newLine)
                                number+=1
                        if(number == 0):
                            wf.write(line)
        else:
           with open(oldFile,'r') as rf:
                with open(fileName, 'w') as wf:
                    for line in rf:
                        lenLine = len(line)
                        number = 0
                        for nodeid in dictionary:
                            if(number == 0 and pump1 in line and pond1 in line and "RainEventFuturePump(1)" in line):
                                newLine = line.replace("RainEventFuturePump(1)", "Pump(1)General")
                                number +=1
                                wf.write(newLine)
                            elif(number == 0 and pump2 in line and pond2 in line and "RainEventFuturePump(2)" in line):
                                newLine = line.replace("RainEventFuturePump(2)", pump2Event3)
                                number +=1
                                wf.write(newLine)
                            elif(number == 0 and pump3 in line and pond3 in line and "RainEventFuturePump(3)" in line):
                                newLine = line.replace("RainEventFuturePump(3)", pump3Event3)
                                number+=1
                                wf.write(newLine)
                            elif(number == 0 and nodeid in line and "TABULAR" in line and ("660" in line or "658" in line or "655" in line)):
                                newLine = line[0:37] + "{:.2f}".format(dictionary[nodeid]) + line[41:lenLine]
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and nodeid in line and ("663" in line or "664" in line or "661" in line or "660" in line or "670" in line or "662" in line or "667" in line or "669" in line or "668" in line or "666" in line or "665" in line) and "Sub" not in line):
                                newLine = line[0:39] + "{:.2f}".format(dictionary[nodeid]) + line[43:lenLine]
                                wf.write(newLine)
                                number+=1
                            elif(number == 0 and nodeid in line and "CIRCULAR" not in line and "YES" not in line and "3228.484" not in line and "BC" not in line and "SURFACE" not in line and "SOIL" not in line and "STORAGE" not in line
                                                                     and "DRAIN" not in line and "Event" not in line and "General" not in line and "14500" not in line and "3983" not in line and "6767" not in line
                                                                     and "11336" not in line and "14533" not in line and "17202" not in line and "15630" not in line and "23266" not in line and "33431" not in line and 
                                                                     "41741" not in line and "48690" not in line and "55193" not in line and "58261" not in line and "61314" not in line and "62567" not in line and "65603"
                                                                     not in line and "7333.795" not in line and "6727.749" not in line and "6710" not in line and "5742" not in line and "5502" not in line and"4094" not in line
                                                                     and "4432" not in line and "3491" not in line and "2772" not in line and "3290" not in line and "2396" not in line and "1799" not in line and"1989"
                                                                     not in line and "1361" not in line and "1472" not in line and "804" not in line and "1007" not in line and "2035" not in line and "1786" not in line
                                                                     and "1260" not in line and "1507" not in line and "1660" not in line and "8206" not in line and "5545" not in line and "2271" not in line and "6966" not in line
                                                                     and "5387" not in line and "2981" not in line and "3067" not in line and "2392" not in line and "1917" not in line and "1933" not in line and "2637" not in line
                                                                     and "Sub" not in line):
                                newLine = line[0:95] + "{:.2f}".format(dictionary[nodeid]) +"\n"
                                wf.write(newLine)
                                number+=1
                        if(number==0):
                                wf.write(line)
        
    def checkMidDepth(self, depth, nodeid, fileName):
        pump = "Pump("
        pond = "Pond("
        pumpMinEvent = "MinDepthEventP("
        pumpMaxEvent = "MaxdepthEventPump("
        genPump = "Pump("
        pondReady = False
        actualPump = ""
        for i in nodeid:
            if(i == '1' or i=='2' or i =='3'):
                genPump = genPump + i +")General"
                pump= pump+i + ")"
                pond=pond+ i + ")"
                pumpMinEvent =pumpMinEvent+ i + ")"
                pumpMaxEvent =pumpMaxEvent+ i + ")"
        with open(fileName, 'r') as rf:
            for line in rf:
                if(pump in line and pond in line and genPump not in line):
                    if(pumpMinEvent in line):
                        actualPump = pumpMinEvent
                    elif(pumpMaxEvent in line):
                        actualPump = pumpMaxEvent
                    pondReady = True
        if (pondReady and pond=="Pond(1)"):
            if(actualPump==pumpMinEvent and depth>6):
                return True
            elif(actualPump == pumpMaxEvent and depth<=5):
                return True
        elif (pondReady and pond=="Pond(2)"):
            if(actualPump==pumpMinEvent and depth>5):
                return True
            elif(actualPump==pumpMaxEvent and depth<=4):
                return True
        elif (pondReady and pond=="Pond(3)"):
            if(actualPump==pumpMinEvent and depth>=7.5):
                return True
            elif(actualPump == pumpMaxEvent and depth<=6):
                return True
        else:
            return False
        
    def updateMidDepth(self, count, nodeid, fileName, dictionary):
        pump = "Pump("
        pond = "Pond("
        pumpMinEvent = "MinDepthEventP("
        pumpMaxEvent = "MaxdepthEventPump("
        genPump = "Pump("
        for i in nodeid:
            if(i == '1' or i=='2' or i =='3'):
                pump = pump+ i + ")"
                pond = pond+i + ")"
                pumpMinEvent = pumpMinEvent + i +")"
                pumpMaxEvent = pumpMaxEvent+i + ")"
                genPump = genPump + i + ")General"
        oldFile = fileName.replace(str(count),str(count-1))
        fileName = fileName.replace(str(count-1),str(count))
        with open(oldFile,'r') as rf:
            with open(fileName, 'w') as wf:
                for line in rf:
                    number = 0 ##
                    lenLine = len(line)
                    for nodeid in dictionary:
                        if(number == 0 and pump in line and pond in line and pumpMinEvent in line):
                            newLine = line.replace(pumpMinEvent, genPump)
                            wf.write(newLine)
                            number+=1
                        elif(number == 0 and pump in line and pond in line and pumpMaxEvent in line):
                            newLine = line.replace(pumpMaxEvent, genPump)
                            wf.write(newLine)
                            number+=1
                        elif(number == 0 and nodeid in line and "TABULAR" in line and ("660" in line or "658" in line or "655" in line)):
                                newLine = line[0:37] + "{:.2f}".format(dictionary[nodeid]) + line[41:lenLine]
                                wf.write(newLine)
                                number+=1
                        elif(number == 0 and nodeid in line and ("663" in line or "664" in line or "661" in line or "660" in line or "670" in line or "662" in line or "667" in line or "669" in line or "668" in line or "666" in line or "665" in line) and "Sub" not in line):
                                newLine = line[0:39] + "{:.2f}".format(dictionary[nodeid]) + line[43:lenLine]
                                wf.write(newLine)
                                number+=1
                        elif(number == 0 and nodeid in line and "CIRCULAR" not in line and "YES" not in line and "3228.484" not in line and "BC" not in line and "SURFACE" not in line and "SOIL" not in line and "STORAGE" not in line
                                                                     and "DRAIN" not in line and "Event" not in line and "General" not in line and "14500" not in line and "3983" not in line and "6767" not in line
                                                                     and "11336" not in line and "14533" not in line and "17202" not in line and "15630" not in line and "23266" not in line and "33431" not in line and 
                                                                     "41741" not in line and "48690" not in line and "55193" not in line and "58261" not in line and "61314" not in line and "62567" not in line and "65603"
                                                                     not in line and "7333.795" not in line and "6727.749" not in line and "6710" not in line and "5742" not in line and "5502" not in line and"4094" not in line
                                                                     and "4432" not in line and "3491" not in line and "2772" not in line and "3290" not in line and "2396" not in line and "1799" not in line and"1989"
                                                                     not in line and "1361" not in line and "1472" not in line and "804" not in line and "1007" not in line and "2035" not in line and "1786" not in line
                                                                     and "1260" not in line and "1507" not in line and "1660" not in line and "8206" not in line and "5545" not in line and "2271" not in line and "6966" not in line
                                                                     and "5387" not in line and "2981" not in line and "3067" not in line and "2392" not in line and "1917" not in line and "1933" not in line and "2637" not in line
                                                                     and "Sub" not in line):
                                newLine = line[0:95] + "{:.2f}".format(dictionary[nodeid]) +"\n"
                                wf.write(newLine)
                                number+=1
                    if(number == 0):
                        wf.write(line)
