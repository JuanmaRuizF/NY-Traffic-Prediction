from historical_apis.historical_api_traffic import HistoricalApiTraffic
from historical_apis.historical_api_air_quality import HistoricalApiAirQuality
from historical_apis.historical_api_weather import HistoricalApiWeather
# from historical_api_traffic import HistoricalApiTraffic
# from historical_api_air_quality import HistoricalApiAirQuality
# from historical_api_weather import HistoricalApiWeather

import os, datetime, calendar
import pandas as pd
from datetime import datetime as dt

print(os.getcwd() + '/data/historical_data/merge_historical')
def apisRequest(start_date, months, directory):

    start_datetime = datetime.datetime.strptime(start_date,"%Y-%m-%dT%H:%M:%S")
    end_datetime = start_datetime + datetime.timedelta(days=14, hours= 23, seconds=3599)
    end_datetime = str(end_datetime).replace(" ","T")
    start_datetime = str(start_datetime).replace(" ","T")
    print(end_datetime[0:19])

    path_file = os.getcwd() + '/data/historical_data/merge_historical/' + directory
    #print(path)
    if os.path.exists(path_file):
        print("Select another name for the folder")
        return
    else:
        os.mkdir(path_file)

    output_name = f"\\historical_data_{directory}.csv"
    print(path_file)

    count = 0
    num = months*2
    while count < num:  

        HistoricalApiTraffic().traffic_historical(10000000, start_datetime, end_datetime)
        HistoricalApiAirQuality().air_quality_historical(start_datetime, end_datetime)
        HistoricalApiWeather().weather_historical(start_datetime, end_datetime)
        res = start_datetime[0:13] + "_to_" + end_datetime[0:13]
        mergeByDatetime(path_file, res)

        start_datetime = dt.strptime(str(end_datetime), "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(seconds = 1)
      
        if start_datetime.day == 1:
            plus = 14
        else:
            res = calendar.monthrange(start_datetime.year, start_datetime.month)
            plus = res[1] - 16
      
        end_datetime =  start_datetime + datetime.timedelta(days=plus, hours= 23, seconds=3599)

        start_datetime = str(start_datetime).replace(" ","T")
        end_datetime = str(end_datetime).replace(" ","T")
        count += 1

    mergeFilesWithLocation(path_file, output_name)

def mergeByDatetime(path_file, datetime):

    data_folder = os.getcwd() + "/data/historical_data/data_without_merge"

    traffic_file = data_folder + f"/traffic_historical/traffic_historical_{datetime}.csv"
    airQuality_file = data_folder + f"/air_quality_historical/air_quality_historical_{datetime}.csv"
    weather_file = data_folder + f"/weather_historical/weather_historical_{datetime}.csv"
    print(path_file)
    pepe = f"/merge_{datetime}.csv"
    print(pepe)
    file_name = path_file + f"/merge_{datetime}.csv"

    traffic_df = pd.read_csv(traffic_file)
    airQuality_df = pd.read_csv(airQuality_file)
    weather_df = pd.read_csv(weather_file)

    traffic_df["datetime"] = pd.to_datetime(traffic_df["datetime"])
    airQuality_df["datetime"] = pd.to_datetime(airQuality_df["datetime"])
    weather_df["datetime"] = pd.to_datetime(weather_df["datetime"])
   
    df = pd.merge(traffic_df,airQuality_df, how= 'outer', on = 'datetime', suffixes= ('_TRAFFIC', '_AIR'))
    df = pd.merge(df, weather_df, how="outer", on="datetime", suffixes= ('','_WEATHER'))
    
    df = df.sort_values("datetime_traffic")

    df.to_csv(file_name,index=False)

    print(f"Merge - Traffic, Air Quality, Weather: {file_name}")
  

def mergeFilesWithLocation(location, output_name):

    path = location #path to merge files
    dirs = os.listdir(path) #files in that directory
    df = pd.DataFrame()
    print("*"*100)
    #this are other folders contained in the location we want to merge the files from. This way they won't be taken into consideration when merging all files.
    undesired_paths = [""]
    
    for file in dirs:
        if file in undesired_paths:
            continue #if file is in the undesired_paths it will continue and not merge
        else:
            file = path +"\\" + file #iterating through all the files in the directory
            df_concat = pd.read_csv(file, low_memory=False) #opening the file to concatenate 
            df = pd.concat([df,df_concat]) #merging the file to the dataframe
            print("write: " + file) #validation message

    print(df.shape[0]) 

    #saving the file with the name given in the parameters with all the merged files
  
    output_csv =  location + output_name
    df.to_csv(output_csv, index=False)


#apisRequest("2019-07-01T00:00:00", 23, "2019_2020_2021")

# apisRequest("2019-07-01T00:00:00", 1, "2019_2020_2021AAAA")

