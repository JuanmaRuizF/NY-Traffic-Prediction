import os
import datetime

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers
import json
from datetime import timedelta as timedelta
from datetime import datetime as dt
import math
mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False


from keras.datasets import imdb
from keras import models, layers, optimizers
import numpy as np

def create_JSON():
    file_directory = os.getcwd() + "/data/realtime_data/"

    df = pd.read_csv(file_directory + "value_comparison.csv", low_memory=False)

    linkName_dictionary = {
        0:'FDR N - TBB E 116TH STREET - MANHATTAN TRUSS',
        1:'LINCOLN TUNNEL E CENTER TUBE NJ - NY',
        2:'LINCOLN TUNNEL E SOUTH TUBE - NJ - NY',
        3:'Westside Hwy N 57th St - GWB',
        4:'LINCOLN TUNNEL W CENTER TUBE NY - NJ',
        5:'BQE N Atlantic Ave - MAN Bridge Manhattan Side',
        6:'BQE N Atlantic Ave - BKN Bridge Manhattan Side',
        7:'12th Ave N 40th - 57th St', 
        8:'FDR N Catherine Slip - 25th St',
        9:'Westside Hwy S GWB - 57th St',
        10:'FDR S 63rd - 25th St',
        11:'FDR N 25th - 63rd St', 
        12:'12th ave @ 45th - 11 ave ganservoort st',
        13:'12th Ave S 57th St - 45th St',
        14:'TBB W - FDR S MANHATTAN TRUSS - E116TH STREET',
        15:'BKN Bridge Manhattan Side - FDR N Catherine Slip',
        16:'LINCOLN TUNNEL W NORTH TUBE NY - NJ',
        17:'BBT W Toll Plaza - Manhattan Portal',
        18:'BBT E Manhattan Portal - Toll Plaza',
        19:'11th ave n ganservoort - 12th ave @ 40th st',
        20:'FDR S 25th St - Catherine Slip',
        21:'11th ave s ganservoort - west st @ spring st',
        22:'FDR S Catherine Slip - BKN Bridge Manhattan Side',
        23:'West St S Spring St - BBT Manhattan Portal outbound',
        24:'GWB E LOWER LEVEL PLAZA - CBE E LOWER LEVEL AMSTERDAM AVE',
        25:'QMT E Manhattan Side - Toll Plaza'
    }
    JSON_dictionary = {}
    JSON_dictionary["Data"] = []
    JSON_dictionary["RealValues"] = []

    for column in df.columns:
        append_predictions_dict = {}
        append_previous_values = {}

        if column != "datetime":
            
            column_number = int(column[0:column.find('-')])
            
            column_type = column[column.find('-')+1:]

            for key in linkName_dictionary:
                if key == column_number:
                    street_name = linkName_dictionary[column_number]
                append_predictions_dict["street"] = street_name
                append_previous_values["street"] = street_name


            if column_type == "value":
                
                for i in range(1,13):
                    hour = df["datetime"].iloc[-i]
                    value = df[column].iloc[-i]
                    if math.isnan(value) == True:
                        continue
                    else:
                        append_previous_values[hour] = value
                JSON_dictionary["RealValues"].append(append_previous_values)
                    
                
            elif column_type == "pred":
                for i in range(1,13):
                    hour = df["datetime"].iloc[-i]
                    value = df[column].iloc[-i]
                    if math.isnan(value) == True:
                        continue
                    else:
                        append_predictions_dict[hour] = value
                JSON_dictionary["Data"].append(append_predictions_dict)
        
        



            #print(column[0:column.find('-')])
            # if column[0:column.find('-')] == "datetim"


            # if column[0:column.find('-')] != "datetim": #para evitar la columna de "datetime"
            #     street_number = int(column[0:column.find('-')])
            #     print(i)
            #     print(street_number)
            #     if street_number == i:    #si el número de la columna hace referencia a la misma iteración del bucle
            #         for key in linkName_dictionary:
            #             if key == street_number:
            #                 # print(street_number)
            #                 # print(key)
            #                 street_name = linkName_dictionary[street_number]
            #                 # print(linkName_dictionary[street_number])
            #             append_previous_values["street"] = street_name
            #             append_predictions_dict["street"] = street_name

            #         if column[2:] == "value": #comprobar si es el valor para la columna de value o prediction
            #             for i in range(1,13):
            #                 hour = df['datetime'].iloc[-i]
            #                 value = df[column].iloc[-i]
            #                 if math.isnan(value) == True:
            #                     continue
            #                 append_previous_values[hour] = value

            #         else:
            #             for i in range(1,13):
            #                 hour = df['datetime'].iloc[-i]
            #                 value = df[column].iloc[-i]
            #                 if math.isnan(value) == True:
            #                     continue
            #                 append_predictions_dict[hour] = value

    # JSON_dictionary["Data"].append(append_predictions_dict) #Se guardan los datos en el objeto que representa el JSON
    
    # JSON_dictionary["RealValues"].append(append_previous_values)
    JSON_location = os.getcwd()
    #JSON_location = JSON_location + "/TrafficJSON.json"
    JSON_location = JSON_location[0:len(JSON_location)-21] + "/web-traffic/src/Data/TrafficJSON.json"


    json.dump(JSON_dictionary, open(JSON_location,"w"))
    return





    for column in df.columns:
        #print(column)
        #     print(df['datetime'].iloc[-1])
        if column == "datetime":
            continue
 
        if column[2:] == "value":
            
            street_name = None
            street_number = column[0:column.find('-')]
            street_number = int(street_number)
            for key in linkName_dictionary:
                if(key == street_number):
                    street_name = linkName_dictionary[street_number]


                append_previous_values["street"] = street_name


            hour = df['datetime'].iloc[-1]

            for i in range(1,13):
                hour = df['datetime'].iloc[-i]
                value = df[column].iloc[-i]
                if math.isnan(value) == True:
                    continue
                append_previous_values[hour] = value
            # print(append_previous_values)
        else:

            street_name = None
            street_number = column[0:column.find('-')]
            street_number = int(street_number)
            for key in linkName_dictionary:
                if(key == street_number):
                    street_name = linkName_dictionary[street_number]


                append_predictions_dict["street"] = street_name
            

            hour = df['datetime'].iloc[-1]

            for i in range(1,13):
                hour = df['datetime'].iloc[-i]
                value = df[column].iloc[-i]
                if math.isnan(value) == True:
                    continue
                append_predictions_dict[hour] = value

            # print(append_predictions_dict)
        

        JSON_dictionary["Data"].append(append_predictions_dict) #Se guardan los datos en el objeto que representa el JSON
    
        JSON_dictionary["RealValues"].append(append_previous_values)
        JSON_location = os.getcwd()
        JSON_location = JSON_location + "/TrafficJSON.json"
        # JSON_location = JSON_location[0:len(JSON_location)-21] + "/web-traffic/src/Data/TrafficJSON.json"


        json.dump(JSON_dictionary, open(JSON_location,"w"))


