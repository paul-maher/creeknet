
from w1temperaturesensorarray import W1TemperatureSensorArray
from valuelogger import ValueLogger
import time
from ledarray import LedArray
import json
from creeknetcfg import CreeknetCfg
from creektracer import CreekTracer

# Wait betwwen readings. Flash the activity LED avery seconds. Number of seconds to delay is read from the config file
def pauseBetweenReadings(count, leds, cfg):

	# Read the delay time from the config object
	count = cfg.getDelay()
	tf.addTraceEntryInfo("Pausing for " + str(count) + " seconds")     

	for n in range(0,count):
		#Led On
		leds.activityOn()
		time.sleep(0.5)
		#Led Off
		leds.activityOff()
		time.sleep(0.5)

# Created handler for LEDs
ledArray = LedArray()

# Create an array of sensors
sensorArray = W1TemperatureSensorArray()

# Create a logger to manage the CSV files
logger = ValueLogger()

# Create a tracing file for logging messages
tf = CreekTracer()

# And go round indefinitly taking readings
count = 0
tf.addTraceEntryInfo("Creeknet Generic Data Collector Starting")      
while(True):

	print(count)
	count+=1
	
	# Create a new config  object each iteration , as the values in the config file may have changes since last time
	config = CreeknetCfg()
	
	# Set the level for the tracing before we go any further
	traceLevel = config.getTraceLevel()
	tf.setTraceLevel(traceLevel)

	# Get the readings from the sensors
	vals = sensorArray.getReadingsEx(ledArray, tf, config)

	# Append values to the CSV file
	logger.AppendValues(vals, tf, config)

	# And wait for a specified delay, while flashing the activity LED
	pauseBetweenReadings(30,ledArray,config)

	# Remove the old config object
	del config
