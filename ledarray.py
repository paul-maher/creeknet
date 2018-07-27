import RPi.GPIO as GPIO
import time

# Class to manage the LEDs on the breakout board
class LedArray:

	def __init__(_self):

		# Set board numbering scheme and warnings
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)

		# Set the pins to be outputs
		GPIO.setup(11, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)

		# Flash each LED in turn at atartup.
		_self.activityOn()
		time.sleep(0.2)
		_self.activityOff()
		_self.warningOn()
		time.sleep(0.2)
		_self.warningOff()
		_self.errorOn()
		time.sleep(0.2)
		_self.errorOff()
		time.sleep(0.2)

	# Switch on the activity LED	
	def activityOn(_self):
                GPIO.output(11, GPIO.HIGH)

	# Switch off the activity LED	
	def activityOff(_self):
                GPIO.output(11, GPIO.LOW)

	# Switch on the warning (orange) LED	
	def warningOn(_self):
                GPIO.output(13, GPIO.HIGH)

	# Switch off the warning (orange) LED	
	def warningOff(_self):
                GPIO.output(13, GPIO.LOW)

	# Switch on the error (red) LED	
	def errorOn(_self):
                GPIO.output(15, GPIO.HIGH)

	# Switch off the error (red) LED	
	def errorOff(_self):
                GPIO.output(15, GPIO.LOW)

