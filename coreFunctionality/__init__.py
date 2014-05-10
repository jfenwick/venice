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
"""
#Version 2

import Configuration as con
import Installation as ins
import GlobalResources as gR
import Logger as log
import TargetAcquisition as tA
import time
import cascade

paths = []
# mac path tends to look like this:
paths.append('/dev/tty.usbmodem1411')
# windows path tends to look like this:
# paths.append(10)

myConfig = con.Configuration("config.csv")

gR.myEStats = ins.EmitterStatuses(myConfig)

myInstallationThread = ins.Installation(myConfig)
myTargetAcquisitionThread = tA.FakeData()
myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, paths)
time.sleep(1)
print 'started communication thread'

myInstallationThread.start()
myCommunicationThread.start()
myTargetAcquisitionThread.start()

myTargetAcquisitionThread.join()
myInstallationThread.stop()
myCommunicationThread.stop()
myInstallationThread.join()
myCommunicationThread.join()

#gR.myEStats.printStatuses()

print "done"
"""


#Version 3

import Configuration as con
import Installation as ins
import GlobalResources as gR
import Logger as log
import TargetAcquisition as tA
import time
import commandClasses as cC
import cascade

if __name__ == '__main__':
    paths = []
    # mac path tends to look like this:
    paths.append('/dev/tty.usbmodem1411')
    # windows path tends to look like this:
    # paths.append(10)
    myConfig = con.Configuration("tiny.csv")
        
    gR.myEStats = ins.EmitterStatuses(myConfig)
    
    myInstallationThread = ins.Installation(myConfig)
    myCommunicationThread = cascade.ArduinoDriver(gR.myEStats, paths)
    
    
    myTargetAcquisitionThread = tA.FakeData()
    
    myInstallationThread.start()
    myCommunicationThread.start()

    cC.ManualControl().cmdloop()
    
    myTargetAcquisitionThread.start()
    myTargetAcquisitionThread.join()
    myInstallationThread.stop()
    myCommunicationThread.stop()
    myInstallationThread.join()
    myCommunicationThread.join()
    
    print "done"
