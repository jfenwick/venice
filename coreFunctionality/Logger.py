'''
Created on May 4, 2014

@author: Matthias
'''
import math

class Logger(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.emitterStates = None
        
    
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
        
    def printArray(self, emitterStates):
        print "printing states:"
        for emitterRow in emitterStates:
            print (10*len(emitterRow)+1)*"-"
            entry = ""
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.2f}".format(self.radToDeg(emitterRow[i][1])).rjust(8, " ")+" "
            entry += "|\n"
            entry += (10*len(emitterRow)+1)*"-"+"\n"
            for i in range(len(emitterRow)):
                entry += "|" + "{0:.0f}".format(emitterRow[i][0]).center(9, " ")
            entry += "|"
            print entry
            print (10*len(emitterRow)+1)*"-"+"\n"
            
    def radToDeg(self, angle):
        return angle * 180 / math.pi
            
            
            
        
        