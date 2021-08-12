# -*- coding: utf-8 -*-
from pyswmm import Simulation, Nodes, Links
from fixingData import FileFunctions
from datetime import datetime, timedelta


newTextFile = r"RecentNOAAList.txt" ## input .txt file if formatting new rain data
oldDataFile = r"PrecipitationList.dat" ##input .dat file to be used
newDataFile = r"" ## Input new .dat file if text file is already formatted
oldSWMM = r"Warner Park Variable Model.inp" ##(Required) input .inp File to run SWMM

if (newDataFile != r""):
    fileFunctions = FileFunctions(newTextFile,oldDataFile,oldSWMM, newDataFile)
else:
    fileFunctions = FileFunctions(newTextFile, oldDataFile, oldSWMM);
startYear = 1
try:
    answer = ''
    answer2 = ''
    while(True):
        answer = str(input("Are you formatting data?(y/n): "))
        ##answer = 'n'
        if(answer=='y'):
            fileFunctions.FormatNewFile()
            break
        elif(answer=='n'):
            break
        else:
            print("Wrong answer, try again: ")
    while(True):
        answer2 = str(input("Are you appending data?(y/n): "))
        ##answer2 = 'n'
        if(answer2=='y'):
            fileFunctions.runMultipleData()
            fileFunctions.runSingleData()
            break
        elif(answer2=='n'):
            fileFunctions.runSingleData()
            break
        else:
            print("Not a valid answer, (y/n), try again: ")
    while(True):
        answer3 = int(input("How many years of data would you like to look at?(1,2,...): "))
        if(answer3>=1):
            startYear = answer3*365
            break
        else:
            print("Value cannot be less than 1")
except TypeError:
    print("Not a valid answer try again: ")
except ValueError:
    print("Not a valid answer try again: ")
simComplete = False
reportNum = 0
simLastTime = datetime(1,1,1,1,1,1)
rainEvent = 0

updatedSWMM = r"Warner Park Variable Model "+str(reportNum)+".inp"
updatedrpt = r"Report " + str(reportNum)+ r".rpt"
def checkTime():
    if(simLastTime==datetime(1,1,1,1,1,1)):
        return True
    else:
        return False

