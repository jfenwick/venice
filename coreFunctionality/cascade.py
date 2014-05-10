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
		self.arduino_delay = 0.0

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
			# store the servo and bulb data in our complex data array
			servoArduinoId = int(e[servoArduinoIndex])
			servoPin = int(e[servoPinIndex])
			tmp = self.data_store[servoArduinoId]
			tmp[servoPin] = angle

			#bulbArduinoId = int(e[bulbArduinoIndex])
			#bulbPin = int(e[bulbPinIndex])
			#tmp = self.data_store[bulbArduinoId]
			#tmp[bulbPin] = int(stateIndex)

	def updateArduinos(self):
		# if enough time has elapsed since the last update, update arduinos
		elapsed = (time.clock() - self.last_update_time)
		if elapsed > self.arduino_delay:
			print 'data_store:'
			print self.data_store
			print 'devices:'
			print self.devices
			# iterate over arduinos to send data to
			for device,datum in zip(self.devices,self.data_store):
				serial_data = ''
				sorted_data = sorted(datum.iteritems(), key=operator.itemgetter(0))
				# the string of data sent over serial
				# states and angles are padded to 3 spaces
				for data in sorted_data:
					serial_data = serial_data + str(data[1]).zfill(3)
				serial_data = serial_data + "\0"
				# send the data to an arduino
				device.port.write(serial_data)
				print serial_data

			# update the clock if you need a delay
			self.last_update_time = time.clock()

	# opens all the arduinos as configured in __init__.py
	def open_ports(self):
		print 'opening ports'
		for device in self.devices:
			device.port = serial.Serial(device.path, 9600)

	# close all the arduinos
	def close_ports(self):
		print 'closing ports'
		for device in self.devices:
			device.port.close()