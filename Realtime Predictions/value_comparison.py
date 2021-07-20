
import os
import datetime
from os import listdir
import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import delete
import pandas as pd
import tensorflow as tf
from datetime import datetime

def value_comparison(hour_datetime, prediction):
    
    file_directory = os.getcwd() + "/data/realtime_data/"

    columns = ["datetime"] #se crean todas las posibles columnas en un array que será utilizado posteriormente
    for i in range(0,26):
        columns.append(f"{i}-value")
        columns.append(f"{i}-pred")

    if("value_comparison.csv" not in listdir(file_directory)): #si no está el archivo de las comparaciones crea el archivo con las columnas generadas anteriormente

        df = pd.DataFrame(columns=columns)
        df.to_csv(file_directory + "value_comparison.csv", index=False)

    df = pd.read_csv(file_directory + "value_comparison.csv", low_memory=False) #si ya existe el archivo, se carga
    df_real_values = pd.read_csv(file_directory + "merge1.csv",  low_memory=False)  #se carga el archivo con datos preprocesados del realtime


    hour_datetime = hour_datetime.strftime('%Y-%m-%d %H:%M:%S') #se convierten ambas columnas a string para poder hacer la comparación bien en el .loc para acotar el DF para la hora solicitada
    df_real_values["datetime"] = df_real_values["datetime"].astype(str)
    df_real_values = df_real_values.loc[df_real_values.loc[:, 'datetime'] == hour_datetime]


    df_append = pd.DataFrame(columns=columns)   #dataframe que añadirá los valores de la hora al archivo final

    df_append.at[0, 'datetime'] = hour_datetime #se le añade el valor de la hora solicitada como columna

    df_iteration = df_real_values   #esto servirá para iterar sobre todas las calles que hay

    if(prediction==False):
        for i in range(0,26):
            df_iteration = df_iteration.loc[df_iteration.loc[:, "link_name"] == i]  #acota el dataframe para tener únicamente los valores de esa calle

            df_append.at[0, f"{i}-value"] = df_iteration["relative_speed"].values[0] #añade los valores a la columna correspondiente
            df_iteration = df_real_values   #como el dataframe ha sido modificado para tener los datos de una de las calles, se le vuelve a asignar el dataframe con todas las calles para las siguientes iteraciones
        
        df = df.append(df_append)   #se añade la fila creada al dataframe
    else:
        print("xd")



    df.to_csv(file_directory + "value_comparison.csv", index=False) #se guarda el archivo creado 


