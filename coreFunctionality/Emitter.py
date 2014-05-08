'''
Created on May 1, 2014

@author: Matthias
'''

import VectorMath as vm
import math
import GlobalResources as gR

class Emitter(object):
    
    def __init__(self, installation, phyLocation, arrLocation, defaultAngle, maxTilt, servoArduinoID, servoPin, relayArduinoID, relayPin ):
        self.phyLocation = phyLocation          #coorinates of physical location
        #print "initiating emitter at: " + str(self.phyLocation)
        self.arrLocation = arrLocation          #coordinates in emitterArray
        self.angle = 0
        self.defaulAngle = defaultAngle         #pre-configured default servo-position
        self.installation = installation        #parent installation-object
        self.relayArduinoID = relayArduinoID
        self.servoArduinoID = servoArduinoID
        self.relayPin = relayPin
        self.servoPin = servoPin
        self.state = 0                           #TRUE for master, FALSE for slave
        #self.range = self.determineRange()       #list of (xMin, xMax, yMin, yMax)
        self.target = None                      #key of tracked target in installation's target dictionary
        self.influence = 2
        self.slaves = None
        self.commands = []
        self.bulbActive = False
        self.secondaryTarget = None
        self.rangeExtension = self.installation.getRSpacing()
        
    """
    checks for targets in range
    sets state
    communicates state to installation
    """
    def determineStatus(self):
        #print "determining status of emiiter " + str(self.arrLocation)
        #retrieve targets in emitter-range from installation as dictionary
        trackedTargetsInRange = self.installation.targetsInRange(self.range)
        #print "targets in Range: " + str(trackedTargetsInRange)
        #print "emitter-range: " +str(self.range)
        
        if trackedTargetsInRange:
            #emitter has targets in range
            
            if self.target != None and trackedTargetsInRange.has_key(self.target):
                #emitter was already tracking a target and that target is still in its range
                return
                
            else:
                #emitter was not tracking before but has targets in Range
                
                self.target = self.determineClosestTarget(trackedTargetsInRange)
                self.beMaster()
                
        else:
            extRange = [ self.range[0] - self.rangeExtension, self.range[1] + self.rangeExtension, self.range[2], self.range[3]  ]
            #print "Range = " + str(self.range)
            #print "extRange = " + str(extRange)
            trackedTargetsInExtRange = self.installation.targetsInRange(extRange)
            
            if trackedTargetsInExtRange:
                #print "target in ext range"
                self.secondaryTarget = self.determineClosestTarget(trackedTargetsInExtRange)
                self.beMaster()
            else:
                #no targets in range
            
                self.beSlave()
        #print "emitter is " + str(self.state)
        self.communicateState()
    
    def targetXDistance(self, targetID):
        return float(self.installation.getTarget(targetID)[0]) - float(self.phyLocation[0])
    
    """
    determine which slaves are influenced by master-emitter
    """
    def getSlaves(self):
        #print "looking for slaves"
        self.slaves = list()
        x=int(self.arrLocation[0])
        y=int(self.arrLocation[1])
        #path 1 
        i=0
        while i < self.influence:
            i += 1
            
            try: 
                slaveCandidate = self.installation.getEmitter(x,y-i)
            except:
                break
            
            if not slaveCandidate.isMaster():
                self.slaves.append(slaveCandidate)
            else:
                break
                
        #path 2
        i=0
        while i < self.influence:
            i += 1
            
            try: 
                slaveCandidate = self.installation.getEmitter(x,y+i)
            except:
                break
            
            if not slaveCandidate.isMaster():
                self.slaves.append(slaveCandidate)
            else:
                break       

    """
    targetList is a dictionary of targets k = targetID v = point
    returns ID/key of closest Point
    """
    def determineClosestTarget(self, targetList):
        distances = {}
        for key in targetList.keys():
            distances[key] = vm.getPointDistance(self.phyLocation, targetList[key])
        
        return min(distances, key=distances.get)
        
    def isMaster(self):
        return self.state
        
    def determineRange(self):
        #print "determining range of " + str(self.arrLocation)
        myArrX = int(self.arrLocation[0])
        myArrY = int(self.arrLocation[1])
        myPhyX = int(self.phyLocation[0])
        myPhyY = int(self.phyLocation[1])
        
        minXLoc = self.installation.getEmitterPhyLocation( myArrX - 1, myArrY )
        if not minXLoc:
            minX = myPhyX - self.installation.getRSpacing()
        else:
            minX = minXLoc[0]
            
        maxXLoc = self.installation.getEmitterPhyLocation( myArrX + 1, myArrY )
        if not maxXLoc:
            maxX = myPhyX + self.installation.getRSpacing()
        else:
            maxX = maxXLoc[0]
            
        minYLoc = self.installation.getEmitterPhyLocation( myArrX, myArrY - 1 )
        if not minYLoc:
            minY = myPhyY - self.installation.getESpacing()
        else:
            minY = minYLoc[1]
        
        maxYLoc = self.installation.getEmitterPhyLocation( myArrX, myArrY + 1 )
        if not maxYLoc:
            maxY = myPhyY + self.installation.getESpacing()
        else:
            maxY = maxYLoc[1]
        
        self.range = (int(minX), int(maxX), int(minY), int(maxY))
        #print "self.arrLocation = " + str(self.arrLocation)
        #print "self.range = " + str(self.range)
        
    def updateAngle(self, masterOrSlave):
        if not masterOrSlave == self.state:
            return
        
        if self.state:
            if self.target:
                self.angle = self.angleToTarget(self.installation.getTarget(self.target))
            elif self.secondaryTarget:
                distance = self.targetXDistance(self.secondaryTarget)
                #print "distance " + str(distance)
                maxAngle = abs(self.angleToTarget( [ float(self.range[1])-float(self.phyLocation[0]),0, 1000 ] ))
                #print "maxAngle = " + str(vm.radToDeg(maxAngle))
                if distance > 0:
                    relevantRange = self.range[1]
                    outOfRange = distance - relevantRange
                    self.angle = vm.mapToDomain(outOfRange, 0, abs(relevantRange), maxAngle, 0)
                elif distance < 0:
                    relevantRange = self.range[0]
                    outOfRange = distance + relevantRange
                    #print "oor " + str(outOfRange)
                    
                    self.angle = vm.mapToDomain(outOfRange, 0, -1 * float(abs(relevantRange)), -1 * float(maxAngle), 0)
                else:
                    raise Exception("Evil's afoot!")
                
                
        elif not self.state:
            i = 0
            comComb = 0
            for command in self.commands:
                comComb += command
                i += 1
            if i == 0:
                self.angle = 0
            else:
                self.angle = comComb/i
        #print "angle: " + str(self.angle)
                                            
    def commandSlaves(self):
        #print "slave commanded"
        if self.state:
            #print "slave commanded2"
            for slave in self.slaves:
                #print "slave commanded3"
                slave.receiveCommand(self.angle, self.arrLocation)
    
    def receiveCommand(self, angle, origin):
        #print "command received"
        self.commands = []
        distance = abs(int(self.arrLocation[0]) - int(origin[0])) + abs(int(self.arrLocation[1]) - int(origin[1]))
        self.commands.append(angle * self.commandEffect(distance))
    
    def commandEffect(self, distance):
        effect = (math.sin((self.influence/2+distance)*math.pi/self.influence)/2+0.5)
        if effect < 0.03:
            effect = 0
        return effect
    
    #def communicateStatus(self):
    
    def angleToTarget(self, target):
        target3D = target
        target2D = (int(target3D[0]), int(target3D[2]))
        location2D = (int(self.phyLocation[0]), int(self.phyLocation[2]))
        
        targetVector = vm.createVector(location2D, target2D)
        
        targetAngle = vm.angleBetween2D([0,-1], targetVector)
        return targetAngle
        
    def beSlave(self):
        self.commands = []
        if self.state:
            self.state = False
            
    def beMaster(self):
        self.commands = []
        if not self.state:
            self.state = True
        
        if self.target:
            if not self.bulbActive:
                self.bulbActive = True
    
    def getBulbState(self):
        return self.bulbActive
    
    def getLocation(self):
        return self.phyLocation
    
    def getArrLocation(self):
        return self.arrLocation
    
    def communicateState(self):
        if self.state:
            self.installation.registerMaster(self)
        else:
            self.installation.registerSlave(self)

    def communicateAngle(self):
        gR.myEStats.updateEmitter(self)
        #self.installation.logger.receiveState(self)
        #self.installation.getComModule().updateEmitter(self.servoArduinoID, self.relayArduinoID, self.servoPin, self.relayPin, self.state, self.angle)
    
    def getState(self):
        return self.state
    
    def getAngle(self):
        return self.angle