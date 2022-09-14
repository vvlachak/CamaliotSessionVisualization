


# CamaliotSessionVisualization

  
*CamaliotSessionVisualization* is a simple tool, developed in Python, aiming to:

- extract information from the CAMALIOT text files, such as the location, duration and number of measurements per session,
- visualize (bar charts and histograms) the temporal distribution of the measurements, and
- facilitate the visualization of the spatial distribution of the session measurements.


### Table Of Content

[Introduction](#introduction)

- [What is CAMALIOT?](#what-is-camaliot)
- [Raw data](#raw-data)
- [Data processing](#data-processing)
- [Plots](#plots)
 
[User guide](#user-guide)


## Introduction

### What is CAMALIOT?

According to [this publication][Publication1], **CAMALIOT** (Appli**ca**tion of **Ma**chine **L**earning Technology for GNSS **IoT** data fusion) is an ongoing project funded by the European Space Agency (ESA) that aims to collect large amounts of GNSS observations by developing an Android application and conducting a dedicated crowdsourcing campaign.

More information about the CAMALIOT project can be found in [this article][ETHZ news] and in the [official webpage of CAMALIOT][CAMALIOT.org].

The first crowdsourcing campaign started on 17 March 2022 and ended on 31 July 2022, while on 1 August 2022 the Autumn campaign has started!

Through a *citizen science* approach anyone can download the free app and collect data (ideally while keeping the phone static and with a good view of the sky) and then upload the data to the CAMALIOT server.

### Raw data

The CAMALIOT app data files contain information in two different structures:
1. ```# Fix, Provider, Latitude, Longitude, Altitude, Speed, Accuracy, (UTC)TimeInMs```\
e.g.,\
```Fix, gps, 46.206899, 6.156595, 421.961243, 0.000000, 9.935046, 1648646790000```
  
2. ```# Raw, ElapsedRealtimeMillis, TimeNanos, LeapSecond, TimeUncertaintyNanos, FullBiasNanos, BiasNanos, BiasUncertaintyNanos, DriftNanosPerSecond, DriftUncertaintyNanosPerSecond, HardwareClockDiscontinuityCount, Svid, TimeOffsetNanos, State, ReceivedSvTimeNanos, ReceivedSvTimeUncertaintyNanos, Cn0DbHz, PseudorangeRateMetersPerSecond, PseudorangeRateUncertaintyMetersPerSecond, AccumulatedDeltaRangeState, AccumulatedDeltaRangeMeters, AccumulatedDeltaRangeUncertaintyMeters, CarrierFrequencyHz, CarrierCycles, CarrierPhase, CarrierPhaseUncertainty, MultipathIndicator, SnrInDb, ConstellationType, AgcDb```\
e.g.,\
```Raw, 28189020, 11232846000000, 18, , -1332670773582635432, 0.8295364379882812, 22.152808014652692, -5.098334209574816, 9.629362666402953, 2, 35, 0.0, 16399, 307592340631009, 6, 30.3, -608.1038818359375, 0.07541361451148987, 16, 0.0, 0.0, 1.17645005E9, , , , 0, , 5, 0.26```

The data files are stored in the following directory in the mobile phone: ```../Android/data/com.iiasa.camaliot/files``` and the filenames follow the format: ```camaliot_app_log_YYYY_MM_DD_HH_MM_SS.txt```

These files should be copied in a subdirectory of the ```data``` folder of the *CamaliotSessionVisualization* tool (see [User guide](#user-guide)).

### Data processing

In the current implementation of the *CamaliotSessionVisualization* tool only a few of the collected data are used.

From the `# Fix`data structure, it uses:
- the first (or minimum) value of the `(UTC)TimeInMs` parameter of each session, which is considered as the starting time,
- the last (or maximum) value of the `(UTC)TimeInMs` parameter of each session, which is considered as the ending time,
- the median of the `Latitude` parameter, which is considered to be a representative latitude of the static position, and
- the median of the `Longitude` parameter, which is considered to be a representative latitude of the static position.- 

From the `# Raw`data structure, it uses:
- the `constellationType` parameter that indicates the GNSS system that was used for each measurement according to the following [GnssConstellationType Enum:][GnssConstellationType Enum]
	
	*0: UNKNOWN\
	1: GPS\
	2: SBAS\
	3: GLONASS\
	4: QZSS\
	5: BEIDOU\
	6: GALILEO\
	7: IRNSS*

The aforementioned parameters are used to create the following data structure for each measurement session and store it in a JSON file.

Example of the data structure for each measurement session:
```python
{
    "Start date-time": "2022-03-26 17:17:44.688000",
    "Duration [MM:SS]": "10:29",
    "Duration [M.f]": 10.4885,
    "Latitude (median) [deg]": 36.197195,
    "Longitude (median) [deg]":16.123804,
    "TotalCountOfMeas": 15468,
    "GnssSystems": {
        "0": "UNKNOWN",
        "1": "GPS",
        "2": "SBAS",
        "3": "GLONASS",
        "4": "QZSS",
        "5": "BEIDOU",
        "6": "GALILEO",
        "7": "IRNSS"
    },
    "MeasCountPerSystem": {
        "0": null,
        "1": 4976.0,
        "2": null,
        "3": 4117.0,
        "4": null,
        "5": 6375.0,
        "6": null,
        "7": null
    },
    "MeasPercentagePerSystem": {
        "0": null,
        "1": 0.32,
        "2": null,
        "3": 0.27,
        "4": null,
        "5": 0.41,
        "6": null,
        "7": null
    }
}
```
Obviously, a large part of the information that is stored in the JSON file is redundant (and may be omitted in the next update), however, it increases the readability of the data in the JSON file.
  

### Plots

*CamaliotSessionVisualization* can be used to create four plots:

1. #### The duration of the measurements per week.
	![Example plot1][plot1]

2. #### The cumulative duration of the measurements per week.
	![Example plot2][plot2]

3. #### The cumulative number of the measurements for each GNSS system.
	![Example plot3][plot3]
	
4. #### The histogram of the duration of the sessions. 
	![Example plot4][plot4]
	

## User guide

  






[Publication1]: https://pure.iiasa.ac.at/id/eprint/18035/
  
[ETHZ news]: https://baug.ethz.ch/en/news-and-events/news/2022/03/use-your-cellphone-to-improve-weather-forecasts.html?fbclid=IwAR1IKgfewtl94-H9P2ONsSXzvFw-rgzQ6gFAOD9mFa0elU9u0yCeCZrxzus

[CAMALIOT.org]: https://www.camaliot.org/
  
[GnssConstellationType Enum]: https://docs.microsoft.com/en-us/dotnet/api/android.locations.gnssconstellationtype?view=xamarin-android-sdk-12

[plot1]: https://github.com/vvlachak/CamaliotSessionVisualization/blob/main/figures/testDataSet_MeasDurationPerWeek.jpg
[plot2]: https://github.com/vvlachak/CamaliotSessionVisualization/blob/main/figures/testDataSet_CumulativeMeasDuration.jpg
[plot3]: https://github.com/vvlachak/CamaliotSessionVisualization/blob/main/figures/testDataSet_MeasCountPerWeek.jpg
[plot4]: https://github.com/vvlachak/CamaliotSessionVisualization/blob/main/figures/testDataSet_DurationHistogram.jpg
  

  
  
  
  
  
  
  
  

## Folder structure
```
CamaliotSessionVisualization
└───data
|   └───testDataSet
│       │   camaliot_app_log_YYYY_MM_DD_HH_MM_SS.txt
│       |   ...
└───figures
|   |   *.png
|   |   *.pdf
|   |   *.jpg
└───source
└───...
```

  
  
  
  
  
  