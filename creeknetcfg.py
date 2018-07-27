import json
import logging

# Class to manage configuration settings. On initialisation read all the values into a class
# variable and add appropriate 'get' functions to return the specific values as required.
class CreeknetCfg:

	data = ""

	# As the class is initiated, read the values dynamically from the config file
	def __init__(_self):

		with open('/home/pi/development/1wtemp/creeknetcfg.json') as data_file:
			_self.data = data = json.load(data_file)

	# Get the delay between readings. Acceptable values are between 5 and 7200 seconds, default value is 30 seconds
	def getDelay(_self):

		try:       
			count = max(5,min(7200,int(_self.data['parameters']['delay'])))
		except:
			count = 30
    
		return count

	# Get the root name of this GCU.
	def getGcuId(_self):

		try:
			# Read the value form the config file
			return _self.data['parameters']['gcuid']
		except:
			return("GCU-UNKNOWN")

	# Get Sensor Definition from config file
	def getSensorDefinition(_self):

		try:
			return(_self.data['sensors'])
		except:
			return ""

	# Get the ip address of the mazi portal server.
	def getMaziAddress(_self):

		# Read the value from the config file
		try:
			return _self.data['parameters']['maziServerAddress']
		except:
			return ""

	# Get the current tracing level.
	def getTraceLevel(_self):

		# Read the value from the config file and select the appropriate logging level
		try:
			lvlStr = _self.data['parameters']['traceLevel']
			if (lvlStr.lower()=="error"):
				return logging.ERROR
			if (lvlStr.lower()=="warning"):
				return logging.WARNING
			if (lvlStr.lower()=="debug"):
				return logging.DEBUG
			else:
				return logging.INFO
		except:
			return logging.INFO
