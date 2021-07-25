import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from os import listdir
from pathlib import Path



from realtime_apis.main_realtime_apis import MainRealtimeApis
from historical_apis.main_historical_apis import apisRequest
from ModelCreation import ModelCreation
from preprocessData import PreprocessData

def main():
    
    historical_data_location =  os.getcwd() + "/data/historical_data/"
    models_data_location = os.getcwd()+  "/traffic_models/"


    realtime_apis = MainRealtimeApis()  
    number_of_models = 25
    unsaved_models = []

    while(number_of_models >= 0):
        #Se comprueba que están todos los modelos. Como son 26 en total, este bucle tendrá 26 iteraciones
        location =  f'RNN_relative_speed_street_{number_of_models}.h5'  #nombre del modelo a comprobar si se encuentra

        if(location in listdir(models_data_location)): #Si el modelo se encuentra, continúa
            number_of_models -= 1
        else:
            unsaved_models.append(number_of_models) #Si el modelo no se encuentra, lo añade a la lista que contiene los modelos que falten
            number_of_models -= 1

        

    if(len(unsaved_models) > 0):   #Si no están todos los modelos, podrán ocurrir 2 situaciones:
        # 1) Falta uno o más modelos por generar. Para generarlos, hace falta utilizar los datos preprocesados, por lo que se comprueba
        # que exista el archivo con los datos preprocesados.
        if('historical_1_hora.csv' in listdir(historical_data_location)):   
            ModelCreation(unsaved_models)
            realtime_apis.realtime_apis()
        # 2) Falta uno o más modelos por generar, pero es porque no se encuentra ningún archivo de datos históricos, por lo que se hacen las
        # solicitudes para obtener todos los datos históricos. Con ellos se realiza el documento con los datos preprocesados, se crean todos los 
        # modelos que falten y se ejecuta el realtime
        else:
            apisRequest("2019-07-01T00:00:00", 23, "2019_2020_2021")
            location_to_preprocess = historical_data_location + "/merge_historical/2019_2020_2021/historical_data_2019_2020_2021.csv"
            print("*"*60)
            print("FIN DESCARGA DE DATOS HISTÓRICOS")
            print("*"*60)
            PreprocessData(location_to_preprocess, True)
            ModelCreation(unsaved_models)
            realtime_apis.realtime_apis()

    else:   #se encuentran los modelos, por tanto se puede empezar con la obtención de datos en tiempo real

        realtime_apis.realtime_apis()
            

if __name__ == "__main__":
    
    main()

