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

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False


from keras.datasets import imdb
from keras import models, layers, optimizers
import numpy as np


from windowPredictions import WindowPredictions

def normalize_data(data_df, i):

    #normalizar datos: (valor - media) / deviación estándar. Se cargan los archivos en los que están las medias y la 
    #desviación estándar de las columnas para cada una de las calles

    mean_model_location = os.getcwd() + '/data/data_for_predictions/models_mean.csv'
    std_model_location = os.getcwd() + '/data/data_for_predictions/models_std.csv'

    mean_model = pd.read_csv(mean_model_location, low_memory=False, index_col=0)

    std_model = pd.read_csv(std_model_location, low_memory=False, index_col=0)

    #Debido a que el archivo contiene los valores para todas las calles en sus columnas, se especifica la columna que 
    #sea el de la calle que se está analizando, y es el valor que se pasa por parámetro.

    val_mean = mean_model[str(i)]
    val_std = std_model[str(i)]

    #se realiza el cálculo de la normalización de los datos y se devuelve.
    data_df = (data_df - val_mean) / val_std

    return data_df


def denormalize_data(list_predictions, i):

    #Para desnormalizar datos basta con coger la fórmula para normalizar datos, y despejar el valor original.
    #Por tanto, la fórmula quedaría así: (valor normalizado * desviación estándar) + media
    #Al igual que para normalizar los datos, se cargan los archivos en donde se encuentran los datos de las medias
    #y la desviación estándar
    mean_model_location = os.getcwd() + '/data/data_for_predictions/models_mean.csv'
    std_model_location = os.getcwd() + '/data/data_for_predictions/models_std.csv'

    mean_model = pd.read_csv(mean_model_location, low_memory=False, index_col=0)

    std_model = pd.read_csv(std_model_location, low_memory=False, index_col=0)

    
    #Como se ha pasado un array con las predicciones sin normalizar, se crea un nuevo array en el que se almacenarán
    #las predicciones desnormalizadas. 

    denormalized_data = []
    denormalized_append = None

    #Se accede al valor de la media y desviación estándar del relative_speed para la calle en concreto.

    denormalize_mean_value = mean_model.loc["relative_speed", str(i)]
    denormalize_std_value = std_model.loc["relative_speed", str(i)]

    #se recorre el array pasado por parámetro con las predicciones sin normalizar y se le aplica la fórmula para desnormalizar.
    #Además, para evitar ligeras desviaciones del modelo en las que puede mostrar valores ligeramente negativos (-0.002) para
    #una variable que no tiene sentido que sea negativa, se coge el valor absoluto de la velocidad relativa y se redondea para 
    # tener sólo 3 decimales. 

    for prediction in list_predictions:
        denormalized_append = round(abs((prediction * denormalize_std_value) + denormalize_mean_value ),3)
        denormalized_data.append(denormalized_append)

    return denormalized_data


def predictions(hour_datetime):


    #se declara el diccionario con las calles y su equivalente con el preprocessed data. Servirá para crear el JSON
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

    #ruta en donde se encuentran los datos para realizar las predicciones.
    # path_to_data = os.getcwd() + '/data/historical_data/pruebas_junio.csv'
    path_to_data = os.getcwd() + '/data/historical_data/historical_1_hora.csv'
    data = pd.read_csv(path_to_data, low_memory=False)

    
    #Se crea el objeto que almacenará el JSON que se utilizará para la página web
    JSON_dictionary = {}
    JSON_dictionary["Data"] = []
    JSON_dictionary["RealValues"] = []

    #Se crea una copia de los datos debido a que al iterar por cada calle, se va a acotar el dataframe por cada calle
    data_df = data
    
    #Hay un total de 25 calles, por tanto se recorren dentro de un for para poder generar las predicciones para
    #cada calle 1 por 1

    for i in range(0,26): 

        data_df  = data #Se vuelve a realizar la asignación de los datos para que sea al de todo el dataframe para poder acotarlo
       
        
        #Se acotan los datos para que cumplan la condición de pertenecer a la calle sobre la que se está iterando
        data_df = data_df.loc[data_df.loc[:, 'link_name'] == i]
        data_df = data_df.drop(["link_name"],axis=1)


        #Los siguientes pasos serán preparar las columnas nuevas requeridas para realizar las predicciones del modelo
        date_time = pd.to_datetime(data_df.pop('datetime'), format='%Y-%m-%dT%H:%M:%S')

        timestamp_s = date_time.map(pd.Timestamp.timestamp)
        day = 24*60*60

        data_df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        data_df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))

        col = data_df.columns.get_loc('relative_speed')

        #Para poder almacenar y representar los datos originales de horas anteriores, se almacenan en un array
        previous_speed_values = []

        for num in range (13):
            previous_speed_values.append(round(data_df["relative_speed"].iloc[-num],3))

        
        #Ahora que se tienen todas las columnas, se normalizan los datos y se crea la ventana de datos que será
        #del mismo tamaño que la utilizada para generar el modelo

        data_df = normalize_data(data_df, i)
        w1 = WindowPredictions(input_width=12, data_df=data_df,
                            label_columns=['relative_speed'])

        
        #Se accede y se carga el modelo concreto para esta calle
        path_model = os.getcwd() + f'/traffic_models/RNN_relative_speed_street_{i}.h5'
        model = keras.models.load_model(path_model)

        #Se realizan las predicciones con la ventana de datos creada
        test_predictions = model.predict(w1.data)

        #Array con las predicciones para relative_speed. Como hay 4 predicciones, el array contiene 4 elementos
        list_predictions = [test_predictions[0,0,col], test_predictions[0,1,col], test_predictions[0,2,col], test_predictions[0,3,col]]

        #Estos elementos generados de las predicciones están normalizados, por tanto se desnormalizan en el método
        denormalized_predictions = denormalize_data(list_predictions, i)


        #Se busca el nombre de la calle analizada en el diccionario mostrado al principio del método para añadirlo al JSON
        street_name = None
        for key in linkName_dictionary:
            if(key == i):
                street_name = linkName_dictionary[i]


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
            keys_predictions[0]: denormalized_predictions[0],
            keys_predictions[1]: denormalized_predictions[1],
            keys_predictions[2]: denormalized_predictions[2],
            keys_predictions[3]: denormalized_predictions[3],
            "street": street_name
        }

        append_previous_values = {
            keys_past[5]: previous_speed_values[5],
            keys_past[4]: previous_speed_values[4],
            keys_past[3]: previous_speed_values[3],
            keys_past[2]: previous_speed_values[2],
            keys_past[1]: previous_speed_values[1],
            keys_past[0]: previous_speed_values[0],
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
     
    
        

# predictions("2021-04-05 23:00:00")    
    


