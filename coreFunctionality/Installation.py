'''
Created on Apr 30, 2014

@author: Matthias Danzmayr
'''

import Emitter
from coreFunctionality import Logger as log
import threading
import GlobalResources as gR
from copy import deepcopy
'''
Installation Class

is the highest unit of organization of the installation
it supervises the operation of the installation:
    - assigns targets to the right emitters
    - makes sure that power constraints are not exceeded

an installation-object holds 
- registry for arrays and emitters
- methods to initiate arrays
- methods to return operation metrics
- Targets
'''
class Installation(threading.Thread):
    '''
    initiate installation object
    '''
    def __init__(self, configuration, targetCollector, logger):#, comModule):
        super(Installation, self).__init__()
        self.configuration = configuration
        self.eSpacing = 400
        self.rSpacing = 1500
        self.masters = []
        self.slaves = []
        self.comModule = comModule
        self.emitters = list()
        self.initiateEmitters()
        self.initiateEmittersPhase2()
        self.targetCollector = targetCollector
        self.trackedTargets = None #{"ID1":(1000, 650, 1000)}
        self.operating = False
        self.logger = logger
        self._stop = threading.Event()
        #self.operate()

    def getComModule(self):
        return self.comModule
    
    def run(self):
        self.operate()
    
    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    
    def initiateEmitters(self):
        for i in self.configuration.getEmitterConfig():
            self.emitters.append(list())
            for j in i:
                self.emitters[-1].append( Emitter.Emitter( self, ( j[0], j[1], j[2] ), ( j[3], j[4] ), j[5], j[6], j[7], j[8], j[9], j[10] ) )
    
    def initiateEmittersPhase2(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.determineRange()
    
    def updateEmitters(self):
            self.updateEmitterStates()     #masters are determined, states are communicated back to installation and respective unit
            self.distributeSlaves()         #invoke getSlaves in Masters
            self.invokeMasters()           #masters determine their angles and command slaves, all communicate angles back to installation and respective unit
            self.invokeSlaves()
            self.updateUnits()             #units are told to communicate new angles to arduino
    
    def updateEmitterStates(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.determineStatus()
        
    def updateUnits(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.communicateAngle()
    
    def invokeMasters(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.updateAngle(True)
                emitter.commandSlaves()
    
    def invokeSlaves(self):
        for emitterRow in self.emitters:
            for emitter in emitterRow:
                emitter.updateAngle(False)
    
    def distributeSlaves(self):
        for master in self.masters:
            master.getSlaves()
        
    def getEmitter(self, x, y):
        if not x < 0 and not y < 0:
            return self.emitters[x][y]
        else:
            raise Exception("Index below 0... fool!")
        
    '''
    register an Emitter as a MasterEmitter by putting it into the masters list
    
    if Emitter was previously registered as Slave remove from Slave list
    '''
    def registerMaster(self, emitter):
        #print "registering master"
        self.masters.append(emitter)
        try:
            self.slaves.remove(emitter)
        except:
            return

    '''
    register an Emitter as a SlaveEmitter by putting it into the slave list
    
    if Emitter was previously registered as Slave remove from Masters list
    '''
    def registerSlave(self, emitter):
        #print "registering slave"
        self.slaves.append(emitter)
        try:
            self.masters.remove(emitter)
        except:
            return

    """
    Makes all registered SlaveEmitter-objects execute the setAngle method
    no returns
    """
    def setSlaveAngles(self):
        for item in self.slaves:
            item.setAngle()

    """
    Makes all registered Emitter-objects (in masters and slaves lists) execute their actuate method
    no returns
    """
    def actuateEmitters(self):
        for item in self.masters:
            item.actuate()
        for item in self.slaves:
            item.actuate()

    """
    Returns the list of target points within the passed domain as dict(ID, point)
    """
    #def targetsInRange(self, rangeDomain):

    def getEmitterPhyLocation(self, x, y):
        #print "looking up: ["+str(x)+"]["+str(y)+"]"
        if not x < 0 and not y < 0:
            try:
                return self.emitters[x][y].getLocation()
            except IndexError:
                return False
            except:
                print "Unexpected Error while looking up emitter-location"
                return False
        else:
            return False
        
    def getESpacing(self):
        return self.eSpacing
        
    def getRSpacing(self):
        return self.rSpacing
    
    def getEmitterList(self):
        return self.emitters
    
    def operate (self):
        while not self.stopped():
            if self.obtainTargets():
                self.updateEmitters()
                gR.emitterUpdatedFlag.set()
    
    def obtainTargets(self):
        if gR.newTargetsFlag.isSet():
            gR.newTargetsFlag.clear()
            gR.lockMyTargets.acquire(1)
            try: self.trackedTargets = deepcopy(gR.myTargets)
            finally: 
                gR.lockMyTargets.release()
            return True
        else:
            return False
            
    
    def getTarget(self, targetID):
        return self.trackedTargets[targetID]

    def targetsInRange(self, eRange):
        targets = {}
        #print "range: " + str(eRange)
        for key, target in self.trackedTargets.iteritems():
            #print target
            if eRange[0] < target[0] and target[0] < eRange[1] and eRange[2] < target[1] and target[1] < eRange[3]:
                #print "True"
                targets[key] = target
            #else: #print "False"
        return targets

class EmitterStatuses(object):
    
    def __init__(self, configuration):
        self.statuses = self.generateEntries(configuration)
        
    def generateEntries(self, configuration):
        statuses = []
        i = 0
        for row in configuration.getEmitterConfig():
            j = 0
            emitterRow = []
            for emitter in row:
                emitterRow.append([configuration.getDefaultAngle(i,j), 0])
                j += 1
            statuses.append(emitterRow)
            i += 1
        return statuses
    
    def updateEmitter(self, emitter):
        emArLoc = emitter.getArrLocation()
        emStatNew = [ emitter.getState(), emitter.getAngle]
        self.statuses[emArLoc[0]][emArLoc[1]] = 
    
    def printStatuses(self):
        print self.statuses
                