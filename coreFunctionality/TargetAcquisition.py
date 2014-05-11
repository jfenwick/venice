'''
Created on May 8, 2014

@author: Matthias
'''
import threading
import GlobalResources as gR
import time
import socket   #for sockets
import sys  #for exit

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

class SensorData(threading.Thread):
    def __init__(self):
        super(SensorData, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip='128.30.79.98'
        port = 7000
        s.connect((remote_ip , port))
        print 'Connected'
        self._stopFlag = threading.Event()

    def run(self):
        while not self._stopFlag.isSet():
            gR.lockMyTargets.acquire(1)
            try:
                gR.newTargetsFlag.set()
                self.update_targets(gR.myTargets)
            finally:
                gR.lockMyTargets.release()

    def stop(self):
        self._stop.set()

    def update_targets(targets):
        reply = s.recv(19)