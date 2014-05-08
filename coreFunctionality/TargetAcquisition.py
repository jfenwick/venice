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
        for i in range(50):
            gR.lockMyTargets.acquire(1)
            gR.myTargets = {1:[100+i*100,1500,1200]}
            gR.lockMyTargets.release()
            gR.newTargetsFlag.set()
            
            time.sleep(0.2)
            