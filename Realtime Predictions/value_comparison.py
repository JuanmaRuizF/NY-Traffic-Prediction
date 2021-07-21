
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
from datetime import datetime as dt
from datetime import timedelta as timedelta

def value_comparison(hour_datetime, prediction, predictions_df=None):
    
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
    df['datetime'] = pd.to_datetime(df['datetime'])

 
    hour_datetime = hour_datetime.strftime('%Y-%m-%d %H:%M:%S') #se convierten ambas columnas a string para poder hacer la comparación bien en el .loc para acotar el DF para la hora solicitada
    df_real_values["datetime"] = df_real_values["datetime"].astype(str)
    print(df_real_values['datetime'])
    df_real_values = df_real_values.loc[df_real_values['datetime'] == hour_datetime]
    df_real_values["datetime"] = pd.to_datetime(df_real_values["datetime"])


    df_append = pd.DataFrame(columns=columns)   #dataframe que añadirá los valores de la hora al archivo final

    # df_append.at[0, 'datetime'] = hour_datetime #se le añade el valor de la hora solicitada como columna

    df_iteration = df_real_values   #esto servirá para iterar sobre todas las calles que hay
    
    # print("-" * 60)
    # print(df_iteration)
    # print(hour_datetime)
    # return
    if(prediction==False):
        if not df.datetime.isin(df_iteration["datetime"]).any().any():
            print("-"*80)
            print("no esta la fecha en  prediction=false")
            print("-"*80)
            print(df_iteration.head())

            if not df_iteration.empty:
                df = df.append({'datetime':df_iteration.loc[df_iteration.index[-1], "datetime"]}, ignore_index=True)
                print("-"*80)
                print("not df_iteration.empty")
                print("-"*80)
            
        for i in range(0,26):
            # print("=*"*100)
            # print(df_iteration.head())
            # print("=*"*100)
            #df_iteration = df_iteration.loc[df_iteration.loc[:, "link_name"] == i]  #acota el dataframe para tener únicamente los valores de esa calle
            df_iteration = df_iteration.loc[df_iteration["link_name"] == i] 
            # print(df_iteration.head())
    
            # print("="*100)
            if not df_iteration.empty:
                df.loc[df.datetime==df_iteration.loc[df_iteration.index[-1], "datetime"],f'{i}-value'] = df_iteration.loc[df_iteration.index[-1],"relative_speed"]

            #df_append.at[0, f"{i}-value"] = df_iteration["relative_speed"].values[0] #añade los valores a la columna correspondiente
            df_iteration = df_real_values   #como el dataframe ha sido modificado para tener los datos de una de las calles, se le vuelve a asignar el dataframe con todas las calles para las siguientes iteraciones
        
        # # df = df.append(df_append)   #se añade la fila creada al dataframe
    else:
        string_prueba = "-pred"

        # predictions_df["datetime"] = predictions_df["datetime"].astype(str)

        for ind in predictions_df.index:

            if not df.datetime.isin([predictions_df["datetime"][ind]]).any().any():
                df = df.append({'datetime':predictions_df["datetime"][ind]}, ignore_index=True)
            
            for i in range(0,26):
                df.loc[df.datetime==predictions_df["datetime"][ind],f'{i}-pred'] = predictions_df[f'{i}-pred'][ind]

            # if predictions_df["datetime"][ind] in df["datetime"].values:
            #     condition = df.index[df['datetime'] == predictions_df["datetime"][ind]]
            #     print("e verda")
                # print(iterate_row[columns])
                # df.loc[df.datetime == hour_datetime_, "columna"] = value

                # df.at[condition]
                #df_append.at[0, f"{i}-value"]
                # print(df.index[df['datetime'] == predictions_df["datetime"][ind]])
            # else:
            #     df = df.append(predictions_df[ind])
                # print(predictions["datetime"][ind])
        # df = df.append(predictions_df)

    df.to_csv(file_directory + "value_comparison.csv", index=False) #se guarda el archivo creado 


# file_directory = os.getcwd() + "/data/realtime_data/a/"
# df = pd.read_csv(file_directory + "value_comparison.csv", low_memory=False)
# value_comparison("2021-07-20 16:00:00", True, df)
