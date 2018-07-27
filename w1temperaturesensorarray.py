from w1thermsensor import W1ThermSensor
import os

# Class to define an array of temperature sensors

class W1TemperatureSensorArray:

	# Get the readings from each sensor in turn
	def getReadingsEx(_self, leds, tf, cfg):

		tf.addTraceEntryInfo("Taking readings from temperature sensors ex")

		# Get a list of sensors to check form the config file	
		sensorArray = cfg.getSensorDefinition()

		# Get the Ip address of the Mazi server in case we need to record any values to it
		maziIP = cfg.getMaziAddress()

		# And the readings will be held here
		sensorReadings = []

		# Turn LEDS on or off
		leds.activityOn()
		leds.warningOff()
		leds.errorOff()

		# Keep a track of the total values read from the sensors
		totalReadings = 0

		# And work through each sensor
		for current in sensorArray:

			try:

				if (current['enabled'].lower() == 'true'):
	
					# Get a reference to the sensor
					sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, current['id'])
				
					# Add the lookup string (e.g. "12M-DEPTH" amd the temperatur reading to the list
					reading = sensor.get_temperature()
					totalReadings += reading
					sensorReadings.append((current['description'],reading))

					# And see if we need to record this value to the MAZI portal server
					if (current['exportToMazi'].lower() != 'false'):
						_self.reportToMaziPortal(tf, current['exportToMazi'],maziIP)

			except:
				# Caught some sort of error. Log the details to the trce file
				tf.addTraceEntryError("Error while trying to read from sensor: " + current['id'] + " " + current['description'])

				# And add the NA for this sensor reading
				sensorReadings.append((current['description'],"N/A"))
	
				# Switch on waring LED
				leds.warningOn()

		# If all the readings are zero, this looks highly suspicious. Turn on error LED		
		if (totalReadings == 0):
			tf.addTraceEntryError("Error, all sensors returned zero values. Please check conection to sensor array")
			leds.errorOn()

		# Finished wih readings, urn off activity LED		
		leds.activityOff()

		# And return the list of readings
		return sensorReadings
	
        # Report a value to the Mazi server. Try and ping the MAZI server first before going to the 
	# trouble of running the script
	def reportToMaziPortal(_self,tf,sensorName, ip):

		try:
			# Ping the server first before trying to run the script. If its not
			# pingable then don't both with the script
			print("Record this value on MAZI server using " + sensorName + " on ip address " + ip)
			if (os.system("ping -c 1 " + ip) == 0):

				# Got a ping responds so try and commint the readings using the 
				# mazi-sense.sh file
				systemCmd = "sudo bash /root/back-end/mazi-sense.sh -n " + sensorName + " -t --store -D " + ip
				tf.addTraceEntryInfo(systemCmd)
				os.system(systemCmd)
			else:
				tf.addTraceEntryWarning("No ping response from MAZI portal server. Abandon attempt to record sensor values")

		except:
			tf.addTraceEntryError("Error while trying to commit readings to MAZI portal server")

