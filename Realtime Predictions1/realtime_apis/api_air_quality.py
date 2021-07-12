import pandas as pd
import json, urllib3, certifi
from datetime import datetime as dt
from datetime import timedelta as timedelta
from realtime_apis.utils_realtime_apis import UtilsRealtimeApis 

class ApiAirQuality:
    ##Método que se conecta con la api y guarda datos en un rango de fecha excluye la primera linea --------
    def air_quality_data_ingestion(self, start_datetime, file_dir):
        utils = UtilsRealtimeApis()
        format_datetime = utils.get_format_datetime()
        str_ny = utils.get_str_ny()
        #pasando hora de NY a UTC para hacer la solicitud a la hora deseada
        hour_datetime = utils.convert_time_str(start_datetime, str_ny, 'UTC')[0:13]
        
        # handle certificate verification and SSL warnings
        # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

        # get data from the API
        url = f"https://www.airnowapi.org/aq/data/?startDate={hour_datetime}&endDate={hour_datetime}&parameters=OZONE,PM25&BBOX=-74.020308,40.700155,-73.940657,40.827572&dataType=B&format=application/json&verbose=0&nowcastonly=0&includerawconcentrations=0&API_KEY=7FD50518-C721-4C9A-861F-883367594091"
        response = http.request('GET', url)
        
        # decode json data into a dict object
        data = json.loads(response.data.decode('utf-8'))
        results_df = pd.DataFrame(data)
        
        res = utils.difference_datetime(start_datetime)
        
        if results_df.empty:
            #si han pasado mas de dos horas y sigue estando vacio se pasa a la se consulta para la hora anterior
            if res.seconds > 7200:

                start_ = dt.strptime(start_datetime, format_datetime)  - timedelta(hours=1)
                ApiAirQuality().air_quality_data_ingestion(str(start_).replace(" ", "T"), file_dir)
                
                result= pd.read_csv(file_dir)
                result["datetime"] = pd.to_datetime(result["datetime"])
                result.loc[0,"datetime"] = result.loc[0,"datetime"] + timedelta(hours=1)
                result["datetime"] =  result["datetime"].dt.strftime(format_datetime)
                result.to_csv(file_dir, index = False)
                
                print(f"AirQualityApi.empty: {start_datetime}")
                return True

            return False
    
        try:
            results_df.loc[1, "Parameter"]
        except:
            if res.days <= 0 and res.seconds <= 7200:      
                    return False
    
        results_df = results_df.rename(columns={"UTC": "datetime"}) 
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        
        results_df = results_df[["datetime", "AQI", "Parameter", "Unit", "Value", "Category"]]
    
        results_df["datetime"] = results_df["datetime"].dt.tz_localize('UTC').dt.tz_convert('America/New_York').dt.strftime("%Y-%m-%dT%H:%M:%S")

        pm25_df = results_df.drop(results_df[results_df['Parameter']=="OZONE"].index)
        ozone_df = results_df.drop(results_df[results_df['Parameter']=="PM2.5"].index)

        #se guardan los valores en una sola fila por hora
        air_quality_df = pd.merge(pm25_df, ozone_df, on = "datetime", how = "outer", suffixes= ("_PM2.5", "_OZONE"))
        #aseguramos guardar valor en orden de fecha
        air_quality_df = air_quality_df.sort_values("datetime")

        #data saving as csv
        air_quality_df.to_csv(file_dir, index=False)

        print(f"AirQualityApi: {file_dir}")
        return True
    