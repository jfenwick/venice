import socket   #for sockets
import sys  #for exit
import GlobalResources as gR

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
			if gR.newTargetsFlag.isSet():
				gR.newTargetsFlag.clear()
				self.update_targets(gR.myTargets)

	def update_targets(targets)
		reply = s.recv(19)