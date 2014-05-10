'''
Created on May 9, 2014

@author: Matthias
'''
import cmd
import GlobalResources as gR
import time

class ManualControl(cmd.Cmd):
    '''
    Class to achieve manual control over an Installation
    '''
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.selectedEmitter = None
    
    def do_sel(self, arrLoc):
        try: self.selectedEmitter = (int(arrLoc[0]),int(arrLoc[1]))
        except: print "selection failed"
        else: print "selection of emitter ", self.selectedEmitter, " successful"
      
    def do_w(self, angle):
        if angle:
            self.issueCommand(abs(float(angle))) 
        else:
            self.issueCommand(1.0) 
        
    def do_s(self, angle):
        if angle:
            self.issueCommand(-1 * abs(float(angle))) 
        else:
            self.issueCommand(-1) 
    
    def do_EOF(self, line):
        return True
    
    def do_saveConfig(self, filename):
        gR.saveConfigFlag.set()
        if filename:
            gR.lockSaveConfigFilename.acquire(1)
            gR.saveConfigFilename = 'filename'
            gR.lockSaveConfigFilename.release()
            
    
    def issueCommand(self, angle):
        '''
        issues a command to rotate the selected emitter by angle
        '''
        if self.selectedEmitter:
            if not gR.newCommandFlag.isSet():
                gR.lockDirectCommand.acquire(1)
                gR.directCommand = (self.selectedEmitter, angle)
                gR.newCommandFlag.set()
                gR.lockDirectCommand.release()
                time.sleep(0.01)
                print "command issued to emitter ", self.selectedEmitter, " moved by ", angle
            else:
                print "command failed, flag set"
        else:
            print "command failed, no emitter selected"