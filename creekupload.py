# Code to upload file to Google drive. Adapted from code on the Google API documentation website

from __future__ import print_function 
import httplib2 
import os 
import apiclient
from apiclient import discovery 
from oauth2client import client 
from oauth2client import tools 
from oauth2client.file import Storage 
from apiclient.http import MediaFileUpload 
import time
import logging 

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials at ~/.credentials/drive-python-quickstart.json SCOPES = 
#'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive' 
CLIENT_SECRET_FILE = 'client_secret.json' 
APPLICATION_NAME = 'Drive API Python Quickstart' 
LOG_FILE_DIR = "/home/pi/development/1wtemp/logs/"

# Upload a set of files to Google drive if they are not already there
def uploadDataFiles(svc, existingFiles,traceFile):

	# Get todays datte
        todayHint = time.strftime("-%Y-%m-%d",time.localtime())

	traceFile.log(logging.INFO,"Uploading files...")
	for file in os.listdir(LOG_FILE_DIR):

		# If the file is already there don;t upload it again
		if (file in existingFiles):
			traceFile.log(logging.INFO,"File already exists so no need to upload: " + file)
		else:

			# And don;t upload today's file as it will most likely be incomplete.
			if (file.find(todayHint) == -1):

				fullPath=LOG_FILE_DIR+file
				traceFile.log(logging.INFO,"Uploading: " + fullPath)	
				file_metadata = {'name':file}
				#print(file_metadata)
				media = MediaFileUpload(fullPath,mimetype='text/csv')
				file = svc.files().create(body=file_metadata,media_body=media,fields='id').execute()
				#print('Google File ID: %s' % file.get('id')) 

			else:
				traceFile.log(logging.INFO,"Skipping today's files: " + file)

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

def createLogger():

        # Set file and logging options
        logger = logging.getLogger("CREEKUPLOAD")
        logger.setLevel(logging.INFO)

        # create a file handler
        handler = logging.FileHandler('/home/pi/development/1wtemp/trace/creekupload.log')

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)

	return logger


# Main code. Get credentials, get a list of files already on Google drive then call a function to add any files 
# that are not already there. Note the hardwired limit of 500 files. You may need to increase that in the futire.
def main():

    # Create a trace file for any messages
    tf = createLogger()

    tf.log(logging.INFO,"Creek uploader starting...")

    # Creates a Google Drive API service object and outputs the names and IDs for up to 500 files.
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    results = service.files().list(
        pageSize=500,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Build a list of the files already on Google drive 
    fileList=[]
    if not items:
        tf.log(logging.INFO,'No files found on Google drive.')
    else:
        for item in items:
	    fileList.append(item['name'])

    # Upload the files. 'fileList' holds a list of existing files and service is the service hadler which will 
    # do the work of the uploading for us.
    uploadDataFiles(service,fileList,tf) 

    tf.log(logging.INFO,"Creek uploader terminating.")

if __name__ == '__main__':
    main()
