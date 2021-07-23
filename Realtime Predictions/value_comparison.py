import os
from os import listdir
from numpy.lib.function_base import delete
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as timedelta

#este método sirve para almacenar en un documento los datos que vengan en tiempo real junto con las predicciones generadas. Estos datos sirven para generar el JSON posteriormente
#el método recibe tanto predicciones como datos generados en tiempo real
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
    df_real_values = df_real_values.loc[df_real_values['datetime'] == hour_datetime]
    df_real_values["datetime"] = pd.to_datetime(df_real_values["datetime"])


    df_iteration = df_real_values   #esto servirá para iterar sobre todas las calles que hay

    if(prediction==False):  #si se trata de valores reales
        if not df.datetime.isin(df_iteration["datetime"]).any().any():  #si existe al menos algún elemento datetime de df_iteration que coincida con un elemento de datetime df -> true
            
            if not df_iteration.empty:  #si no existe esa fecha y además df_iteration no está vacío, se añade la fecha sin el contenido
                df = df.append({'datetime':df_iteration.loc[df_iteration.index[-1], "datetime"]}, ignore_index=True)
            
        for i in range(0,26): #para cada valor de df_iteration se coge el relative_speed por calle y se añaden a la fecha de df correspondiente
            df_iteration = df_iteration.loc[df_iteration["link_name"] == i] #acota el dataframe para tener únicamente los valores de esa calle
            if not df_iteration.empty:
                df.loc[df.datetime==df_iteration.loc[df_iteration.index[-1], "datetime"],f'{i}-value'] = df_iteration.loc[df_iteration.index[-1],"relative_speed"]


            df_iteration = df_real_values   #como el dataframe ha sido modificado para tener los datos de una de las calles, se le vuelve a asignar el dataframe con todas las calles para las siguientes iteraciones

    else:   #si se trata de predicciones

        for ind in predictions_df.index:

            if not df.datetime.isin([predictions_df["datetime"][ind]]).any().any():
                df = df.append({'datetime':predictions_df["datetime"][ind]}, ignore_index=True) #si no se encuentra la fecha y hora, la añade
            
            for i in range(0,26):#para cada valor de predictions_df se añade la columna correspondiente a df
                df.loc[df.datetime==predictions_df["datetime"][ind],f'{i}-pred'] = predictions_df[f'{i}-pred'][ind]


    df.to_csv(file_directory + "value_comparison.csv", index=False) #se guarda el archivo creado o con los cambios


