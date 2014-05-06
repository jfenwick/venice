"""
from  coreFunctionality import Configuration

configuration = Configuration('config.csv')
print configuration.getEmitterConfig()
"""
"""
from coreFunctionality import Configuration as cF

myConfig = cF.Configuration('../config.csv')

print myConfig.getEmitterConfig()
"""
"""
def testFunction (x):
    y = ( 1, 2, 3)
    return y[x]


try:
    print testFunction(3)
except:
    print 'exception'
"""
"""
import math
from coreFunctionality import VectorMath as vm

print vm.angleBetween2D((1,0),(2,-0.1))
print math.pi * 1.5 + math.atan(2/0.1)
print vm.angle2DVector((2,-0.0001))
print math.pi
"""
"""
num = 123341
print num
num = "{0:.2f}".format(num)
print num
"""

"""
def printArray(emitterStates):
    for emitterRow in emitterStates:
        print (10*len(emitterRow)+1)*"-"
        entry = ""
        for i in range(len(emitterRow)):
            entry += "|" + "{0:.2f}".format(emitterRow[i][1]).rjust(8, " ")+" "
        entry += "|\n"
        entry += (10*len(emitterRow)+1)*"-"+"\n"
        for i in range(len(emitterRow)):
            entry += "|" + "{0:.0f}".format(emitterRow[i][0]).center(9, " ")
        entry += "|"
        print entry
        print (10*len(emitterRow)+1)*"-"+"\n"

myList = ( ( (0, 14.2324), (0, -12), (1, 12.1), (0, -12), (1, 12.1), (0, -12), (1, 12.1) ), ( (0, 14.2324), (0, 12), (1, 12.1), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12) ) )

printArray(myList)
"""
"""
import Tkinter as tk
import time

root = tk.Tk()

var = tk.StringVar()
var.set("fgh")

status = tk.Label(root, textvariable = var)
status.pack()
root.update()
time.sleep(3)
var.set("asd")
root.update()
"""

#MAIN
from coreFunctionality import Configuration
from coreFunctionality import Installation
#import comModule...
from output import GUInterface
from output import Logger
import threading
import time

#updateGUI = threading.Event()
#emitterStates_lock = threading.Lock()

myConfig = Configuration.Configuration("../config.csv")
myLogger = Logger.Logger()
myComModule = #fill in the blanks
myInstallationThread = Installation.Installation(myConfig, myLogger, myComModule)
myLogger.obtainEmitterList(myInstallationThread.getEmitterList())
myInstallationThread.start()
#myInstallation.stopOperation()
#time.sleep(5)
#myInstallationThread.stop()
#print "stop issued"
#myInstallationThread.join()
#print "done"

