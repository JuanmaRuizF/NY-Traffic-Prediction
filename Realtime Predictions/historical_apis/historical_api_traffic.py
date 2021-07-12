import pandas as pd
from sodapy import Socrata
import os

class HistoricalApiTraffic:
    #Date tiene que ser de formato: yyyy-mm-ddThh:mm:ss
    def traffic_historical(self, datalimit, start_datetime, end_datetime):

        # Unauthenticated client only works with public data sets. Note 'None'
        # in place of application token, and no username or password:
        client = Socrata("data.cityofnewyork.us", None)

        # First dataLimit results, returned as JSON from API / converted to Python list of
        # dictionaries by sodapy.
        date = f"data_as_of between '{start_datetime}' and '{end_datetime}'"
        print(date)
        
        columns = "data_as_of, id, speed, travel_time, link_name"

        results = client.get("i4gi-tjb9", limit = datalimit, borough = "Manhattan", where = date, select = columns)
        
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
    
        #-----------------------------------------datetime - time_hour --------------------------------------#
        results_df["datetime"] = results_df["data_as_of"].str[:-9] + "00:00"
        results_df["datetime_traffic"] = results_df["data_as_of"].str[:-4]
        
        results_df["datetime"] = pd.to_datetime(results_df["datetime"])
        results_df["datetime_traffic"] = pd.to_datetime(results_df["datetime_traffic"])
        results_df["weekday"] = results_df['datetime'].dt.day_name()

        results_df = results_df[["datetime", "datetime_traffic", "weekday", "speed", "travel_time", "link_name"]]
    
        #guardando -----------------------------------------------------------------------------------------
        file_name = os.getcwd() + f"/data/historical_data/data_without_merge/traffic_historical/traffic_historical_{start_datetime[0:13]}_to_{end_datetime[0:13]}.csv"

        results_df.to_csv(file_name, index=False)
        print(f"HistoricalApiTraffic: {file_name}")





