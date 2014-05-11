'''
Created on May 8, 2014

@author: Matthias
'''

import threading
import GlobalResources as gR

myEStats = None
lockMyEstates = threading.Lock()
myTargets = None
lockMyTargets = threading.Lock()
newTargetsFlag = threading.Event()
emitterUpdatedFlag = threading.Event()

directCommand = {}
lockDirectCommand = threading.Lock()
newCommandFlag = threading.Event()

saveConfigFlag = threading.Event()
saveConfigFilename = 'config.csv'
lockSaveConfigFilename = threading.Lock()