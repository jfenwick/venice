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
        self.eSpacing = 400
        self.rSpacing = 1500
        self.config = self.readConfig(filename)
        self.emitterParams = 11
        self.emitterConfig = [ [ [ row[i] for row in self.config[ j*self.emitterParams:j*self.emitterParams+self.emitterParams ] ] for i in range( len( self.config[ j * self.emitterParams ] ) ) ] for j in range( len( self.config ) / self.emitterParams ) ]

    def readConfig(self, filename):
        #print "start to read file: " + filename
        configFile = open(filename)
        configReader = csv.reader(configFile)
        configArray = list()
        for row in configReader:
            configArray.append(row)
        return configArray
        
    def getEmitterConfig (self):
        return self.emitterConfig
    
    def getDefaultAngle(self, x, y):
        return self.emitterConfig[x][y][5]
    
    def getESpacing(self):
        return self.eSpacing
    
    def getRSpacing(self):
        return self.rSpacing