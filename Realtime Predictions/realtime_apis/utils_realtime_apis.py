import pytz, os,     csv
from datetime import datetime as dt
from datetime import timedelta as timedelta

#métodos que son utilizados por los distintos archivos de solicitudes a las API en tiempo real
class UtilsRealtimeApis():

    def get_format_datetime(self):
        return "%Y-%m-%dT%H:%M:%S"

    def get_str_ny(self):
        return 'America/New_York'

    def convert_time_str(self, time, from_time, to_time):
        from_time = pytz.timezone(from_time)
        to_time = pytz.timezone(to_time)
        format_datetime = UtilsRealtimeApis().get_format_datetime()

        res = dt.strptime(time, format_datetime)
        res = from_time.localize(res)
        res = res.astimezone(to_time)
        res = res.strftime(format_datetime)
        return res

    #método que devuelve la diferencia entre la fecha local en NY y la fecha pasada por parámetro
    def difference_datetime(self, datetime_value):
        my_class = UtilsRealtimeApis()
        tz_ny = pytz.timezone(my_class.get_str_ny()) 
        format_datetime = my_class.get_format_datetime()
        current_datetime = dt.now(tz_ny)
        current_datetime = dt.strptime(str(current_datetime)[0:-13],"%Y-%m-%d %H:%M:%S")
        datetime_value = dt.strptime(datetime_value, format_datetime)
        return current_datetime - datetime_value

    def get_lists(self):    #lista con los datos que se desea de cada una de las API
        list_traffic = ["datetime","datetime_traffic","weekday","speed","travel_time","link_name"]
        list_airQuality = ["datetime","AQI_PM2.5","Parameter_PM2.5","Unit_PM2.5","Value_PM2.5","Category_PM2.5","AQI_OZONE","Parameter_OZONE","Unit_OZONE","Value_OZONE","Category_OZONE"]
        list_weather = ["datetime","Minimum Temperature","Maximum Temperature","Temperature","Dew Point","Relative Humidity","Heat Index","Wind Speed","Wind Gust","Wind Direction","Wind Chill","Precipitation","Precipitation Cover","Snow Depth","Visibility","Cloud Cover","Sea Level Pressure","Conditions"]
        list_merge = list_traffic + list_airQuality[1:] + list_weather[1:]
        return list_traffic, list_airQuality, list_weather, list_merge

    def get_realtime_apis_file_directions(self):    #ubicación de los archivos donde se almacenan los datos obtenidos en tiempo real

        current_dir = os.getcwd() + "/data/realtime_data"

        merge_file = current_dir + "/apis_data/merge.csv"
        traffic_file = current_dir + "/apis_data/traffic.csv"
        air_quality_file = current_dir + "/apis_data/airQuality.csv"
        weather_file = current_dir + "/apis_data/weather.csv"

        return merge_file, traffic_file, air_quality_file, weather_file

    """ fileCreator:
        *** recibe una direccion/path @file_name y una lista @list con nombres de columnas
        - Si el archivo @file_name no existe
            *entonces lo crea y le asigna @list como cabecera
    """
    def file_creator(self, file_name, list): 
        print("file_creator: ", file_name)

        file = open(file_name, 'w')
        with file:
            writer = csv.DictWriter(file, fieldnames = list)
            writer.writeheader()