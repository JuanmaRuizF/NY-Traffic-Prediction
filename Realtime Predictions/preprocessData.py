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

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False



def deleteColumns(df):

    #Se eliminan las columnas no deseadas y se devuelve el dataframe actualizado
    columns = [ 'Parameter_PM2.5', 'Unit_PM2.5', 'Parameter_OZONE', 
                  'Unit_OZONE','Minimum Temperature', 'Maximum Temperature','Heat Index', 
                  'Wind Gust','Wind Chill', 'Precipitation Cover',"Category_OZONE",
                  "Category_PM2.5",  "Dew Point","Wind Speed", "Wind Direction", "Cloud Cover",
                    "Sea Level Pressure"]

    df = df.drop(columns,axis=1)

    return df



def editColumns(df):

    #Método para editar algunas columnas y agregar nuevas como son "relative_speed"
    relative_speed_file =  os.getcwd() +  "/data/uniqueStreets.csv"
    df_relative_speed =  pd.read_csv(relative_speed_file, low_memory=False)

    df = pd.merge(df, df_relative_speed, on="link_name")

    df["vmaxM"] = df["vmaxM"].astype(np.float64)
    df["speed"] = df["speed"].astype(np.float64)

    df["vmaxM"] =  1.609 * df["vmaxM"] 
    df["relative_speed"] = df["speed"] / df["vmaxM"]

    print(df["relative_speed"])

    df['link_name'] = df['link_name'].replace(['FDR N - TBB E 116TH STREET - MANHATTAN TRUSS',
           'LINCOLN TUNNEL E CENTER TUBE NJ - NY',
           'LINCOLN TUNNEL E SOUTH TUBE - NJ - NY',
           'Westside Hwy N 57th St - GWB',
           'LINCOLN TUNNEL W CENTER TUBE NY - NJ',
           'BQE N Atlantic Ave - MAN Bridge Manhattan Side',
           'BQE N Atlantic Ave - BKN Bridge Manhattan Side',
           '12th Ave N 40th - 57th St', 'FDR N Catherine Slip - 25th St',
           'Westside Hwy S GWB - 57th St', 'FDR S 63rd - 25th St',
           'FDR N 25th - 63rd St', '12th ave @ 45th - 11 ave ganservoort st',
           '12th Ave S 57th St - 45th St',
           'TBB W - FDR S MANHATTAN TRUSS - E116TH STREET',
           'BKN Bridge Manhattan Side - FDR N Catherine Slip',
           'LINCOLN TUNNEL W NORTH TUBE NY - NJ',
           'BBT W Toll Plaza - Manhattan Portal',
           'BBT E Manhattan Portal - Toll Plaza',
           '11th ave n ganservoort - 12th ave @ 40th st',
           'FDR S 25th St - Catherine Slip',
           '11th ave s ganservoort - west st @ spring st',
           'FDR S Catherine Slip - BKN Bridge Manhattan Side',
           'West St S Spring St - BBT Manhattan Portal outbound',
           'GWB E LOWER LEVEL PLAZA - CBE E LOWER LEVEL AMSTERDAM AVE',
           'QMT E Manhattan Side - Toll Plaza'],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])

    
    df['Conditions'] = df['Conditions'].astype('category')
    df['weekday'] = df['weekday'].astype('category')
    

    df['Conditions'] = df['Conditions'].cat.codes
    df['weekday'] = df['weekday'].cat.codes
    
    
    df["Conditions"] = df["Conditions"].astype(np.float64)
    df["weekday"] = df["weekday"].astype(np.float64)

    df = df.drop([ "vmaxM", "coordX", "coordY", "zonaX", "zonaY", "zona"],axis=1)

    df = df.fillna(0)
    # df = df.dropna()

    return df


def PreprocessData(file_path, isHistorical):


    #se accede al archivo para hacer el preprocesamiento, se lee y se le aplican los distintos métodos realizados
    
    # file_location =  os.getcwd() +  "/data/historical_data/merge_historical/2019_2020_2021/historical_data_2019_2020_2021.csv"
    # file_location =  os.getcwd() +  "/data/historical_data/merge_historical/pruebas_junio/historical_data_pruebas_junio.csv"

    df = pd.read_csv(file_path, low_memory=False)
    
    df = deleteColumns(df)

    df = editColumns(df)

    #Se agrupan los datos para tener 1 dato por calle y hora. Esto es lo que se aplicará a los modelos

    df = df.groupby(['datetime', 'link_name']).mean()
    #df = df.rename(columns={'datetime': 'datetime_traffic'}) 

    if isHistorical == True:

    #Se guarda el nuevo dataframe con los cambios en el directorio indicado.

        df.to_csv(os.getcwd() + "/data/historical_data/historical_1_hora.csv", index=True)


    # df.to_csv(os.getcwd() + "/data/historical_data/pruebas_junio.csv", index=True)
    else:


        file_save = os.getcwd() + "/data/realtime_data/merge1.csv"

        
        open_file = pd.read_csv(file_save, low_memory=False)

        #open_file = open_file.rename(columns={'datetime': 'datetime_traffic'}) 

        open_file.set_index(['datetime','link_name'], inplace = True)
        open_file = pd.concat([open_file, df])
        print(open_file.tail(20))
        open_file.to_csv(os.getcwd() + "/data/realtime_data/merge1.csv", index=True)

