'''
Created on May 8, 2014

@author: Matthias
'''
import threading
import GlobalResources as gR
import time

class FakeData(threading.Thread):



    def __init__(self):

        super(FakeData, self).__init__()
        
    def run(self):
        """
        #fakeData1
        gR.lockMyTargets.acquire(1)
        gR.myTargets = {1:[500,500,1200]}
        gR.lockMyTargets.release()
        gR.newTargetsFlag.set()
        
        time.sleep(2)
        gR.lockMyTargets.acquire(1)
        gR.myTargets = {1:[500,1500,1200]}
        gR.lockMyTargets.release()
        gR.newTargetsFlag.set()
        
        time.sleep(2)
        gR.lockMyTargets.acquire(1)
        gR.myTargets = {1:[500,2500,1200]}
        gR.lockMyTargets.release()
        gR.newTargetsFlag.set()
        """
        
        #fakeData2
        for i in range(1):
            gR.lockMyTargets.acquire(1)
            gR.myTargets = {}#1:[-1500+i*10,1000,1200], 2:[900,0+i*10,1200], 3:[3600-i*5,3000-i*4,1200] }
            gR.lockMyTargets.release()
            gR.newTargetsFlag.set()
            
            time.sleep(0.01)
            