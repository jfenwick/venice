"""
#Version1
import Configuration
import Installation
#import comModule...
from output import GUInterface
from output import Logger
import threading
import time

myConfig = Configuration.Configuration("../config.csv")
myLogger = Logger.Logger()
#myComModule = #fill in the blanks
myInstallationThread = Installation.Installation(myConfig, myLogger)#, myComModule)
myLogger.obtainEmitterList(myInstallationThread.getEmitterList())
myInstallationThread.start()
time.sleep(1)
myInstallationThread.stop()
print "stop issued"
myInstallationThread.join()
print "done"
"""

#Version 2

import Configuration as con
import Installation as ins
import GlobalResources as gR
import Logger

myConfig = con.Configuration("../config.csv")
    
gR.myEStats = ins.EmitterStatuses(myConfig)

myInstallationThread
myTargetAcquisitionThread
myCommunicationThread



