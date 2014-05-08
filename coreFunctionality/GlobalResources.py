'''
Created on May 8, 2014

@author: Matthias
'''

import threading

myEStats = None
lockMyEstates = threading.Lock()
myTargets = None
lockMyTargets = threading.Lock()
newTargetsFlag = threading.Event()
emitterUpdatedFlag = threading.Event()