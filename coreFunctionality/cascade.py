import glob
import operator
import serial
import sys
import time

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

class ArduinoDriver:
	def __init__(self, emitters, paths):
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
			angle = e[angleIndex]
			angle = 90 + angle
			# constrain the servo angle, just in case
			if angle > 135:
				angle = 135
			elif angle < 45:
				angle = 45
			# ew
			self.data_store[e[servoArduinoIndex]][e[servoPinIndex]] = e[angleIndex]

	def updateArduinos(self):
		# if enough time has elapsed since the last update, update arduinos
		elapsed = (time.clock() - self.last_update_time)
		if elapsed > 0.05:
			for device,datum in zip(self.devices,self.data_store):
				serial_data = ''
				sorted_data = sorted(datum.iteritems(), key=operator.itemgetter(0))
				for data in sorted_data:
					serial_data = serial_data + str(data[1]).zfill(3)
				serial_data = serial_data + "\0"
				#print serial_data
				device.port.write(serial_data)


			self.last_update_time = time.clock()
			time.sleep(3)

	# looks for all devices that have the same name pattern as an Arduino and opens them
	def open_ports(self):
		# find arduinos
		# note: currently this is Mac only
		found_ports = glob.glob('/dev/tty.usbmodem*')

		if len(found_ports) == 0:
			print "No Arduinos found"
			sys.exit(1)

		if len(self.devices) != len(found_ports):
			print "Number of found Arduinos does not match configured number"
			sys.exit(1)

		for found_port in found_ports:
			try:
				for device in self.devices:
					if device.path == found_port:
						# connect to serial port
						device.port = serial.Serial(found_port, 9600)
						break
			except:
				print 'Failed to open port'
				sys.exit(1)
		# need a short delay right after serial port is started for the Arduino to initialize
		time.sleep(1)

	def close_ports(self):
		print 'closing ports'
		for device in self.devices:
			device.port.close()

if __name__ == "__main__":
	paths = []
	paths.append('/dev/tty.usbmodem14141')

	num_emitters = 35
	emitters = []
	for i in range(0, num_emitters):
		emitters.append([0, 1, i+2, i+2, 0, 0])

	driver = ArduinoDriver(emitters, paths)
	try:
		driver.open_ports()

		for i in range(0, num_emitters):
			emitters.append([0, 1, i+2, i+2, 0, 135])

		time.sleep(2)
		print 'entering loop'

		while True:
			driver.updateEmitters(emitters)
			driver.updateArduinos()
	finally:
		driver.close_ports()