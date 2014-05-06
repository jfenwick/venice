"""
Control n servos on n arduinos over serial

"""

import glob
import platform
import serial
import time
import sys

'''
Servo
Pin number, angle for servo, Arduino port servo is on
For now the port is used as an index, so please number them going from 0-n

'''
class Servo:
	pin = 0
	port = 0
	angle = 0

	def __init__(self, pin, port, angle):
		self.pin = pin
		self.port = port
		self.angle = angle

'''
Bulb
Pin number, on/off, Arduino port bulb is on
'''
class Bulb:
	pin = 0
	port = 0
	on = False

	def __init__(self, pin, port, bulb):
		self.pin = pin
		self.port = port
		self.bulb = bulb

'''
ServoDriver
-Stores a list of servos
-Open ports to Arduinos
-Stores a list of those ports
-Creates a map of which servos are on which ports
-Provides a way to update the angle of all servos on all ports
'''
class ServoDriver:
	def __init__(self, servos, bulbs, port_types):
		self.servos = servos
		self.bulbs = bulbs
		self.ports = self.open_ports()
		#self.port_types = 
		self.last_update_time = time.clock()

	# looks for all devices that have the same name pattern as an Arduino and opens them
	def open_ports(self):
		# find arduinos
		# note: currently this is Mac only
		devices = glob.glob('/dev/tty.usbmodem*')
		print devices

		if len(devices) == 0:
			print "No Arduinos found"
			sys.exit(1)

		ports = []
		for device in devices:
			try:
				# connect to serial port
				ports.append(serial.Serial(device, 9600))
			except:
				print 'Failed to open port'
				sys.exit(1)

			
		# need a short delay right after serial port is started for the Arduino to initialize
		time.sleep(1)
		return ports

	# update the model with emitter information and update if enough time has passed
	def updateEmitter(self, servoArduinoNumber, bulbArduinoNumber, emitterServoPin, emitterBulbPin, emitterState, emitterAngle):
		# constrain the servo angle
		if emitterAngle > 135:
			emitterAngle = 135
		elif emitterAngle < 45:
			emitterAngle = 45

		# find and update servo
		for servo in self.servos:
			if servo.pin == emitterServoPin and servo.port == servoArduinoNumber:
				servo.angle = emitterAngle
				break

		# update bulb
		# NEED BULB CODE

		# if enough time has elapsed since the last update, update arduinos
		elapsed = (time.clock() - self.last_update_time)
		if elapsed > 1.0:
			#print 'elapsed: ' + str(elapsed)			
			servo_data = []
			bulb_data = []
			# initialize servo_data array
			for p in self.ports:
				servo_data.append('')

			for servo in self.servos:
				#print 'servo: ' + str(servo.pin) + 'port: ' + str(servo.port)
				# append angle to the datum for this port
				servo_data[servo.port] = servo_data[servo.port] + str(servo.angle).zfill(3)

				# append null byte to character arrays going to arduinos to signal end of update
				for servo_datum in servo_data:
					servo_datum = servo_datum + "\0"
			# send data to the Arduinos
			#print servo_data
			for port,servo_datum in zip(self.ports,servo_data):
				port.write(servo_datum)
			self.last_update_time = time.clock()



	def close_ports(self):
		print 'closing ports'
		for port in self.ports:
			port.close()

# generates values for making a servo sweep back and forth
def servo_iter():
	l = []
	for i in range(0,100):
		l.append(40)
	for i in range(0,100):
		l.append(80)
	for pos in l:
		yield pos

def servo_iter_2(total):
	for i in range(0,total):
		yield i

if __name__ == "__main__":
	# create a list of servos with mappings to ports
	# if you have the wrong number of servos it acts weird
	#num_servos = 32
	num_servos = 2
	servos = []
	servos.append(Servo(9, 0, 40))
	servos.append(Servo(10, 0, 40))
	'''
	servos.append(Servo(2, 0, 40))
	servos.append(Servo(3, 0, 40))
	servos.append(Servo(4, 0, 40))
	servos.append(Servo(5, 0, 40))
	servos.append(Servo(6, 0, 40))
	servos.append(Servo(7, 0, 40))
	servos.append(Servo(8, 0, 40))
	servos.append(Servo(9, 0, 40))
	servos.append(Servo(10, 0, 40))
	servos.append(Servo(11, 0, 40))
	servos.append(Servo(12, 0, 40))
	servos.append(Servo(13, 0, 40))
	servos.append(Servo(14, 0, 40))
	servos.append(Servo(15, 0, 40))
	servos.append(Servo(16, 0, 40))
	servos.append(Servo(17, 0, 40))
	servos.append(Servo(18, 0, 40))
	servos.append(Servo(19, 0, 40))
	servos.append(Servo(20, 0, 40))
	servos.append(Servo(21, 0, 40))
	servos.append(Servo(22, 0, 40))
	servos.append(Servo(23, 0, 40))
	servos.append(Servo(24, 0, 40))
	servos.append(Servo(25, 0, 40))
	servos.append(Servo(26, 0, 40))
	servos.append(Servo(27, 0, 40))
	servos.append(Servo(28, 0, 40))
	servos.append(Servo(29, 0, 40))
	servos.append(Servo(30, 0, 40))
	servos.append(Servo(31, 0, 40))
	servos.append(Servo(32, 0, 40))
	'''

	if len(servos) != num_servos:
		print 'wrong number of servos'
		sys.exit(1)

	# comment out the next two lines if you only have 1 arduino
	#servos.append(Servo(2, 1, 40))
	#servos.append(Servo(3, 1, 40))
	#servos.append(Servo(4, 2, 40))
	#servos.append(Servo(5, 2, 40))

	angles = []
	for i in range(0,len(servos)):
		angles.append(40)

	bulbs = []

	try:
		# instantiate a driver
		# must happen inside try-finally
		x = ''
		driver = ServoDriver(servos, bulbs, x)
		
		iter1 = True
		if iter1:
			pos = servo_iter()
		else:
			pos = servo_iter_2(len(servos))

		while True:
			try:
				x = pos.next()
			except StopIteration:
				if iter1:
					pos = servo_iter()
				else:	
					pos = servo_iter_2(len(servos))
				x = pos.next()
			# create a list of servos with ids and angles to update positions of servos
			if iter1:
				for servo in servos:
					servo.angle = x
					# update emitter data model
					driver.updateEmitter(servo.port, 1, servo.pin, 10, False, servo.angle)
			else:
				for i,servo in zip(angles,servos):
					servo.angle = i
					# update emitter data model
					driver.updateEmitter(servo.port, 1, servo.pin, 10, False, servo.angle)


			for i in range(0, len(servos)):
				if i == x:
					angles[i] = 80
				else:
					angles[i] = 40

	# close the serial port on exit, or you will have to unplug the arduinos to connect again
	finally:
		driver.close_ports()