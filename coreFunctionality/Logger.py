'''
Created on May 4, 2014

@author: Matthias
'''
import math
import threading
import GlobalResources as gR
from copy import deepcopy
import csv

class Logger(threading.Thread):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        super(Logger, self).__init__()
        #self.emitterStates = None
        self._stopFlag = threading.Event()
        gR.emitterUpdatedFlag.set()
        
    def run(self):
        while not self._stopFlag.isSet():
            if gR.emitterUpdatedFlag.isSet():
                gR.emitterUpdatedFlag.clear()
                oList = self.createOrederedList(gR.myEStats)
                self.printArray(oList)
                self.writeEmitterFile(oList)
                self.writeTargetFile()
    
    def stop(self):
        self._stopFlag.set()
    
    def writeTargetFile(self):
        gR.lockMyTargets.acquire()
        targets = deepcopy(gR.myTargets)
        gR.lockMyTargets.release()
        #print targets.values()
        try:
            with open('targets.csv', 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in targets.values():
                    spamwriter.writerow(row)
        except:
            print "file write error, targets"
            
    def writeEmitterFile(self, orderedList):
        try:
            with open('eStats.csv', 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in orderedList:
                    nextRow = []
                    for emitter in row:
                        nextRow.append( emitter[1] )
                    spamwriter.writerow(nextRow)
        except:
            print "file write error"
            
    def createOrederedList(self, emitterStatuses):
        gR.lockMyEstates.acquire(1)
        statusDic = deepcopy(emitterStatuses.getStatuses())
        gR.lockMyEstates.release()
        orderedList = [[]]
        row = 0
        column = 0
        fails = 0
        while 1:
            emitterStats = statusDic.get( ( int(row), int(column) ) )
            if emitterStats == None:
                if fails<2:
                    fails += 1
                    row += 1
                    column = 0
                    newRow = []
                    orderedList.append( newRow )
                else: 
                    orderedList.pop(-1)
                    orderedList.pop(-1)
                    break
            else:
                fails = 0
                orderedList[row].append( [ emitterStats[-2], emitterStats[-1] ] )
                column += 1
                
        return orderedList
    
    def printArray(self, orderedList):
                
        printString =  "printing states:\n"
        for emitterRow in orderedList:
            printString += (10*len(emitterRow)+1)*"-" + "\n"
            entry = ""
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.2f}".format(float(emitterRow[i][1])).rjust(8, " ")+" "
            entry += "|\n"
            entry += (10*len(emitterRow)+1)*"-"+"\n"
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.0f}".format(emitterRow[i][0]).center(9, " ")
            entry += "|\n"
            printString += entry
            printString += (10*len(emitterRow)+1)*"-"+"\n\n"
        print printString

        
        
        
        
        try:
            with open('eStats.csv', 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in orderedList:
                    nextRow = []
                    for emitter in row:
                        nextRow.append( emitter[1] )
                    spamwriter.writerow(nextRow)
        except:
            print "file write error"