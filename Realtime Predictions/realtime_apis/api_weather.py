import pandas as pd
import requests, io
from datetime import datetime as dt
from datetime import timedelta as timedelta
from realtime_apis.utils_realtime_apis import UtilsRealtimeApis

class ApiWeather:
     #Método que se conecta con la API de clima y guarda datos para la fecha solicitada (hora de Nueva York)
    def weather_data_ingestion(self, start_datetime, file_dir):
        utils = UtilsRealtimeApis()
        datetime= start_datetime[0:-5] + "00:00"
        #como se hacen bastantes solicitudes a este método porque es ejecutado constantemente en tiempo real, se proporcionan dos keys
        if int(datetime[8:10]) < 15:
            key = "" #ADD KEY 1 FROM https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather/
        else: 
            key = "" #ADD KEY 2 FROM https://rapidapi.com/visual-crossing-corporation-visual-crossing-corporation-default/api/visual-crossing-weather/

        # obtener los datos de la API según las condiciones específicas (ej:valores de Manhattan)
        url = "https://visual-crossing-weather.p.rapidapi.com/history"
        querystring = {"startDateTime":f"{datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}
    
        headers = { #clave con la que hacer las peticiones a la API
            'x-rapidapi-key': key,
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }
        response = requests.request("GET",url, headers=headers, params = querystring)  
    
        results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

        res = utils.difference_datetime(start_datetime)
        date_format = utils.get_format_datetime()

        if results_df.empty or str(results_df.loc[0,"Info"]) == "No data available":
            #si han pasado más de 3 horas (10800seg) y sigue estando vacía la respuesta, se pasa a la se consulta para la hora anterior
            if res.seconds > 10800:

                start_ = dt.strptime(start_datetime, date_format)  - timedelta(hours=1)
                ApiWeather().weather_data_ingestion(str(start_).replace(" ", "T"), file_dir)
                
                result= pd.read_csv(file_dir)
                result["datetime"] = pd.to_datetime(result["datetime"])
                result.loc[0,"datetime"] = result.loc[0,"datetime"] + timedelta(hours=1)
                result["datetime"] =  result["datetime"].dt.strftime(date_format)
                result.to_csv(file_dir, index = False)
                
                print(f"WeatherApi.empty: {start_datetime}")
                return True
            return False
        
         #se guardan los datos en el formato querido y se eliminan aquellas columnas que no serán utilizadas
        str_datetime = "Date time"
        results_df[str_datetime] = pd.to_datetime(results_df[str_datetime]).dt.strftime(date_format)
        results_df = results_df.rename(columns={str_datetime: "datetime"}) 
        results_df = results_df.drop(["Address","Latitude","Longitude","Resolved Address","Name","Info", "Weather Type"], axis=1)
        
        results_df["Conditions"]= results_df["Conditions"].str.replace(",", "")

        ##guardando datos obtenidos en csv en el directorio correspondiente
        results_df.to_csv(file_dir, index=False)

        print(f"WeatherApi: {file_dir}")
        return True
