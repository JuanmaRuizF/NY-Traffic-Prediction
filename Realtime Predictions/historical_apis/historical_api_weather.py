import pandas as pd
import os, requests, io

class HistoricalApiWeather:
    #Método que se conecta con la API de clima y guarda datos en un rango de fecha en hora de Nueva York
    def weather_historical(self, start_datetime, end_datetime):

        start_datetime= start_datetime[0:-5] + "00:00"

        # obtener los datos de la API según las condiciones específicas (ej:valores de Manhattan)
        url = "https://visual-crossing-weather.p.rapidapi.com/history"
        querystring = {"startDateTime":f"{start_datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","endDateTime":f"{end_datetime}","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}
    
        headers = { #clave con la que hacer las peticiones a la API
            'x-rapidapi-key': "c7e1b16b1dmsh0c4a9ad78b63e34p12d779jsn456dc589d5cd",
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }
        response = requests.request("GET",url, headers=headers, params = querystring)  #respuesta de la API
        results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        #se guardan los datos en el formato querido y se eliminan aquellas columnas que no serán utilizadas
        results_df["Date time"] = pd.to_datetime(results_df["Date time"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
        results_df = results_df.rename(columns={"Date time": "datetime"}) 
        results_df = results_df.drop(["Address","Latitude","Longitude","Resolved Address","Name","Info", "Weather Type"], axis=1)

        results_df["Conditions"]= results_df["Conditions"].str.replace(",", "")

        #guardando datos obtenidos en csv en el directorio correspondiente
        file_name = os.getcwd() + f"/data/historical_data/data_without_merge/weather_historical/weather_historical_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"
        results_df.to_csv(file_name, index=False)

        print(f"HistoricalApiWeather: {file_name}")