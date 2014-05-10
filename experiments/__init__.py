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
"""
#input experiment

import cmd

class InstallationControll(cmd.Cmd):
   
    
    def do_w(self, person):
        Greet the named person
        if person:
            print "hi,", person
        else:
            print 'hi'
    
    def do_EOF(self, line):
        return True
    
    def postloop(self):
        print

if __name__ == '__main__':
    InstallationControll().cmdloop()
    print "done"
"""



"""
#shared resources experiment

import threading
import time
import DataGen
import globalVars as gv

class Printer(threading.Thread):
    
    def __init__(self, data):
        super(Printer, self).__init__()
        self.data = data
        
    def run(self):
        while 1:
            gv.dataLock.acquire(1)
            try:
            
                print self.data
            finally:
                gv.dataLock.release()
                    
            if gv.dataFlag.isSet():
                return


dataGenThread = DataGen.DataGen(gv.data)
printThread = Printer(gv.data)

printThread.start()
dataGenThread.start()

printThread.join()
dataGenThread.join()
print "done"
"""
"""
#csv-write Experiment
import csv
with open('eggs.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

"""
"""
#MAIN
from coreFunctionality import Configuration
from coreFunctionality import Installation
#import comModule...
from output import GUInterface
from output import Logger
import threading
import time
from coreFunctionality import cascade

#updateGUI = threading.Event()
#emitterStates_lock = threading.Lock()

myConfig = Configuration.Configuration("config.csv")
myLogger = Logger.Logger()
myComModule = cascade.EmitterDriver()
myInstallationThread = Installation.Installation(myConfig, myLogger, myComModule)
myLogger.obtainEmitterList(myInstallationThread.getEmitterList())
# copy the data from the emitter data structures into the servo/bulb data structures
servos = []
bulbs = []
for emitterArray in myInstallationThread.getEmitterList():
    for emitter in emitterArray:
        servos.append(cascade.Servo(int(emitter.servoPin), int(emitter.servoArduinoID), 90))
        #bulbs.append()
ports = []
ports.append(cascade.Port(0, '/dev/tty.usbmodem14141', False))
#ports.append(cascade.Port(1, '/dev/tty.usbmodem141341', False))
myComModule.initialize(servos, bulbs, ports)
for servo in myComModule.servos:
    print "pin: " + str(servo.pin) + " port:" + str(servo.port)
#time.sleep(100)
myInstallationThread.start()
time.sleep(1)
myInstallationThread.stop()
print "stop issued"
myInstallationThread.join()
print "done"

"""
