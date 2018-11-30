# Code to look for changes to IP address, write to a log file and push the log fle to Google drive
from __future__ import print_function 
import httplib2 
import os 
import apiclient
#from apiclient import discovery 
from googleapiclient import discovery 
from oauth2client import client 
from oauth2client import tools 
from oauth2client.file import Storage 
from googleapiclient.http import MediaFileUpload 
import time
import logging 
import commands
from creektracer import CreekTracer
from creeknetcfg import CreeknetCfg

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# Define the scope and other variables for Google drive authentication
SCOPES = 'https://www.googleapis.com/auth/drive' 
CLIENT_SECRET_FILE = 'client_secret.json' 
APPLICATION_NAME = 'Drive API Python Quickstart' 
LOG_FILE_DIR = "/home/pi/development/1wtemp/trace/"
LOG_FILE_NAME = "ipchange.log"

# Uplodad the local log files contaning IP address changes to Google Drive
def uploadLogFile(tf, gcuId, logName, logDir):

	# TODO:  append the name of the collector unit from the JSON config file

	# Creates a Google Drive API service object and upload the specified log file
	try:
		# Get the credenetials and service for the Google Drive service
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('drive', 'v3', http=http)

		# And use the servide to upload the file
		fullPath=logDir+logName
		tf.addTraceEntryInfo("Uploading: " + fullPath)	
		file_metadata = {'name':gcuId + "-" + logName}
		media = MediaFileUpload(fullPath,mimetype='text/csv')
		file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()

		# And tell the caller the upload is completed
		return False

	except:
		# Something has not worrked out. So log the fact and tell the caller that the upload has failed 
		# so it can be re-attempted on the next iteration
		tf.addTraceEntryError("Unable to establish credentials or service for access to Google Drive, abandon upload attempt")
		return True


# Get the appropriate credentials to use with this Google drive account
def get_credentials():

    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials 

# Main code. Get the current IP address (internal and external) and wait for it to change. If it does change write the values to a file and
# upload the file to Google drive
def main():

    # Might be starting off crontab so allow time for the network to establish itself 
    time.sleep(30)
    
    ipInOld="0.0.0.0"
    ipOutOld=ipInOld

    # Create a trace file for any messages
    tf = CreekTracer(LOG_FILE_DIR + LOG_FILE_NAME)
    #tf.setTraceLevel(logging.INFO)
    tf.addTraceEntryInfo("IP Address change log utility starting...")

    # Keep looping forever
    while(True):

        # Create a new config  object each iteration , as the values in the config file may have changed
        config = CreeknetCfg()
        traceLevel=(config.getTraceLevel())
	tf.setTraceLevel(traceLevel)

	# Use OS commands to get the local and remote IP address. These will be empty if there is no connection
        ipIn=commands.getoutput('hostname -I')
        ipOut=commands.getoutput('curl -s ipinfo.io/ip')
        tf.addTraceEntryDebug("Inside IP Address: " + ipIn)
        tf.addTraceEntryDebug("Outside IP Address: " + ipOut)

	# Note if the internal IP has changed
        if(ipIn!=ipInOld):
                tf.addTraceEntryWarning("Internal IP address changed to: " + ipIn)
                ipInOld=ipIn
                uploadRequired=True

	# Note if the external IP has changed
        if(ipOut!=ipOutOld):
                tf.addTraceEntryWarning("External IP address changed to: " + ipOut)
                ipOutOld=ipOut
                uploadRequired=True

	# If an upload is necessary, go ahead and try it here. Note its not worth trying unless we have an internal and extenal 
	# ip address available. Otherwise just skip this step. Not much else we can do 
        if (uploadRequired==True and ipOut!='' and ipIn!=''):
                tf.addTraceEntryWarning("Uploading log file to Google drive in response to an address change")
                uploadRequired=uploadLogFile(tf,config.getGcuId(),LOG_FILE_NAME,LOG_FILE_DIR) 

	# Wait before going around again....
        time.sleep(300)

    tf.addTraceEntryInfo("IP Address change log utility exiting.")

if __name__ == '__main__':
    main()
