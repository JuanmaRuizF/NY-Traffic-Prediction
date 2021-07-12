import pandas as pd
import os, requests, io

class HistoricalApiWeather:
    ##Metodo que se conecta con la api y guarda datos en un rango de fecha en NY time--------------------------------------------
    def weather_historical(self, start_datetime, end_datetime):

        start_datetime= start_datetime[0:-5] + "00:00"

        # get data from the API
        url = "https://visual-crossing-weather.p.rapidapi.com/history"
        querystring = {"startDateTime":f"{start_datetime}","aggregateHours":"1","location":"Manhattan,NY,USA","endDateTime":f"{end_datetime}","unitGroup":"us","dayStartTime":"0:00:00","contentType":"csv","dayEndTime":"23:59:59","shortColumnNames":"0"}
    
        headers = {
            'x-rapidapi-key': "564857dda0msh05f30bc625bcd3ep1c10a8jsndf47856ab143",
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }
        response = requests.request("GET",url, headers=headers, params = querystring)  
        results_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        
        #tipografia de los datos,  -----------------------------------------------
        results_df["Date time"] = pd.to_datetime(results_df["Date time"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
        results_df = results_df.rename(columns={"Date time": "datetime"}) 
        results_df = results_df.drop(["Address","Latitude","Longitude","Resolved Address","Name","Info", "Weather Type"], axis=1)

        results_df["Conditions"]= results_df["Conditions"].str.replace(",", "")

        #guardando datos obtenidos en csv 
        file_name = os.getcwd() + f"/data/historical_data/data_without_merge/weather_historical/weather_historical_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"
        results_df.to_csv(file_name, index=False)

        print(f"HistoricalApiWeather: {file_name}")