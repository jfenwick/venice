'''
Created on May 1, 2014

@author: Matthias
'''

import csv

class Configuration(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        '''
        Constructor
        '''
        self.eSpacing = 235
        self.rSpacing = 1829
        self.emitterParams = 12
        self.loadConfig(filename)
        
    def createEmitterConfig(self, config):
        ml = [config[i:i+self.emitterParams] for i in range(0, len(config), self.emitterParams)] 
        ml = [map(list, zip(*row)) for row in ml]
        ml2 = []
        for row in ml:
            newRow = []
            for emi in row:
                if not '' in emi:
                    newRow.append(emi)
            if len(newRow) > 0:
                ml2.append(newRow)
        
        return ml2
        
    def readConfig(self, filename):
        #print "start to read file: " + filename
        configFile = open(filename)
        configReader = csv.reader(configFile)
        configArray = list()
        for row in configReader:
            configArray.append(row)
        #print configArray
        return configArray
        
    def getEmitterConfig (self):
        return self.emitterConfig
    
    def getDefaultAngle(self, x, y):
        return self.emitterConfig[x][y][5]
    
    def getESpacing(self):
        return self.eSpacing
    
    def getRSpacing(self):
        return self.rSpacing
    
    def updateDefaultAngle(self, arrLoc, newDefAng):
        self.emitterConfig[int(arrLoc[0])][int(arrLoc[1])][5] = newDefAng
    
    def writeConfig(self, filename):
        outputList = []
        print self.emitterConfig
        
        for h, row in enumerate(self.emitterConfig):
            for i in range(self.emitterParams):
                outputList.append([])
                
                #for emitter in row:
                    #outputList[-1].append('')
                    
            for emitter in row:
                print "emitter ",emitter
                
                for i, param in  enumerate(emitter):
                    outputList[h*self.emitterParams+i].append(param)
                
                
        
        with open(filename, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in outputList:
                spamwriter.writerow(row)
                
    def loadConfig(self, filename):
        self.config = self.readConfig(filename)
        self.emitterConfig = self.createEmitterConfig(self.config)
        