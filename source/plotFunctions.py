import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import json




def plotDurationPerWeek(__PROJECTNAME__,
                        file,
                        format = ['jpg']
                        ):

    """Plot two graphs: the duration of the measurements per week and the cumulative duration.
    
    Parameter:
        __PROJECTNAME__ (type str): 
            The folder name in which the CAMALIOT text files are stored. 
        file (type str):               
            The path of the relevant JSON file.
        format (type list)
            The list of the user-defined formats to export the figures.
            It supports only the formats jpg, pdf and png.
        
    Returns: 
        0
    """  
    
    #### Read data from the JSON file ####

    try:
        # Opening JSON file to read
        with open(file, 'r') as inputFile:
            # Read the json file
            dataJSON = json.load(inputFile)
        inputFile.close()
    except:
        print('Problem with opening the JSON file.')
        return 1
        
    
    #### Restructure data before plotting ####
    
    # list to collect the required data for the plot 
    data2plot = []
    
    # Iterate the imported list of dictionaries
    for item in dataJSON:
        
        # The starting date-time of each measurement session. It is used to compute the respective day of year (DOY) and week of year (WOY)
        date = datetime.datetime.strptime(item['Start date-time'],'%Y-%m-%d %H:%M:%S.%f')
        # The week of year of the measurement session. (It is used in the current implementation to group the data to plot)
        WOY = date.isocalendar()[1]
        # The duration of each measurement session
        Duration = item['Duration [M.f]']
    
        # List of the aforementioned data
        values2plot = [WOY,
                       Duration, 
                       ]
        
        # Append data to a list
        data2plot.append(values2plot)

          
    # Create the header (name of columns) of the dataframe    
    columns2plot = ['WOY', 'Duration']
    
    # Create a dataframe with the values to be used in the plot
    df2plot = pd.DataFrame(data2plot, columns=columns2plot)
    # Convert the JSON null (None type) values to numpy NaN values
    df2plot = df2plot.fillna(value=np.nan)
    
    # Group data with respect to the week of year
    df2plot = df2plot.groupby('WOY', as_index=False).agg('sum')

    # Create a dataframe that contains all the week numbers for the given interval of the measurement sessions
    dfWOY = pd.DataFrame(range(df2plot['WOY'].min(), df2plot['WOY'].max()+1),
                      columns=['WOY'])

    # Create a dataframe in which the weeks of the year that have no measurements will be filled with NaN values
    df2plot = dfWOY.join(df2plot.set_index('WOY'), on='WOY')
    
    # Convert the numpy NaN values to zeros (0)
    df2plot = df2plot.fillna(0)
    
    # Compute the cumulative duration of the measurements
    df2plot['CumulativeDuration'] = df2plot['Duration'].cumsum()/60
    

    #### Make the \figures folder if it does not already exist ####

    # Get the \figures directory to save the following figures
    dirPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/"))
    # Make the \figures folder if it does not already exist
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
        
        
    #### Plot the duration of the measurements per week ####     

    
    fig = plt.figure()
    ax = plt.gca()
    
    # Create a colormap
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "yellow", "green"])
    
    plt.bar(df2plot['WOY'], df2plot['Duration'], color=cmap(df2plot['Duration']/df2plot['Duration'].max()))

    step = 1
    xMin = df2plot['WOY'].min() 
    xMax = df2plot['WOY'].max() 

    # x-axis ticks
    ax.set_xticks(np.arange(xMin, xMax + step, step=step))
    # x-axis ticklabels
    ax.set_xticklabels(np.arange(xMin, xMax + step, step=step), fontsize = 14)
    # x-axis limits
    ax.set_xlim(xMin - 1, xMax + 1)
    
    # y-axis grid
    ax.yaxis.grid()
    
    # x-axis label
    plt.xlabel('Week of year 2022', fontsize = 18)
    # y-axis label
    plt.ylabel('Duration of measurements per week [min]', fontsize = 18)
       
    # attributes of the figure
    xlength = 12
    fig.set_size_inches(xlength, xlength/1.618)
    
    # show the plot
    plt.show()
    
    # Save as .pdf at \figures folder
    if 'pdf' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_MeasDurationPerWeek.pdf"))
        fig.savefig(figPath, format='pdf', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_MeasDurationPerWeek.pdf is stored in the \figures folder')
    # Save as .png at \figures folder
    if 'png' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_MeasDurationPerWeek.png"))
        fig.savefig(figPath, format='png', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_MeasDurationPerWeek.png is stored in the \figures folder')
    # Save as .jpg at \figures folder
    if 'jpg' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_MeasDurationPerWeek.jpg"))
        fig.savefig(figPath, format='jpeg', dpi=200, bbox_inches='tight')    
        print(f'The figure {__PROJECTNAME__}_MeasDurationPerWeek.jpg is stored in the \figures folder')
        

    #### Plot the cumulative number of the measurements for each GNSS system ####  
        
    fig = plt.figure()
    ax = plt.gca()
    
    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "yellow", "green"])
    
    plt.bar(df2plot['WOY'], df2plot['CumulativeDuration'], color=cmap(df2plot['CumulativeDuration']/df2plot['CumulativeDuration'].max()))
    
    step = 1
    xMin = df2plot['WOY'].min() 
    xMax = df2plot['WOY'].max() 
    # x-axis ticks
    ax.set_xticks(np.arange(xMin, xMax + step, step=step))
    # x-axis ticklabels
    ax.set_xticklabels(np.arange(xMin, xMax + step, step=step), fontsize = 14)
    # x-axis limits
    ax.set_xlim(xMin - 1, xMax + 1)
    
    # y-axis grid
    ax.yaxis.grid()
    
    # x-axis label
    plt.xlabel('Week of year 2022', fontsize = 18)
    # y-axis label
    plt.ylabel('Cumulative duration of measurements [hr]', fontsize = 18)
       
    # attributes of the figure
    xlength = 12
    fig.set_size_inches(xlength, xlength/1.618)
    
    # show the plot
    plt.show()
    
    
    # Save as .pdf at \figures folder
    if 'pdf' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_CumulativeMeasDuration.pdf"))
        fig.savefig(figPath, format='pdf', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_CumulativeMeasDuration.pdf is stored in the \figures folder')
    # Save as .png at \figures folder
    if 'png' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_CumulativeMeasDuration.png"))
        fig.savefig(figPath, format='png', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_CumulativeMeasDuration.png is stored in the \figures folder')
    # Save as .jpg at \figures folder
    if 'jpg' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_CumulativeMeasDuration.jpg"))
        fig.savefig(figPath, format='jpeg', dpi=200, bbox_inches='tight')    
        print(f'The figure {__PROJECTNAME__}_CumulativeMeasDuration.jpg is stored in the \figures folder')
    
    return 0


            
            
            
            
def plotMeasCountPerWeek(__PROJECTNAME__,
                        file,
                        format = ['jpg']
                        ):
    
    """Plot the cumulative number of the measurements for each GNSS system.
    
    Parameter:
        __PROJECTNAME__ (type str): 
            The folder name in which the CAMALIOT text files are stored. 
        file (type str):               
            The path of the relevant JSON file.
        format (type list)
            The list of the user-defined formats to export the figures.
            It supports only the formats jpg, pdf and png.
        
    Returns: 
        0
    """  

    #### Read data from the JSON file ####
    
    try:
        # Opening JSON file to read
        with open(file, 'r') as inputFile:
            # Read the json file
            dataJSON = json.load(inputFile)
        inputFile.close()
    except:
        print('Problem with opening the JSON file.')
        return 1
        

    #### Restructure data before plotting ####
          
    # list to collect the required data for the plot 
    data2plot = []
    
    # Iterate the imported list of dictionaries
    for item in dataJSON:
        
        # The starting date-time of each measurement session. It is used to compute the respective day of year (DOY) and week of year (WOY)
        date = datetime.datetime.strptime(item['Start date-time'],'%Y-%m-%d %H:%M:%S.%f')
        # The week of year of the measurement session. (It is used in the current implementation to group the data to plot)
        WOY = date.isocalendar()[1]
    
        # List of the aforementioned data
        values2plot = [WOY]
        
        # Add the measurement count per system as imported from the JSON file
        values2plot.extend(list(item['MeasCountPerSystem'].values()))
        
        # Append data to a list
        data2plot.append(values2plot)
        
        
    # Create the header (name of columns) of the dataframe    
    columns2plot = ['WOY']
    columns2plot.extend(list(item['GnssSystems'].values()))
    
    # Create a dataframe with the values to be used in the plot
    df2plot = pd.DataFrame(data2plot, columns=columns2plot)
    # Convert the JSON null (None type) values to numpy NaN values
    df2plot = df2plot.fillna(value=np.nan)
    
    # Group data with respect to the week of year
    df2plot = df2plot.groupby('WOY', as_index=False).agg('sum')
    
    # Create a dataframe that contains all the week numbers for the given interval of the measurement sessions
    dfWOY = pd.DataFrame(range(df2plot['WOY'].min(), df2plot['WOY'].max()+1),
                      columns=['WOY'])
    
    # Create a dataframe in which the weeks of the year that have no measurements will be filled with NaN values
    df2plot = dfWOY.join(df2plot.set_index('WOY'), on='WOY')

    # Convert the numpy NaN values to zeros (0)
    df2plot = df2plot.fillna(0)
    
    # Initialize a dataframe to contain the cumulative values
    df2plotCumulative = pd.DataFrame(df2plot['WOY'])
    
    # Iterate the columns
    for column in df2plot:
        
        if column != 'WOY': # Do not accumulate the WOY values.
            # Accumulate the values for each column
            df2plotCumulative[column] = df2plot[column].cumsum()
    

    #### Make the \figures folder if it does not already exist ####
            
    # Get the \figures directory to save the following figures
    dirPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/"))
    # Make the \figures folder if it does not already exist
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
        
        
     
    #### Plot the cumulative number of the measurements for each GNSS system ####
        
    fig = plt.figure()
    ax = plt.gca()
    
    # Create a colormap
    cmap = ['#c9c9c9',
            '#c5d956',  
            '#ebc03f', 
            '#dd63df', 
            '#ff8262', 
            '#ff6688', 
            '#8d75ff', 
            '#ffa246', 
            ]
    
    x = df2plotCumulative['WOY']
    yBottom = pd.Series([0]*len(x))
    systemList = list(item['GnssSystems'].values())
    
    for i, system in enumerate(systemList):
        y = df2plotCumulative[system]/10**6
        if y.sum() == 0: continue
        # print(i, cmap[i], y.name)
        plt.bar(x, y, bottom = yBottom, color=cmap[i], label=y.name)
        yBottom += y

    
    step = 1
    xMin = df2plot['WOY'].min() 
    xMax = df2plot['WOY'].max() 
    
    # x-axis ticks
    ax.set_xticks(np.arange(xMin, xMax + step, step=step))
    # x-axis ticklabels
    ax.set_xticklabels(np.arange(xMin, xMax + step, step=step), fontsize = 14)
    # x-axis limits
    ax.set_xlim(xMin - 1, xMax + 1)
    
    import matplotlib.ticker as ticker
    
    # Rewrite the y labels
    # y_labels = ax.get_yticks()
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2fM'))

    # ax.xaxis.set_major_formatter(million_formatter)
    
    # y-axis grid
    ax.yaxis.grid()
    
    # x-axis label
    plt.xlabel('Week of year 2022', fontsize = 18)
    # y-axis label
    plt.ylabel('Cumulative number of measurements\nper GNSS system (in millions)', fontsize = 18)
       
    # attributes of the figure
    xlength = 12
    fig.set_size_inches(xlength, xlength/1.618)
    
    # legend
    plt.legend(fontsize = 16)
    
    # show the plot
    plt.show()
    
    # Save as .pdf at \figures folder
    if 'pdf' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_MeasCountPerWeek.pdf"))
        fig.savefig(figPath, format='pdf', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_MeasCountPerWeek.pdf is stored in the \figures folder')
    # Save as .png at \figures folder
    if 'png' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_MeasCountPerWeek.png"))
        fig.savefig(figPath, format='png', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_MeasCountPerWeek.png is stored in the \figures folder')
    # Save as .jpg at \figures folder
    if 'jpg' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_MeasCountPerWeek.jpg"))
        fig.savefig(figPath, format='jpeg', dpi=200, bbox_inches='tight')    
        print(f'The figure {__PROJECTNAME__}_MeasCountPerWeek.jpg is stored in the \figures folder')
          
    return 0          
            







def plotDurationHistogram(__PROJECTNAME__,
                          file,
                          format = ['jpg']
                          ):

    """Plot the histogram of the duration of the sessions.
    
    Parameter:
        __PROJECTNAME__ (type str): 
            The folder name in which the CAMALIOT text files are stored. 
        file (type str):               
            The path of the relevant JSON file.
        format (type list)
            The list of the user-defined formats to export the figures.
            It supports only the formats jpg, pdf and png.
        
    Returns: 
        0
    """

    #### Read data from the JSON file ####
    
    try:
        # Opening JSON file to read
        with open(file, 'r') as inputFile:
            # Read the json file
            dataJSON = json.load(inputFile)
        inputFile.close()
    except:
        print('Problem with opening the JSON file.')
        return 1
        

    #### Restructure data before plotting ####
          
    # list to collect the required data for the plot 
    data2plot = []
    
    # Iterate the imported list of dictionaries
    for item in dataJSON:
        
        # The duration of each measurement session
        Duration = item['Duration [M.f]']
    
        # List of the aforementioned data
        values2plot = [Duration, 
                       ]
        
        # Append data to a list
        data2plot.append(values2plot)
        
        
    # Create the header (name of columns) of the dataframe    
    columns2plot = ['Duration']
    
    # Create a dataframe with the values to be used in the plot
    df2plot = pd.DataFrame(data2plot, columns=columns2plot)
    # Convert the JSON null (None type) values to zeros (0)
    df2plot = df2plot.fillna(0)
    
    
    #### Make the \figures folder if it does not already exist ####
    
    # Get the \figures directory to save the following figures
    dirPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/"))
    # Make the \figures folder if it does not already exist
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
        
        
    #### Plot the histogram of the duration of the sessions ####
    
    fig = plt.figure()
    ax = plt.gca()
    
    plt.hist(df2plot['Duration'], bins=range(0,int(np.ceil(df2plot['Duration'].max())),1), rwidth=0.8, color='#7398da')
      
    # y-axis grid
    ax.yaxis.grid()
    
    # x-axis label
    plt.xlabel('Duration of measurement session [min]', fontsize = 18)
    # y-axis label
    plt.ylabel('Number of sessions', fontsize = 18)
       
    # attributes of the figure
    xlength = 12
    fig.set_size_inches(xlength, xlength/1.618)
    
    # show the plot
    plt.show()
    
    # Save as .pdf at \figures folder
    if 'pdf' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_DurationHistogram.pdf"))
        fig.savefig(figPath, format='pdf', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_DurationHistogram.pdf is stored in the \figures folder')
    # Save as .png at \figures folder
    if 'png' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_DurationHistogram.png"))
        fig.savefig(figPath, format='png', dpi=200, bbox_inches='tight')
        print(f'The figure {__PROJECTNAME__}_DurationHistogram.png is stored in the \figures folder')
    # Save as .jpg at \figures folder
    if 'jpg' in format:
        figPath = os.path.abspath(os.path.join(os.getcwd(), "../figures/", __PROJECTNAME__ + "_DurationHistogram.jpg"))
        fig.savefig(figPath, format='jpeg', dpi=200, bbox_inches='tight')    
        print(f'The figure {__PROJECTNAME__}_DurationHistogram.jpg is stored in the \figures folder')
        
    return 0


# The day of year of the measurement session. (It is not used in the current implementation!)
# DOY = date.timetuple().tm_yday,


