
import os
import datetime
import pandas as pd
import numpy as np
import json


def data2dict(__PROJECTNAME__):
    
    """Create a dictionary with the required data for the application.
    
    Parameter:
        __PROJECTNAME__ (type str): 
            The folder name in which the CAMALIOT text files are stored. 
            The CAMALIOT text file names follow the format:
            camaliot_app_log_YYYY_MM_DD_HH_MM_SS.txt
            The folder must be located in the "\data" folder of the application. 
                    
    Returns: 
        dataDict (type list): 
            A list of dictionaries containing the required data.
    """   

    # Initialize the list of dictionaries containing the required data
    dataDict = []
    
    
    # Get the directory of the CAMALIOT text files
    dirPath = os.path.abspath(os.path.join(os.getcwd(), "../data/", __PROJECTNAME__))

    cnt = 0
    checkPercentage = 5
    print('Processing progress: ', end='')
    # Get a list of the CAMALIOT text files in the user-defined folder
    for path, subdirs, files in os.walk(dirPath):

        # Iterate the files
        for name in files:
            # Construct the file path for each file
            fullPath = path + "\\" + name

            # Initiaize a list to contain data from the lines starting with the keyword "Fix"
            fixLines = []
            # Initiaize a list to contain the constellationType values of the lines starting with the keyword "Raw"
            constellationType = []
            
            cnt += 1
            donePercentage = 100*cnt/len(files)
            if donePercentage > checkPercentage:
                print('* ', end='')
                checkPercentage += 5
            
            
            try:
                # Opening CAMALIOT text file to read
                with open(fullPath, 'r') as inputfile:
                    # Iterate the lines of the files
                    for line in inputfile:
                        
                        # From the line staring with "# Fix" get the header of the data 
                        if line.split(',')[0] == "# Fix":    
                            line = line.strip()                     # (this it to remove the trailing "\n")
                            fixLinesHeader = line.split(',')[2:]    # (ignore the first two, i.e. Fix and Provider)
                            
                        # From the line staring with "Fix" get the values of the data 
                        elif line.split(',')[0] == "Fix":
                            fixLines.append(float(item) for item in line.split(',')[2:])   # (ignore the first two, i.e. Fix and gps)
                            
                        # From the line staring with "Raw" get the values of the constellationType 
                        if line.split(',')[0] == "Raw":                
                            constellationType.append(line.split(',')[28])  # (position 28 in the list)
                # Close file            
                inputfile.close() 
            except:
                print('Problem with opening CAMALIOT text files.')
                return 1
                    
            # Initialize pandas dataframe to store the "Fix" data   
            dfFix = pd.DataFrame(fixLines, columns=fixLinesHeader)   
            
            # Initialize pandas dataframe to store the constellationType values of the "Raw" data
            dfRaw = pd.DataFrame(constellationType, columns=['constellationType'])
              
            # Initialize pandas dataframe to match the GNSS systems with the constellationType values
            dfRawNumInit = pd.DataFrame(['UNKNOWN','GPS','SBAS','GLONASS','QZSS','BEIDOU','GALILEO','IRNSS'], 
                            index=['0','1','2','3','4','5','6','7'], columns=['gnssSystems'] )
            
            # Initialize pandas dataframe to store the measurement count per GNSS system
            dfRawCnt = dfRaw['constellationType'].value_counts().to_frame()
            dfRawCnt.columns = ['MeasCountPerSystem']
                 
            # Initialize pandas dataframe to store the measurement percentage per GNSS system
            dfRawPer = dfRaw['constellationType'].value_counts(1).to_frame() # (1 is used to get the frequencies)
            dfRawPer.columns = ['MeasPercentagePerSystem']
            
            # Initialize pandas dataframe to combine the required information
            dfRawStat = pd.concat([dfRawNumInit, dfRawCnt, dfRawPer], axis=1)

            # Round percentages to two digits
            dfRawStat['MeasPercentagePerSystem'] = dfRawStat['MeasPercentagePerSystem'].round(2)
            
            # Replace the default NaN value to None that is to compatible with the JSON format
            dfRawStat = dfRawStat.replace({np.NaN: None})
            
            # Convert pandas dataframe to dictionary
            dictStat = dfRawStat.to_dict()

            # Append information while iterating the data files
            dataDict.append({
                            # Timestamp of the first measurement (minimum in the list of timestamps "(UTC)TimeInMs") 
                            "Start date-time": datetime.datetime.fromtimestamp(dfFix['(UTC)TimeInMs'].min()/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'),
                            # Duration of measurement (maximum - minimum of the timestamps "(UTC)TimeInMs") in [MM:SS] format
                            "Duration [MM:SS]": datetime.datetime.fromtimestamp((dfFix['(UTC)TimeInMs'].max()-dfFix['(UTC)TimeInMs'].min())/1000.0).strftime('%M:%S'),
                            # Duration of measurement (maximum - minimum of the timestamps "(UTC)TimeInMs") in decimal minutes [MM:f] format
                            "Duration [M.f]": round((dfFix['(UTC)TimeInMs'].max()-dfFix['(UTC)TimeInMs'].min())/60000, 4),
                            # Latitude of the measurment (median of the list of latitudes) in decimal degrees [deg] format
                            "Latitude (median) [deg]": round(dfFix['Latitude'].median(), 6),
                            # Longitude of the measurment (median of the list of Longitudes) in decimal degrees [deg] format
                            "Longitude (median) [deg]": round(dfFix['Longitude'].median(), 6),
                            # Total count of measurements (number of "Raw" records)
                            "TotalCountOfMeas": int(len(dfRaw)),
                            # Dictionary matching constellationType to the name of the GNSS system
                            "GnssSystems" : dictStat['gnssSystems'],
                            # Dictionary matching constellationType to the count of measurements for each GNSS system
                            "MeasCountPerSystem" : dictStat['MeasCountPerSystem'],
                            # Dictionary matching constellationType to the percentage of measurements for each GNSS system
                            "MeasPercentagePerSystem" : dictStat['MeasPercentagePerSystem']
                            }
            )
            
            # Example of the dataDict structure
            # {
            #     "Start date-time": "2022-03-26 17:17:44.688000",
            #     "Duration [MM:SS]": "10:29",
            #     "Duration [M.f]": 10.4885,
            #     "Latitude (median) [deg]": 36.197195,
            #     "Longitude (median) [deg]":16.123804,
            #     "TotalCountOfMeas": 15468,
            #     "GnssSystems": {
            #         "0": "UNKNOWN",
            #         "1": "GPS",
            #         "2": "SBAS",
            #         "3": "GLONASS",
            #         "4": "QZSS",
            #         "5": "BEIDOU",
            #         "6": "GALILEO",
            #         "7": "IRNSS"
            #     },
            #     "MeasCountPerSystem": {
            #         "0": null,
            #         "1": 4976.0,
            #         "2": null,
            #         "3": 4117.0,
            #         "4": null,
            #         "5": 6375.0,
            #         "6": null,
            #         "7": null
            #     },
            #     "MeasPercentagePerSystem": {
            #         "0": null,
            #         "1": 0.32,
            #         "2": null,
            #         "3": 0.27,
            #         "4": null,
            #         "5": 0.41,
            #         "6": null,
            #         "7": null
            #     }
            # }
                
        print('\nAll files are processed!')
                
    return dataDict





def dict2json(data, __PROJECTNAME__):

    """Serialize data and store them in a JSON format file.
    
    Parameter:
        data (type list): 
            A list of dictionaries containing the required data.
        __PROJECTNAME__ (type str): 
            The folder name in which the CAMALIOT text files are stored. 
            The CAMALIOT text file names follow the format:
            camaliot_app_log_YYYY_MM_DD_HH_MM_SS.txt
            The folder must be located in the "\data" folder of the application.     
    Returns: 
        0
    """   
       
    # Get the path to create the JSON file
    filePath = os.path.abspath(os.path.join(os.getcwd(), "../data/", __PROJECTNAME__ + ".json"))
 
    # Serializing json 
    json_object = json.dumps(data, indent = 4)
      
    try:
        # Writing to JSON file
        with open(filePath, 'w') as outFile:
            outFile.write(json_object)
        
        outFile.close()                     
    except:
        print('Problem with writing the JSON file.')
        return 1
    
    print(f"The {__PROJECTNAME__}.json file is stored in the \\data folder.")
    return 0
    


def dict2csv(data, __PROJECTNAME__):

    """Extract and list the longitudes and latitudes in a CSV format file
    
    Parameter:
        data (type list): 
            A list of dictionaries containing the required data.
        __PROJECTNAME__ (type str): 
            The folder name in which the CAMALIOT text files are stored. 
            The CAMALIOT text file names follow the format:
            camaliot_app_log_YYYY_MM_DD_HH_MM_SS.txt
            The folder must be located in the "\data" folder of the application. 
    
    Returns: 
        0
    """   

    # Get the path to create the CSV file
    filePath = os.path.abspath(os.path.join(os.getcwd(), "../data/", __PROJECTNAME__ + ".csv"))

    try:
        # Writing to CSV file
        with open(filePath, 'w') as outFile:
            # Write the header
            outFile.write('Longitude (median) [deg], Latitude (median) [deg]\n')
            
            # Iterate the list of dictionaries
            for item in data:
                
                # Extract the longitude and latitude values
                long = item['Longitude (median) [deg]']
                lat = item['Latitude (median) [deg]']
            
                # Write the longitude and latitude values
                outFile.write(f"{long}, {lat}\n")           
            
        outFile.close()                     
    except:
        print('Problem with writing the CSV file.')
        return 1
    
    print(f"The {__PROJECTNAME__}.csv file is stored in the \\data folder.")
    return 0
       

    
    
    
    
    
    
    
    