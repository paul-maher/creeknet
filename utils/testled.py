import RPi.GPIO as GPIO
import time
#from w1temperaturesensorarray import W1TemperatureSensorArray

# Class to verify LED operation.
class TestLedArray:

	def __init__(_self):

		# Set board numbering scheme and warnings
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)

		GPIO.setup(11, GPIO.OUT)
		GPIO.setup(13, GPIO.OUT)
		GPIO.setup(15, GPIO.OUT)

	def activityOn(_self):
                GPIO.output(11, GPIO.HIGH)

	def activityOff(_self):
                GPIO.output(11, GPIO.LOW)

	def warningOn(_self):
                GPIO.output(13, GPIO.HIGH)

	def warningOff(_self):
                GPIO.output(13, GPIO.LOW)

	def errorOn(_self):
                GPIO.output(15, GPIO.HIGH)

	def errorOff(_self):
                GPIO.output(15, GPIO.LOW)


# Flash LEDs one at a time
leds = TestLedArray()
while(True):

	leds.activityOn()
	time.sleep(0.1)
	leds.activityOff()
	time.sleep(0.1)

	leds.warningOn()
	time.sleep(0.1)
	leds.warningOff()
	time.sleep(0.1)

	leds.errorOn()
	time.sleep(0.1)
	leds.errorOff()
	time.sleep(0.1)

