import time
import os.path
from creeknetcfg import CreeknetCfg

class ValueLogger:

	# Add some value to the logger file
	def AppendValues(_self, values, tf, cfg):

		filePrefix = cfg.getGcuId()

		# Write values out as CSV values
		addComma = False
		line = time.strftime("%d/%m/%Y,%H:%M:%S,",time.localtime())

		# Add each value in turn 
		for value in values:
			
			# Add commas as appropriate
			if addComma == True:
				line+= ","
			addComma = True

			# Add valur to 2 decimal places
			if (value[1] == "N/A"):
				line += value[1]
			else:
				line += "{:.02f}".format(value[1])
					
		tf.addTraceEntryDebug("Writing to log file: " + line)
		line += "\r\n"

		# And write this entry to the log file				
		fp = _self.openLogFile(values, filePrefix,tf)
		fp.write(line)
		fp.close()
		
	def openLogFile(_self, values, prefix, tf):

		#logFileName = "./logs/" + prefix + time.strftime("-%Y-%m-%d",time.localtime()) + ".csv"
		logFileName = "/home/pi/development/1wtemp/logs/" + prefix + time.strftime("-%Y-%m-%d",time.localtime()) + ".csv"

		#logFileName = _self.gcuID + time.strftime("-%Y-%m-%d",time.localtime()) + ".csv"
		#logFileName = _self.gcuID + time.strftime("-%Y-%m-%d-%H",time.localtime()) + ".csv"

		#print("Create value logger:",logFileName)
		tf.addTraceEntryDebug("Opening log file: " + logFileName)

		# If the file is there open it, otherwise create it
		fileExists = os.path.isfile(logFileName)
		fp = open(logFileName,"a")

		# If we just created it need to add the headers
		if (fileExists == False):
			headers = "Date,Time"
			for value in values:
				headers = headers + "," + value[0] 
			fp.write(headers + "\r\n")
			print(headers)

		return fp
