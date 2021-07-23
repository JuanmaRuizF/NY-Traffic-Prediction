from historical_apis.historical_api_traffic import HistoricalApiTraffic
from historical_apis.historical_api_air_quality import HistoricalApiAirQuality
from historical_apis.historical_api_weather import HistoricalApiWeather

import os, datetime, calendar
import pandas as pd
from datetime import datetime as dt

"""
#Llamada a todas las API para obtener los datos históricos. 
Se proporciona la fecha de comienzo, el número de meses a realizar la solicitud de datos y el nombre del directorio en el que serán almacenados los datos
El método hará llamadas una vez terminen las solicitudes para unir todos los archivos de tráfico, calidad del aire y clima por los rangos de fecha
Finalmente se hará una llamada que una todos los archivos resultantes, de tal forma que se obtenga un único archivo con todos los datos unidos para las 3 API
"""

def apisRequest(start_date, months, directory):

    start_datetime = datetime.datetime.strptime(start_date,"%Y-%m-%dT%H:%M:%S") 
    end_datetime = start_datetime + datetime.timedelta(days=14, hours= 23, seconds=3599)
    end_datetime = str(end_datetime).replace(" ","T")
    start_datetime = str(start_datetime).replace(" ","T")

    path_file = os.getcwd() + '/data/historical_data/merge_historical/' + directory

    if os.path.exists(path_file):
        print("El nombre de la carpeta ya existe. Pon otro nombre")
        return
    else:
        os.mkdir(path_file) #crea el directorio donde se almacenarán las uniones de los archivos

    output_name = f"\\historical_data_{directory}.csv"

    count = 0
    num = months*2  #como se hacen peticiones cada 15 días, se itera sobre 2*número de meses
    while count < num:  
        #peticiones a las distintas API
        HistoricalApiTraffic().traffic_historical(10000000, start_datetime, end_datetime)
        HistoricalApiAirQuality().air_quality_historical(start_datetime, end_datetime)
        HistoricalApiWeather().weather_historical(start_datetime, end_datetime)
        res = start_datetime[0:13] + "_to_" + end_datetime[0:13]
        mergeByDatetime(path_file, res) #unión de los resultados de las API por fecha y hora

        start_datetime = dt.strptime(str(end_datetime), "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(seconds = 1)
        #se comprueba que las fechas estén bien para seguir iterando
        if start_datetime.day == 1:
            plus = 14
        else:
            res = calendar.monthrange(start_datetime.year, start_datetime.month)
            plus = res[1] - 16
      
        end_datetime =  start_datetime + datetime.timedelta(days=plus, hours= 23, seconds=3599)

        start_datetime = str(start_datetime).replace(" ","T")
        end_datetime = str(end_datetime).replace(" ","T")
        count += 1
    #una vez se tiene con todas las uniones de los archivos por fecha y hora, se hace una unión de todos los archivos de ese directorio para tener un
    #archivo único con la unión de los datos históricos
    mergeFilesWithLocation(path_file, output_name)


#hace la unión de los archivos que tengan el mismo rango de fecha y los une en un archivo nuevo por la fecha.
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
  

#une todos los archivos dentro de un directorio
def mergeFilesWithLocation(location, output_name):

    path = location #ruta para la unión de los archivos
    dirs = os.listdir(path) #archivos dentro del directorio de unión
    df = pd.DataFrame()
    print("*"*100)
    #si se encuentra algún archivo que no queramos unir, se añade a la lista de undesired_paths
    undesired_paths = [""]
    
    for file in dirs:
        if file in undesired_paths:
            continue #si el archivo es de los no deseados, continuará
        else:
            file = path +"\\" + file #acceder al archivo en cuestión
            df_concat = pd.read_csv(file, low_memory=False) #apertura del archivo
            df = pd.concat([df,df_concat]) #el archivo es unido al dataframe con todos los archivos
            print("write: " + file) #mensaje de validación para la unión

    print(f'Número total de filas: {df.shape[0]}') 
    #el archivo de unión es guardado en el directorio dado por parámetro.
    output_csv =  location + output_name
    df.to_csv(output_csv, index=False)

