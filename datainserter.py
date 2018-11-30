
import pandas as pd

# Class to insert spot entries into specific CSV data files. Relies on the pandas libraries for the CSV manipulation.
class DataInserter:
    
    # Initialise the class, TODO: get the name root from the config file
    def __init__(_self, nameRoot, tf):

        _self.nameRoot = nameRoot
        tf.addTraceEntryDebug("Using name root: " + _self.nameRoot)

    # Insert a single entry into a specific data file. Entries ar of the form yyyy-mm-dd, hh:mm:ss, column name, value to insert
    def insertSingleEntry(_self, csvEntry, tf):

        tf.addTraceEntryDebug("Insert Single Entry: " + _self.nameRoot + " " + csvEntry)
        
        try:
            # Split into the individual parts
            vals =csvEntry.split(',')
    
            # So the file name is the first entry
            fileName = "logs/" + _self.nameRoot + vals[0] + ".csv"
 
            # Get the entry time, columne name and value to write
            entryTime = vals[1]
            colName = vals[2]
            newVal = vals[3]
    
        except:   
            # Looks like an error with the provided data, so report error and give up
            tf.addTraceEntryError("An error has occured trying to parse the CSV entry: " + csvEntry)
            return 

        try:      
            # Try to read in the specified file. TODO: Need to put a lock on the file while we are using it.
            dataset = pd.read_csv(fileName, keep_default_na = False)
    
        except:          
            # Problems readin in the data file, maybe it doesn;t exist?
            tf.addTraceEntryError('Error while reading the specified CSV data file:' + fileName)
            return
            
        try: 
            # Make a logical array based on the time. The first False in the logical array is where we insert this entry
            log = dataset['Time'] >= entryTime
        
            # So here the index of the first True value is where we need to put the entry. If the logical array is all False entris
            # then there is no corresponding time, so abandon
            rowidx = log[log == False].size
            if (rowidx == dataset.shape[0]):
                tf.addTraceEntryWarning('No corresponding entry in the data file for this time period')
                return
            
                # Get the col index for the specified column
            colidx = dataset.columns.get_loc(colName)
            print("colidx = " + str(colidx))

            # Set the entry in the dataframe 
            dataset.iloc[rowidx,colidx] = newVal

            # And write back to the CSV file
            tf.addTraceEntryDebug("Overwriting existing CSV  datafile")
            dataset.to_csv(fileName, index=False)
            #dataset.to_csv('test.csv',index=False)
            
        except Exception as e:
            tf.addTraceEntryError("An error has occured trying to add the log entry")
            
    # Insert multiple entries, delimited with a '|' character..
    def insertMultipleEntries(_self, csvEntries, tf):
        print("Insert multi Entries")
        
        vals =csvEntries.split('|')
        for val in vals:
            _self.insertSingleEntry(val, tf)
        
    def insertFromFile(_self, fileName, tf):
        print("Insert from File:" + fileName)
        
        # Read in the file one line at a time and call insert single entry
        
    def insertFromDataFrame(_self, df, tf):
        print("Insert from DataFrame")
     
        # work through each line in the data file and call add single entry
        
# Add one entry
#insertSingleEntry("2018-09-03,08:15:00,Salinity,2.9")
#insertSingleEntry("2018-09-03,09:00:00,Salinity,2.8")
#insertSingleEntry("2018-09-03,10:00:00,Salinity,2.8")
#insertSingleEntry("2018-09-03,11:00:00,Salinity,2.7")
#insertSingleEntry("2018-09-03,12:00:00,Salinity,2.8")
#insertSingleEntry("2018-09-03,13:00:00,Salinity,2.8")
#insertSingleEntry("2018-09-03,14:00:00,Salinity,2.4")
#insertSingleEntry("2018-09-03,15:00:00,Salinity,2.6")
#insertSingleEntry("2018-09-03,16:00:00,Salinity,2.3")
#insertSingleEntry("2018-09-03,17:00:00,Salinity,2.8")
#insertSingleEntry("2018-09-03,18:00:00,Salinity,2.8")

#a = DataInserter("TEST-RIG-")
#a.insertSingleEntry("2018-08-25,14:00:00,Salinity,2.9")

#a.insertMultiplEntries("2018-09-03,08:15:00,Salinity,2.1|2018-09-03,08:20:00,Salinity,2.9|2018-09-03,08:25:00,Salinity,3.1")
#a.insertMultiplEntries("2018-09-03,08:15:00,Salinity,2.1|2018-09-03,08:20:00,Salinity,2.9")
#a.insertMultipleEntries("2018-08-25,14:00:00,Salinity,2.9|2018-08-25,14:05:00,Salinity,2.5")

#a.insertMultiplEntries("2018-09-03,08:15:00,Salinity,2.1")

#a.insertFromFile("fred.csv.txt")
 


