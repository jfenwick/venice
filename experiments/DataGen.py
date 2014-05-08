'''
Created on May 8, 2014

@author: Matthias
'''
import threading
import globalVars as gv

class DataGen(threading.Thread):
    
    def __init__(self, data):
        super(DataGen, self).__init__()
        self.data = data
        
    def run(self):
        i=0
        while i < 20:
            gv.dataLock.acquire(1)
            try:
                self.data.append("1")
            finally:
                gv.dataLock.release()
            i += 1
        gv.dataFlag.set()