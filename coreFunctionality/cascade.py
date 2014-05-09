import glob
import operator
import serial
import sys
import time
import threading
import GlobalResources as gR
from copy import deepcopy

'''
Device
id_num - id as specified in config
path - path to the device on the os, also specified in config
port - open serial port connection
'''
class Device:
	def __init__(self, id_num, path):
		self.id_num = id_num
		self.path = path

class ArduinoDriver(threading.Thread):
	def __init__(self, emitters, paths):
		super(ArduinoDriver, self).__init__()
		# indexes to device paths
		self.devices = []
		self.last_update_time = time.clock()

		for i,path in enumerate(paths):
			self.devices.append(Device(i, path))

		self.data_store = []

		# architecture of data_store
		# list of devices (arduinos)
		# each index of list contains a dictionary
		# dictionary contains keys, which are pins
		# values of dictionary are angle/state
		# example:
		#[{pin:angle}, {pin:state}, {pin:angle}, {pin:state}, ...]
		for path in paths:
			self.data_store.append({})

		self.unwrapEmitters(emitters.getStatuses())
		self.open_ports()
        self._stopFlag = threading.Event()

	def run(self):
        while not self._stopFlag.isSet():
			if gR.emitterUpdatedFlag.isSet():
				gR.emitterUpdatedFlag.clear()
				self.unwrapEmitters(gR.myEStats.getStatuses())
				#time.sleep(1)
				self.updateArduinos()

	def stop(self):
		self.close_ports()
        self._stopFlag.set()

	def unwrapEmitters(self, wrapped_emitters):
		emitters = []
		for i,emitter in enumerate(wrapped_emitters.itervalues()):
			emitters.append(emitter)
		self.updateEmitters(emitters)

	def updateEmitters(self, emitters):
		servoArduinoIndex = 0
		bulbArduinoIndex = 1
		servoPinIndex = 2
		bulbPinIndex = 3
		stateIndex = 4
		angleIndex = 5

		# fill the data_store with emitters
		for e in emitters:
			angle = int(e[angleIndex])
			angle = 90 + angle
			# constrain the servo angle, just in case
			if angle > 135:
				angle = 135
			elif angle < 45:
				angle = 45
			tmp = self.data_store[int(e[servoArduinoIndex])]
			tmp[int(e[servoPinIndex])] = angle

	def updateArduinos(self):
		# if enough time has elapsed since the last update, update arduinos
		elapsed = (time.clock() - self.last_update_time)
		if elapsed > 2:
			print 'data_store:'
			print self.data_store
			print 'devices:'
			print self.devices
			for device,datum in zip(self.devices,self.data_store):
				serial_data = ''
				sorted_data = sorted(datum.iteritems(), key=operator.itemgetter(0))
				for data in sorted_data:
					serial_data = serial_data + str(data[1]).zfill(3)
				serial_data = serial_data + "\0"
				device.port.write(serial_data)
				print serial_data

			self.last_update_time = time.clock()
			#time.sleep(3)

	# looks for all devices that have the same name pattern as an Arduino and opens them
	def open_ports(self):
		# find arduinos
		# note: currently this is Mac only
		found_ports = glob.glob('/dev/tty.usbmodem*')

		if len(found_ports) == 0:
			print "No Arduinos found"
			#sys.exit(1)

		if len(self.devices) != len(found_ports):
			print "Number of found Arduinos does not match configured number"
			#sys.exit(1)

		print 'found ports:'
		for found_port in found_ports:
			print found_port
			try:
				for device in self.devices:
					if device.path == found_port:
						# connect to serial port
						print 'assigning port'
						device.port = serial.Serial(found_port, 9600)
						break
			except:
				print 'Failed to open port'
		# need a short delay right after serial port is started for the Arduino to initialize
		#time.sleep(1)

	def close_ports(self):
		print 'closing ports'
		for device in self.devices:
			device.port.close()

if __name__ == "__main__":
	pass
	'''
	paths = []
	paths.append('/dev/tty.usbmodem14141')

	num_emitters = 3
	emitters = []

	for i in range(0, num_emitters):
		emitters.append([0, 1, i+2, i+2, 0, 45])

	print 'getting thread'
	driverThread = ArduinoDriver(emitters, paths)
	print 'got thread'
	try:
		print 'in the try'
		if matdan:
			emitters = {(1, 3): ['0', '1', '2', '2', 1, 45], (2, 8): ['0', '1', '3', '3', 0, -45], (3, 8): ['0', '1', '4', '4', 0, -45]}
		else:
			for i in range(0, num_emitters):
				if i % 2 == 0:
					emitters.append([0, 1, i+2, i+2, 0, 45])
				else:
					emitters.append([0, 1, i+2, i+2, 0, -45])
		print 'assigning emitters'
		gr.myEStats = emitters
		print 'assigned emitters'

		print 'opening ports'
		driverThread.open_ports()
		sleep(10)
		driverThread.run()
			
		time.sleep(2)
		print 'entering loop'

		#while True:
		#	if matdan:
		#		driver.unwrapEmitters(emitters)
		#	else:
		#		driver.updateEmitters(emitters)
		#	driver.updateArduinos()
	except:
		print "Unexpected error:", sys.exc_info()[0]
	finally:
		driverThread.close_ports()
	'''