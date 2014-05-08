'''
Created on May 4, 2014

@author: Matthias
'''
import math
import threading
import GlobalResources as gR

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
        
    def run(self):
        while not self._stopFlag.isSet():
            if gR.emitterUpdatedFlag.isSet():
                gR.emitterUpdatedFlag.clear()
                #gR.lockMyEstates.acquire(1)
                self.printArray(gR.myEStats)
                #gR.lockMyEstates.release()
    
    def stop(self):
        self._stopFlag.set()
        
    def obtainEmitterList(self, emitterList):
        self.emitterStates = self.createEmitterList(emitterList)
    
    def getEmitterList(self):
        return self.emitterStates
    
    def createEmitterList(self, emitterList):
        emitterStates = list()
        for i in range(len(emitterList)):
            emitterStates.append(list())
            for j in range(len(emitterList[i])):
                emitterStates[i].append( [0,0] )
        return emitterStates
        
    def receiveState(self, emitter):
        state = [ int(emitter.getState()) + int(emitter.getBulbState()), emitter.getAngle() ]
        self.emitterStates[ int( emitter.getArrLocation()[0] ) ][ int( emitter.getArrLocation()[1] ) ] = state
        
    def printArray(self, emitterStatuses):
        gR.printLock.acquire()
        print "printing states:"
        for emitterRow in emitterStatuses.getStatuses():
            print (10*len(emitterRow)+1)*"-"
            entry = ""
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.2f}".format(self.radToDeg(float(emitterRow[i][1]))).rjust(8, " ")+" "
            entry += "|\n"
            entry += (10*len(emitterRow)+1)*"-"+"\n"
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.0f}".format(emitterRow[i][0]).center(9, " ")
            entry += "|"
            print entry
            print (10*len(emitterRow)+1)*"-"+"\n"
        gR.printLock.release()
            
    def radToDeg(self, angle):
        return angle * 180 / math.pi
            
            
            
        
        