
"""
    This is the entry point of the application.
    The user should provide only the name of the folder that contain the CAMALIOT text files.
    The folder must be located in the "\data" folder of the application.
    
    The user should sequentially use the following functions in order to prepare the data for visualization.
        dataDictionary:      To obtain the required data
        dict2json:           To store the required data in JSON format

    Optionally, the function dict2csv can be used to get a list of the latitudes and longitudes of the measurement points.
      
    For the visualization of the data, one or more of the following functions should be called.
        plotDurationPerWeek:     To plot two graphs: the duration of the measurements per week and the cumulative duration.
        plotMeasCountPerWeek:    To plot the cumulative number of the measurements for each GNSS system.
        plotDurationHistogram:   To plot the histogram of the duration of the sessions.
"""  



import os
from dataFunctions import data2dict, dict2json, dict2csv
from plotFunctions import plotDurationPerWeek, plotMeasCountPerWeek, plotDurationHistogram


# Please provide the folder name in which the CAMALIOT text files are stored. 
# The folder must be located in the "\data" folder of the application.
__PROJECTNAME__ = 'testDataSet'



if __name__ == '__main__':

    # Get the CAMALIOT text files in the directory "\data\{__PROJECTNAME__}" and extract data to a list of dictionaries "dataDictionary"
    dataDictionary = data2dict(__PROJECTNAME__)

    # Get the list of dictionaries "dataDictionary" and store the values in the {__PROJECTNAME__}.JSON file in the "\data" folder
    dict2json(dataDictionary, __PROJECTNAME__)

    # Get the list of dictionaries "dataDictionary" and store the longitude and latitude values in the {__PROJECTNAME__}.CSV file in the "\data" folder
    dict2csv(dataDictionary, __PROJECTNAME__)

    # Get the path of the JSON file
    jsonInFilename = os.path.abspath(os.path.join(os.getcwd(), "../data", __PROJECTNAME__ + ".json"))
    
    # Plot two graphs: the duration of the measurements per week and the cumulative duration (stored in the "\figures" folder)
    plotDurationPerWeek(__PROJECTNAME__, file = jsonInFilename) # format=['pdf', 'png', 'jpg']

    # Plot the cumulative number of the measurements for each GNSS system (stored in the "\figures" folder)
    plotMeasCountPerWeek(__PROJECTNAME__, file = jsonInFilename, format=['pdf', 'png', 'jpg'])

    # Plot the histogram of the duration of the sessions (stored in the "\figures" folder)
    plotDurationHistogram(__PROJECTNAME__, file = jsonInFilename) # format=['pdf', 'png', 'jpg']

 
























