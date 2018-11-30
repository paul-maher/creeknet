
import socket
import logging
from datainserter import DataInserter
from creektracer import CreekTracer
from creeknetcfg import CreeknetCfg

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 3001        # Port to listen on (non-privileged ports are > 1023)
LOG_FILE_DIR = "/home/pi/development/1wtemp/trace/"
LOG_FILE_NAME = "datalistener.log"

class DataListener:
    
    def listenForRequest(self):
        
        bytesRead = ''

        tf.addTraceEntryDebug("Data Listener Service entering listening mode on port: " + str(PORT))

         # Create a listening socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # Bind to the port and listen
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
    
            # A connection is made so read some data
            with conn:
                while True:
                    data = conn.recv(1024)
                    if data:
                        bytesRead = bytesRead + data.decode("utf-8")
                    else:
                        break
                    #conn.sendall(data)

        tf.addTraceEntryDebug("Bytes to process: " + bytesRead)
        
        return bytesRead

# Create a trace file for any messages
tf = CreekTracer(LOG_FILE_DIR + LOG_FILE_NAME)
tf.setTraceLevel(logging.INFO)
tf.addTraceEntryInfo("Data Listener Service utility starting...")

# Create a new config 
config = CreeknetCfg()
traceLevel=(config.getTraceLevel())
tf.setTraceLevel(traceLevel)
tf.setTraceLevel(logging.DEBUG) # take out after debug

localId = config.getGcuId()
tf.addTraceEntryInfo("Using GCU prefix of: "  + localId)

# Create the data listener
listener = DataListener()
inserter = DataInserter(localId + '-', tf)

print('Starting...')
while True:

    print('Waiting...')
    data = listener.listenForRequest()
    print("Data received: " + data)
    inserter.insertMultipleEntries(data, tf)

