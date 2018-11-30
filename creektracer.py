import logging

# Class to append entries to Creeknet tracing file
class CreekTracer:
        
    # Initilise the logger
    def __init__(_self):
        
        # Set file and logging options
        _self.logger = logging.getLogger("CREEKNET")
        _self.logger.setLevel(logging.WARNING)

        # create a file handler
        handler = logging.FileHandler('/home/pi/development/1wtemp/trace/creeknettrace.log')
        #handler.setLevel(logging.INFO)

        # create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        _self.logger.addHandler(handler)

    # Add an info msg antry to the trace file        
    def addTraceEntryDebug(_self,str):

        _self.logger.log(logging.DEBUG,str)

    def addTraceEntryInfo(_self,str):

        _self.logger.log(logging.INFO,str)

    def addTraceEntryWarning(_self,str):

        _self.logger.log(logging.WARNING,str)

    def addTraceEntryError(_self,str):

        _self.logger.log(logging.ERROR,str)
        
    def setTraceLevel(_self,lvl):

        #print("Set logging to: " + str(lvl))
        _self.logger.setLevel(lvl)
	  