while(not simComplete):
    updatedSWMM = r"Warner Park Variable Model "+str(reportNum)+".inp"
    updatedrpt = r"Report " + str(reportNum)+ r".rpt"
    with Simulation(updatedSWMM,
                    updatedrpt) as sim:
        nodes = Nodes(sim)
        links = Links(sim)
        Pump1 = links["Pump(1)"]
        Pump2 = links["Pump(2)"]
        Pump3 = links["Pump(3)"]
        Pond1 = nodes["Pond(1)"]
        Pond2 = nodes["Pond(2)"]
        Pond3 = nodes["Pond(3)"]
        P1_Outlet = nodes["P(1)_Outlet"]
        Park1 = nodes["Park(1)"]
        Park1_Outlet = nodes["Park(1)_Outlet"]
        P2_Inlet = nodes["P(2)_Inlet"]
        P2_Outlet = nodes["P(2)_Outlet"]
        Junc1 = nodes["Junc(1)"]
        J5 = nodes["J5"]
        J4 = nodes["J4"]
        J6 = nodes["J6"]
        Junc2 = nodes["Junc(2)"]
        P3_Inlet = nodes["P(3)_Inlet"]
        J9 = nodes["J9"]
        J9_Out = nodes["J9_Out"]
        J10 = nodes["J10"]
        J10_Out = nodes["J10_Out"]
        J11 = nodes["J11"]
        J11_Out = nodes["J11_Out"]
        J8 = nodes["J8"]
        J8_Out = nodes["J8_Out"]
        Channel3 = nodes["Channel(3)"]
        Channel2 = nodes["Channel(2)"]
        Channel1 = nodes["Channel(1)"]
        C1 = links["P(1)_Out-Park(1)_Out"]
        C2 = links["Park(1)-Park(1)_Out"]
        C3 = links["Park(1)_Out-P(2)_In"]
        C4 = links["P(2)_In-Pond(2)"]
        C5 = links["P(1)_Outlet-Junc(1)"]
        C6 = links["J5-Junc(1)"]
        C7 = links["Junc(1)-Junc(2)"]
        C8 = links["J4-Junc(2)"]
        C9 = links["J6-Junc(2)"]
        C10 = links["Junc(2)-P(2)_Inlet"]
        C11 = links["Pond(3)-P(3)_Out"]
        C11 = links["J9-J9_Out"]
        C12 = links["J9_Out-Pond(3)"]
        C13 = links["J10-J10_Out"]
        C14 = links["J11-J11_Out"]
        C15 = links["J8-J8_Out"]
        C16 = links["J11_Out-Ch(3)"]
        C17 = links["*Ch(3)"]
        C18 = links["*Ch(2)"]
        C19 = links["*20"]
        C20 = links["*21"]
        C21 = links["*Ch(1)"]
        if(not checkTime()):
            sim.start_time=simLastTime
        if(sim.end_time-sim.start_time>=timedelta(startYear)):
            sim.start_time = sim.end_time-timedelta(startYear)
        for step in sim:
            dictOfNL = {Pump1.linkid:Pump1.flow,Pump2.linkid:Pump2.flow,Pump3.linkid:Pump3.flow,Pond1.nodeid:Pond1.depth,Pond2.nodeid:Pond2.depth,Pond3.nodeid:Pond3.depth,P1_Outlet.nodeid:P1_Outlet.depth,Park1.nodeid:Park1.depth,
                    Park1_Outlet.nodeid:Park1_Outlet.depth,P2_Inlet.nodeid:P2_Inlet.depth,P2_Outlet.nodeid:P2_Outlet.depth,Junc1.nodeid:Junc1.depth,J5.nodeid:J5.depth,J4.nodeid:J4.depth,J6.nodeid:J6.depth,
                    Junc2.nodeid:Junc2.depth,P3_Inlet.nodeid:P3_Inlet.depth,J9.nodeid:J9.depth,J9_Out.nodeid:J9_Out.depth,J10.nodeid:J10.depth,J10_Out.nodeid:J10_Out.depth,J11.nodeid:J11.depth,J11_Out.nodeid:J11_Out.depth,
                    J8.nodeid:J8.depth,J8_Out.nodeid:J8_Out.depth,Channel3.nodeid:Channel3.depth,Channel2.nodeid:Channel2.depth,Channel1.nodeid:Channel1.depth,C1.linkid:C1.flow,C2.linkid:C2.flow,C3.linkid:C3.flow,C4.linkid:C4.flow,
                    C5.linkid:C5.flow,C6.linkid:C6.flow,C7.linkid:C7.flow,C8.linkid:C8.flow,C9.linkid:C9.flow,C10.linkid:C10.flow,C11.linkid:C11.flow,C12.linkid:C12.flow,C13.linkid:C13.flow,C14.linkid:C14.flow,
                    C15.linkid:C15.flow,C16.linkid:C16.flow,C17.linkid:C17.flow,C18.linkid:C18.flow,C19.linkid:C19.flow,C20.linkid:C20.flow,C21.linkid:C21.flow}
            if(sim.end_time-sim.start_time>=timedelta(1)):
                sim.step_advance(3600)
            else:
                difference = sim.end_time-simLastTime
                sim.step_advance(difference.total_seconds()-1)
            simLastTime = sim.current_time
            #print(type(sim.current_time))
            print("Current_Time: "+ str(simLastTime))
            print("Last time of restart: "+str(sim.start_time))
            print("End time: " + str(sim.end_time))
            print("Pond 1 depth: " + str(Pond1.depth))
            print("Pond 2 depth: "+ str(Pond2.depth))
            print("Pond 3 depth: "+str(Pond3.depth))
            print("Pump 1 flow: "+str(Pump1.flow))
            print("Pump 2 flow: "+str(Pump2.flow))
            print("Pump 3 flow: "+str(Pump3.flow))
            if(fileFunctions.checkRainEvent(sim.current_time, rainEvent)):
                rainEvent +=1
                simLastTime = sim.current_time
                if(fileFunctions.changeRainEvent(updatedSWMM, rainEvent)):
                    reportNum+=1
                    fileFunctions.updateRainEvent(reportNum, updatedSWMM, rainEvent, dictOfNL)
                    if(rainEvent==1):
                        print("RAIN EVENT STARTED AT: " + str(sim.current_time))
                    elif(rainEvent==26):
                        print("RAIN EVENT STOPPED AT: "+ str(sim.current_time))
                        rainEvent = 0
                    sim.terminate_simulation()
                else:
                    print("RAIN EVENT IN PROGRESS AT: "+str(sim.current_time))
            elif(fileFunctions.checkLowDepth(Pond1.depth, Pond1.nodeid, updatedSWMM)): 
                simLastTime=sim.current_time
                print(Pond1.depth)
                reportNum+=1
                fileFunctions.updateLowDepth(reportNum, Pond1.nodeid, updatedSWMM, dictOfNL)
                print("Pond(1) min depth hit at: " + str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkLowDepth(Pond2.depth, Pond2.nodeid, updatedSWMM)): 
                simLastTime=sim.current_time
                print(Pond2.depth)
                reportNum+=1
                fileFunctions.updateLowDepth(reportNum, Pond2.nodeid, updatedSWMM, dictOfNL)
                print("Pond(2) min depth hit at: " + str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkLowDepth(Pond3.depth, Pond3.nodeid, updatedSWMM)): 
                simLastTime=sim.current_time
                print(Pond3.depth)
                reportNum+=1
                fileFunctions.updateLowDepth(reportNum, Pond3.nodeid, updatedSWMM, dictOfNL)
                print("Pond(3) min depth hit at: " + str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkMaxDepth(Pond1.depth, Pond1.nodeid, updatedSWMM)):
                simLastTime = sim.current_time
                reportNum+=1
                print(Pond1.depth)
                fileFunctions.updateMaxDepth(reportNum, Pond1.nodeid, updatedSWMM, dictOfNL)
                print("Pond(1) max depth hit at: " + str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkMaxDepth(Pond2.depth, Pond2.nodeid, updatedSWMM)):
                simLastTime = sim.current_time
                reportNum+=1
                print(Pond2.depth)
                fileFunctions.updateMaxDepth(reportNum, Pond2.nodeid, updatedSWMM, dictOfNL)
                print("Pond(2) max depth hit at: " + str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkMaxDepth(Pond3.depth, Pond3.nodeid, updatedSWMM)):
                simLastTime = sim.current_time
                reportNum+=1
                print(Pond3.depth)
                fileFunctions.updateMaxDepth(reportNum, Pond3.nodeid, updatedSWMM, dictOfNL)
                print("Pond(1) max depth hit at: " + str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkMidDepth(Pond1.depth, Pond1.nodeid, updatedSWMM)):
                simLastTime = sim.current_time
                reportNum+=1
                print(Pond1.depth)
                fileFunctions.updateMidDepth(reportNum, Pond1.nodeid, updatedSWMM, dictOfNL)
                print("Pond(1) mid depth hit at: "+str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkMidDepth(Pond2.depth, Pond2.nodeid, updatedSWMM)):
                simLastTime = sim.current_time
                reportNum+=1
                print(Pond2.depth)
                fileFunctions.updateMidDepth(reportNum, Pond2.nodeid, updatedSWMM, dictOfNL)
                print("Pond(2) mid depth hit at: "+str(sim.current_time))
                sim.terminate_simulation()
            elif(fileFunctions.checkMidDepth(Pond3.depth, Pond3.nodeid, updatedSWMM)):
                simLastTime = sim.current_time
                reportNum+=1
                print(Pond3.depth)
                fileFunctions.updateMidDepth(reportNum, Pond3.nodeid, updatedSWMM, dictOfNL)
                print("Pond(3) mid depth hit at: "+str(sim.current_time))
                sim.terminate_simulation()
            simPercentComplete = sim.percent_complete
            print("Percent Complete: {:.2f}%".format(sim.percent_complete*100))
                
        if(simPercentComplete>.99):
            print("Complete")
            sim.report()
            simComplete=True
        else:
            print("RESTART")
            sim.report()
