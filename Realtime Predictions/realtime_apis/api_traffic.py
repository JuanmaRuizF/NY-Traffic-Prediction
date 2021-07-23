# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata
from realtime_apis.utils_realtime_apis import UtilsRealtimeApis

class ApiTraffic:
    #Date tiene que ser de formato: yyyy-mm-ddThh:mm:ss
    #devuelve false si el dataframe está vacío y true si se escribe algo
    def traffic_data_ingestion(self, datalimit, start_datetime, file_dir):
        utils = UtilsRealtimeApis()
        # El cliente no autenticado solo funciona con conjuntos de datos públicos. Por ello se pone "None"
        # n lugar del token de la aplicación, y sin nombre de usuario ni contraseña:
        client = Socrata("data.cityofnewyork.us", None)

        date = f"data_as_of>'{start_datetime}'"  #se define la fecha de inicio de la consulta que es la hora solicitada en el realtime
        date = date.replace(" ", "T")
        # print(date)
        
        columns = "data_as_of, speed, travel_time, link_name"  #columnas solicitadas a la API

        #configuración de las columnas a extraer del tráfico y las condiciones
        results = client.get("i4gi-tjb9", limit=datalimit, borough = "Manhattan", where = date, select = columns) 
        
        # convertir los resultados a dataframe
        results_df = pd.DataFrame.from_records(results)
        
        if results_df.empty:    #si no se ha obtenido ningún resultado
            return False
        #preparación y creación de la columna datetime, datetime_traffic y weekday
        results_df["datetime"] = results_df["data_as_of"].str[:-9] + "00:00"
        results_df["datetime_traffic"] = results_df["data_as_of"].str[:-4]
        
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        results_df["weekday"] = results_df['datetime'].dt.day_name()
        results_df["datetime"] = results_df["datetime"].dt.strftime(utils.get_format_datetime())

        results_df = results_df[["datetime", "datetime_traffic", "weekday", "speed", "travel_time", "link_name"]]

        #se guarda en la direccion del archivo pasado como parametro
        results_df.to_csv(file_dir, index=False)
        print(f"TrafficApi: {file_dir}")
        return True