"""
def create_JSON():
    file_directory = os.getcwd() + "/data/realtime_data/"

    df = pd.read_csv(file_directory + "value_comparison.csv", low_memory=False)

    linkName_dictionary = {
        0:'FDR N - TBB E 116TH STREET - MANHATTAN TRUSS',
        1:'LINCOLN TUNNEL E CENTER TUBE NJ - NY',
        2:'LINCOLN TUNNEL E SOUTH TUBE - NJ - NY',
        3:'Westside Hwy N 57th St - GWB',
        4:'LINCOLN TUNNEL W CENTER TUBE NY - NJ',
        5:'BQE N Atlantic Ave - MAN Bridge Manhattan Side',
        6:'BQE N Atlantic Ave - BKN Bridge Manhattan Side',
        7:'12th Ave N 40th - 57th St', 
        8:'FDR N Catherine Slip - 25th St',
        9:'Westside Hwy S GWB - 57th St',
        10:'FDR S 63rd - 25th St',
        11:'FDR N 25th - 63rd St', 
        12:'12th ave @ 45th - 11 ave ganservoort st',
        13:'12th Ave S 57th St - 45th St',
        14:'TBB W - FDR S MANHATTAN TRUSS - E116TH STREET',
        15:'BKN Bridge Manhattan Side - FDR N Catherine Slip',
        16:'LINCOLN TUNNEL W NORTH TUBE NY - NJ',
        17:'BBT W Toll Plaza - Manhattan Portal',
        18:'BBT E Manhattan Portal - Toll Plaza',
        19:'11th ave n ganservoort - 12th ave @ 40th st',
        20:'FDR S 25th St - Catherine Slip',
        21:'11th ave s ganservoort - west st @ spring st',
        22:'FDR S Catherine Slip - BKN Bridge Manhattan Side',
        23:'West St S Spring St - BBT Manhattan Portal outbound',
        24:'GWB E LOWER LEVEL PLAZA - CBE E LOWER LEVEL AMSTERDAM AVE',
        25:'QMT E Manhattan Side - Toll Plaza'
    }
    JSON_dictionary = {}
    JSON_dictionary["Data"] = []
    JSON_dictionary["RealValues"] = []

        #Se busca el nombre de la calle analizada en el diccionario mostrado al principio del método para añadirlo al JSON
    street_name = None
    for key in linkName_dictionary:
        if(key == street_number):
            street_name = linkName_dictionary[street_number]


    keys_past = []
    for hour in range(1,7):
        append_time = dt.strptime(str(hour_datetime), "%Y-%m-%d %H:%M:%S") - timedelta(hours=hour)
        # keys_past.append(append_time.hour)
        keys_past.append(str(append_time))

    keys_predictions = []
    for hour in range(0,4):
        append_time = dt.strptime(str(hour_datetime), "%Y-%m-%d %H:%M:%S") + timedelta(hours=hour)
        # keys_predictions.append(append_time.hour) 
        keys_predictions.append(str(append_time)) 

    #Datos que contiene el JSON: La calle, algunos valores de horas anteriores y las predicciones
    append_predictions_dict = {
        keys_predictions[0]: list_predictions[0],
        keys_predictions[1]: list_predictions[1],
        keys_predictions[2]: list_predictions[2],
        keys_predictions[3]: list_predictions[3],
        "street": street_name
    }

    append_previous_values = {
        keys_past[5]: list_predictions[5],
        keys_past[4]: list_predictions[4],
        keys_past[3]: list_predictions[3],
        keys_past[2]: list_predictions[2],
        keys_past[1]: list_predictions[1],
        keys_past[0]: list_predictions[0],
        "street": street_name 
    }



    JSON_dictionary["Data"].append(append_predictions_dict) #Se guardan los datos en el objeto que representa el JSON
    
    JSON_dictionary["RealValues"].append(append_previous_values)
    print('='*100)


    #Una vez terminado de generar predicciones para cada calle, se guardará el archivo JSON en la carpeta correspondiente
    #Para la página web
    
    JSON_location = os.getcwd()
    JSON_location = JSON_location[0:len(JSON_location)-21] + "/web-traffic/src/Data/TrafficJSON.json"


    json.dump(JSON_dictionary, open(JSON_location,"w"))
     
    
"""

#create_JSON()