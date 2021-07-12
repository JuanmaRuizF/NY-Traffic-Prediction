import pandas as pd
import numpy as np
import csv
import datetime
from datetime import date
import os
from os import listdir
from pathlib import Path
import matplotlib.pyplot as plt
import math


from realtime_apis.main_realtime_apis import MainRealtimeApis
from historical_apis.main_historical_apis import apisRequest
from ModelCreation import ModelCreation
from preprocessData import PreprocessData


def main():
    
    historical_data_location =  os.getcwd() + "/data/historical_data/"
    print(listdir(historical_data_location))
    models_data_location = os.getcwd()+  "/traffic_models/"

    #Se comprueba si existe el archivo histórico con las horas y datos preprocesados

    if('historical_1_hora.csv' in listdir(historical_data_location)):

        #Si está ese archivo, se comprueba que no falte ningún modelo antes de ejecutar el realtime

        number_of_models = 25
        
        unsaved_models = []

        while(number_of_models >= 0):
            #Se comprueba que no falte ningún modelo antes de poder empezar con el realtime
            location =  f'RNN_relative_speed_street_{number_of_models}.h5'

            if(location in listdir(models_data_location)):
                # print("está")
                number_of_models -= 1
            else:
                unsaved_models.append(number_of_models)
                number_of_models -= 1
                # print("no está")
        
        if(len(unsaved_models) == 0):
            #están todos los modelos, se puede empezar con el realtime
            realtime_apis = MainRealtimeApis()
            realtime_apis.realtime_apis()
            

        else:
            #crea los modelos que faltan y después ejecuta el realtime.
            ModelCreation(unsaved_models)
            realtime_apis = MainRealtimeApis()
            realtime_apis.realtime_apis()

    # Si no se encuentra el merge con los históricos preprocesados puede ser 
    # 1) que los datos estén descargados 
    else:

        #Si está el merge histórico pero falta preprocesar los datos, se le pasa el método para preprocesar.
        #No se ejecuta el realtime porque se debe comprobar que estén todos los modelos.

        if('historical_data_2019_2020_2021.csv' in listdir(historical_data_location + "/merge_historical/")): #ARREGLAR DONDE SE GUARDA ESTO
            location_to_preprocess = historical_data_location + "/merge_historical/historical_data_2019_2020_2021.csv"
            PreprocessData(location_to_preprocess)

        else:

        # Los datos no se encuentran, por tanto llama a las API para descargarlos y los preprocesa.
            apisRequest("2019-07-01T00:00:00", 23, "2019_2020_2021")
            location_to_preprocess = historical_data_location + "/merge_historical/historical_data_2019_2020_2021.csv"
            PreprocessData(location_to_preprocess)

            # apisRequest("2021-06-01T00:00:00", 1, "pruebas_junio")

            




if __name__ == "__main__":
    
    main()

