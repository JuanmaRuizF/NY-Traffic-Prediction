from datetime import datetime as dt
from datetime import timedelta as timedelta
from realtime_apis.api_traffic import ApiTraffic
from realtime_apis.api_air_quality import ApiAirQuality
from realtime_apis.api_weather import ApiWeather
from realtime_apis.utils_realtime_apis import UtilsRealtimeApis
import pandas as pd
import threading, time, os, pytz
from preprocessData import PreprocessData
from predictions import predictions
from value_comparison import value_comparison



class MainRealtimeApis:

    """ DEFINICIÓN DE VARIABLES EN EL CONSTRUCTOR:
    Se registra la hora de ejecución
    Se guardan en variables las rutas de los archivos
    Se guardan en listas las cabeceras para cada archivo
    """
 
    file = os.getcwd() + "/data/realtime_data/apis_data/merge.csv"
    def __init__(self):

        self.utils = UtilsRealtimeApis()

        self.format_datetime = self.utils.get_format_datetime()
        tz_NY = pytz.timezone('America/New_York') 
        self.ini_datetime = dt.now(tz_NY).strftime(self.format_datetime)
        self.ini_datetime = self.ini_datetime[:-5] + "00:00"
        self.next_iter_air_quality = False
        self.next_iter_weather = False
        self.traffic_iter_time = 5*60

        self.merge_file, self.traffic_file, self.air_quality_file, self.weather_file = self.utils.get_realtime_apis_file_directions()
        self.list_traffic, self.list_air_quality, self.list_weather, self.list_merge = self.utils.get_lists()


    """ MÉTODOS PARA LLAMAR A LAS APIS
    """
    def traffic_api(self, iter_time, limit):
        print("traffic: executed")

        api_traffic = ApiTraffic()
        self.traffic_iter_time = iter_time
        """ 
            -- mientras método de API retorne falso se espera
            -- cuando método de API retorna verdadero se escribe el valor en merge y se empieza a iterar
        """  
        while not api_traffic.traffic_data_ingestion(limit, self.input_datetime, self.traffic_file):
            print("traffic: file not found - waiting for new values")
            time.sleep(iter_time)

        write_thread = threading.Thread(target=self.write, args = (self.traffic_file,) )
        write_thread.start()
        time.sleep(15)
        
        """ Se empieza a iterar
            -- los valores para la consulta a la api se toman del último valor registrado en el archivo merge
        """

        while True:
            traffic= pd.read_csv(self.merge_file)     #se lee el último valor (última hora) registrada en el archivo de tráfico
            datetime = traffic.loc[traffic.index[-1], "datetime_traffic"]
            print(f"traffic: call {datetime}")
            
            while not api_traffic.traffic_data_ingestion(limit, datetime, self.traffic_file):
                print("traffic: WAITING FOR NEW VALUES")
                time.sleep(iter_time)
            
            write_thread = threading.Thread(target=self.write, args = (self.traffic_file,) )
            write_thread.start()
            time.sleep(10)

    """ Calidad de aire y Clima:
        Se consultan datos que se traen por hora
        --Al registrarlos en merge:
            * La fecha consultada debe ser menor que la fecha del último registro para tráfico en merge
            * Si se detecta un salto temporal en los datos de tráfico se introduce la línea en orden sin datos de tráfico
            * APIS - Si no hay valores para una Fecha y han pasado más de 2 horas se guarda el valor anterior

        --Se toma la hora de ejecución y a medida que se rellenen los datos se le va sumando 1 hora para buscar y traer los datos de la hora siguiente

    """
    def weather_api(self, iter_time):
        print("weather: executed")
        api_weather = ApiWeather()

        start_datetime = self.input_datetime 
    
        while True:
            print(f"weather: call {start_datetime}")
            time.sleep(15)
            while not api_weather.weather_data_ingestion(start_datetime, self.weather_file):
                print(f"weather: WAITING FOR NEW VALUES FOR WEATHER")
                time.sleep(iter_time)
            
            write_thread = threading.Thread(target=self.write, args = (self.weather_file, self.merge_file, self.list_weather) )
            write_thread.start()
            time.sleep(15)
        
            while not self.next_iter_weather:
                    print(f"weather: WAITING TO NEW VALUES FOR TRAFFIC {start_datetime}")
                    time.sleep(self.traffic_iter_time)
                    write_thread = threading.Thread(target=self.write, args = (self.weather_file, self.merge_file, self.list_weather) )
                    write_thread.start()
                    time.sleep(10)
            
            self.next_iter_weather = False
            start_datetime = dt.strptime(str(start_datetime), self.format_datetime) + timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")

    def air_api(self, iter_time):
        print("air: executed")
        api_air_quality = ApiAirQuality()

        start_datetime = self.input_datetime

        while True:
            print(f"air: call {start_datetime}")
            time.sleep(20)
            while not api_air_quality.air_quality_data_ingestion(start_datetime, self.air_quality_file):
                print(f"air: WAITING TO NEW VALUES FOR air_quality")
                time.sleep(iter_time)
            
            write_thread = threading.Thread(target=self.write, args = (self.air_quality_file, self.merge_file, self.list_air_quality) )
            write_thread.start()
            time.sleep(15)
            while not self.next_iter_air_quality:
                    print(f"air: WAITING TO NEW VALUES FOR TRAFFIC {start_datetime}")
                    time.sleep(self.traffic_iter_time)
                    write_thread = threading.Thread(target=self.write, args = (self.air_quality_file, self.merge_file, self.list_air_quality) )
                    write_thread.start()
                    time.sleep(10)
            
            self.next_iter_air_quality = False
            start_datetime = dt.strptime(str(start_datetime), self.format_datetime) + timedelta(hours=1)
            start_datetime = str(start_datetime).replace(" ","T")


    """ write:
        *** recibe dos direcciones de archivos @file_name,  @merge_file_used y una lista @list con nombres de columnas
        - Si el @file_name es el correspondiente a tráfico
            *se registran los nuevos valores
        - Si @merge_file_used esta en blanco
            *se devuelve false y se sale del método
        - else
            *Se llama al metodo fileConcatMerge
                se devuelve el resultado de la llamada
    """
    def write(self, file_name, merge_file_used=file, list=[]):
        print("write type:" + str(file_name))
        my_class = MainRealtimeApis()
        
        df0= pd.read_csv(merge_file_used)
        df0["datetime"] = pd.to_datetime(df0["datetime"],format="%Y-%m-%d %H:%M:%S")

        df1 = pd.read_csv(file_name)
        df1["datetime"] = pd.to_datetime(df1["datetime"],format="%Y-%m-%d %H:%M:%S") 

        """ 1T_W: SE REGISTRAN VALORES DE TRÁFICO
            2T_W: NO HAY VALORES DE TRÁFICO EN MERGE
                * se espera para guardar cualquier otro valor distinto a los de tráfico
        """   
        if file_name == self.traffic_file:
            df0 = pd.concat([df0, df1])
            df0.to_csv(merge_file_used, index= False, date_format='%Y-%m-%d %H:%M:%S')
            return
        elif df0.shape[0] <= 0: 
            return
        """ CONDICIÓN ^^Línea de arriba - if TRUE: FIN else FALSE: CONTINUE
            -- Si el documento no tiene ni un solo registro guardado no se ejecuta el resto del código ya que no estarán los datos del tráfico
        """
        #si llega aquí es que hay datos de tráfico, por lo que se pueden unir los de calidad de aire y clima
        result = my_class.file_concat_merge(df0, df1, list)

        if file_name == self.air_quality_file:
            self.next_iter_air_quality = result[0]        
        elif file_name == self.weather_file:
            self.next_iter_weather= result[0]
        
        if not result[0]:
            return

        df0 = result[1]
        df0.to_csv(merge_file_used, index= False, date_format='%Y-%m-%d %H:%M:%S')

        ### Si se han registrado los valores para aire y clima en el rango de tiempo
        hour_datetime = df1.loc[0, 'datetime']
        write_air = df0.loc[df0.datetime == hour_datetime, self.list_air_quality[1:]]
        write_weather = df0.loc[df0.datetime == hour_datetime, self.list_weather[1:]]
        if not write_air.isnull().all().all() and not write_weather.isnull().all().all():
            print(f"write - register: {hour_datetime}")
            df = df0.loc[df0.datetime == hour_datetime]
            # donde se guarda todos los valores de la hora en concreto donde estamos
            file_path = os.getcwd() + "/data/realtime_data/merge_hora.csv"
            df.to_csv(file_path, index=False, date_format='%Y-%m-%d %H:%M:%S')
            PreprocessData(file_path, False)
            value_comparison(hour_datetime, False)
            if (hour_datetime + timedelta(hours=4)) >= dt.strptime(self.ini_datetime, "%Y-%m-%dT%H:%M:%S"):
                predictions(hour_datetime)

        

    """ fileConcatMerge:   
        *** recibe dos dataframes @df0 y @df1 y una lista con nombres de columnas @columns
        -Incluye en @df0 los valores de @df1 de @columns cuando la columna "datetime" coincide
        -Sólo registra los valores de @df1 en @df0 
            *Si se han recogido todos los valores de tráfico para el valor "datetime" en @df0.
                Es decir, se registra cuando el último valor de @df0["datetime"] es mayor que @df1["datetime"]
        -En caso de no encontrar coincidencias:
            *Si se cumple la condicion anterior, indica que no hay valores de tráfico para el "datetime" consultado
                entonces, se salta a la siguiente hora 
    """
    def file_concat_merge(self, df0, df1, columns):
        sms = "fileConcatMerge: executed"
        print(sms)
            
        res = pd.to_datetime(df0.loc[df0.index[-1], "datetime"], format="%Y-%m-%d %H:%M:%S") <= pd.to_datetime(df1["datetime"], format="%Y-%m-%d %H:%M:%S")
        if res.bool():
            """ 1T_W_F: AUN FALTAN VALORES DE TRÁFICO 
            -- Hasta que no se registre la hora entera de tráfico no se guardan los datos
                * return false, se espera a que esten todos los valores para la hora a registrar               
            """
            sms =  "fileConcatMerge: 1T_W AUN FALTAN VALORES PARA TRÁFICO"
            return [False, df0, sms]
                
        """ ULTIMA HORA DE TRÁFICO ES MAYOR QUE LA HORA A REGISTRAR

        """
        """ 2T_W_F: SALTO EN VALORES DE TRÁFICO
            -- Hay valores de tráfico mayores a la hora consulta pero NO se encontraron coincidencias
                *return true, no se registran los nuevos valores
            3T_W_F: REGISTRO CORRECTO
            -- Se pasa una lista de valores y se registran cuando @datetime coincida
        """

        for i in columns[1:]:
            df0.loc[df0.datetime == df1.loc[0,"datetime"], i]= df1.loc[0, i]

        sms = "fileConcatMerge: REGISTRO CORRECTO"
        
        return[True, df0, sms]

    def realtime_apis(self):    #inicializa los hilos que tienen la ejecución de la obtención de datos en tiempo real de las distintas API


        self.input_datetime = dt.strptime(str(self.ini_datetime), self.format_datetime) - timedelta(hours=12+4) #Este timedelta son 12 horas que necesita el modelo para hacer predicciones + 4 horas de predicciones que genera

        self.input_datetime = str(self.input_datetime).replace(" ","T")
        self.utils.file_creator(self.merge_file, self.list_merge) 

        #columnas que serán guardadas tras la obtención y preprocesamiento de los datos en tiempo real
        column_list = ["datetime","link_name","weekday","speed","travel_time","AQI_PM2.5","Value_PM2.5","AQI_OZONE","Value_OZONE","Temperature","Relative Humidity","Precipitation","Snow Depth","Visibility","Conditions","relative_speed"]
        
        file_save = os.getcwd() + "/data/realtime_data/merge1.csv"  #fichero donde se almacenan los datos en tiempo real preprocesados

        self.utils.file_creator(file_save, column_list) 

        
        traffic_api_ = threading.Thread(target = self.traffic_api, args = (5*60, 1000000), name="traffic_api")
        air_api_ = threading.Thread(target= self.air_api, args = (17*60,), name="air_api")
        weather_api_ = threading.Thread(target= self.weather_api, args = (29*60,) )
        traffic_api_.start()
        air_api_.start() 
        weather_api_.start()  
