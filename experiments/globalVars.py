'''
Created on May 8, 2014

@author: Matthias
'''
import threading

dataLock = threading.Lock()
dataFlag = threading.Event()
data = []