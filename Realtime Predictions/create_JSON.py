import os
from numpy.lib.function_base import append
import pandas as pd
import json
from datetime import timedelta as timedelta
from datetime import datetime as dt
import math


#Creación del archivo JSON
def create_JSON():

    file_directory = os.getcwd() + "/data/realtime_data/"   

    df = pd.read_csv(file_directory + "value_comparison.csv", low_memory=False) # se abre el archivodonde están los valores reales y predicciones

    linkName_dictionary = { #Este diccionario servirá para hacer la traducción entre el número de la calle que aparezca y el nombre real de la calle.
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

    JSON_dictionary = {}    #Este es el JSON que será creado. Se crea como diccionario
    JSON_dictionary["Data"] = []    #Como el JSON tendrá 2 partes, se definen ambas partes
    JSON_dictionary["RealValues"] = []

    for column in df.columns:   #Las columnas continen los valores para las predicciones y valores reales de cada una de las calles por lo que se recorrerán todas para obtener los datos
        append_predictions_dict = {}    #estos serán los diccionarios con los datos específicos de cada calle que se añadirán a cada una de las partes del JSON final
        append_previous_values = {}

        if column != "datetime":    #Se evita la columna "datetime", puesto que no representa a ninguna calle
            
            column_number = int(column[0:column.find('-')])
            
            column_type = column[column.find('-')+1:]

            for key in linkName_dictionary: #Se almacena para la nueva entrada del diccionario el nombre de la calle con su traducción
                if key == column_number:
                    street_name = linkName_dictionary[column_number]
                append_predictions_dict["street"] = street_name
                append_previous_values["street"] = street_name


            if column_type == "value": #las columnas pueden ser de 2 tipos: nº-pred o nº-value. Dependiendo del tipo, se tratarán de forma diferente puesto que esa información será añadida a una parte distinta del JSON
                
                for i in range(1,17):   #se añaden 16 horas a la entrada de datos y se van añadiendo las últimas horas junto con el valor para la columna en concreto
                    hour = df["datetime"].iloc[-i]
                    value = df[column].iloc[-i]
                    if math.isnan(value) == True:
                        continue
                    else:
                        append_previous_values[hour] = value    
                JSON_dictionary["RealValues"].append(append_previous_values)    #se añade la nueva entrada al JSON
                    
                
            elif column_type == "pred": #Si la columna en cuestión se trata de predicciones, se realiza lo mismo, pero se almacena en la parte del JSON con valores de predicciones
                for i in range(1,17):
                    hour = df["datetime"].iloc[-i]
                    value = df[column].iloc[-i]
                    if math.isnan(value) == True:
                        continue
                    else:
                        append_predictions_dict[hour] = value
                JSON_dictionary["Data"].append(append_predictions_dict)
        
        
    JSON_location = os.getcwd()
    JSON_location = JSON_location[0:len(JSON_location)-21] + "/web-traffic/src/Data/TrafficJSON.json"   #Directorio donde se almacena la información para la página web.


    json.dump(JSON_dictionary, open(JSON_location,"w")) #se guarda el JSON en la localización deseada.
