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
from value_comparison import value_comparison
mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False
from keras.datasets import imdb
from keras import models, layers, optimizers
from create_JSON import create_JSON
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


#recibe por parámetro la hora en la que se registró el último valor en tiempo real
def predictions(hour_datetime):

    hour_datetime  = dt.strptime(str(hour_datetime), "%Y-%m-%d %H:%M:%S") + timedelta(hours=1)  #se añade una hora a la hora pasada por parámetros. Así, la primera hora que generará predicciones será a futuro

    #ruta en donde se encuentran los datos para realizar las predicciones.
    path_to_data = os.getcwd() + '/data/realtime_data/merge1.csv'
    data = pd.read_csv(path_to_data, low_memory=False)


    #Se crea una copia de los datos debido a que al iterar por cada calle, se va a acotar el dataframe por cada calle
    data_df = data
    
    columns = ["datetime"] #se crean todas las posibles columnas en un array que será utilizado posteriormente
    for i in range(0,26):
        columns.append(f"{i}-value")
        columns.append(f"{i}-pred")
    
    df_append = pd.DataFrame(columns=columns)

    #se guarda en el dataframe los valores de las 4 próximas horas de tiempo, que serán las horas en las que se harán las predicciones
    for i in range(0,4):
        df_append.at[i, 'datetime'] = dt.strptime(str(hour_datetime), "%Y-%m-%d %H:%M:%S") + timedelta(hours=i)


    #Hay un total de 25 calles, por tanto se recorren dentro de un for para poder generar las predicciones para
    #cada calle 1 por 1
    for i in range(0,26): 

        data_df  = data #Se vuelve a realizar la asignación de los datos para que sea al de todo el dataframe para poder acotarlo
       
        #Se acotan los datos para que cumplan la condición de pertenecer a la calle sobre la que se está iterando
        data_df = data_df.loc[data_df.loc[:, 'link_name'] == i]
        data_df = data_df.drop(["link_name"],axis=1)

        """
        Los siguientes pasos serán preparar las columnas nuevas requeridas para realizar las predicciones del modelo
        Los datos que se pasen como ventana de datos al modelo deberán tener el mismo formato con el que fueron entrenados
        por lo que se crearán las columnas que fueron utilizadas para el entreno
        """
        date_time = pd.to_datetime(data_df.pop('datetime'), format='%Y-%m-%dT%H:%M:%S') #creación de las columnas con el tiempo como señales de seno y coseno
        timestamp_s = date_time.map(pd.Timestamp.timestamp)
        day = 24*60*60
        data_df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        data_df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))

        col = data_df.columns.get_loc('relative_speed')  


        #Se accede y se carga el modelo concreto para esta calle
        path_model = os.getcwd() + f'/traffic_models/RNN_relative_speed_street_{i}.h5'
        model = keras.models.load_model(path_model)

        #Ahora que se tienen todas las columnas, se normalizan los datos y se crea la ventana de datos que será
        #del mismo tamaño que la utilizada para generar el modelo
        data_df = normalize_data(data_df, i)
        

        # Se reentrena el modelo con los últimos datos normalizados de tiempo real para esa calle en concreto
        window_len = 16
        if len(data_df) >= window_len:
            multi_window_train = WindowPredictions(input_width=12,
                                                label_width=4,
                                                shift=4,
                                                data_df=data_df,
                                                label_columns=['relative_speed'])
            model.fit(multi_window_train.data, epochs=20)

        model.save(path_model)  #se guarda el modelo reentrenado


        w1 = WindowPredictions(input_width=12, label_width=0, shift=0, data_df=data_df, #ventana de datos para la creación de nuevas predicciones
                            label_columns=['relative_speed'])


        #Se realizan las predicciones con la ventana de datos creada
        test_predictions = model.predict(w1.data)

        #Array con las predicciones para relative_speed. Como hay 4 predicciones, el array contiene 4 elementos
        list_predictions = [test_predictions[0,0,col], test_predictions[0,1,col], test_predictions[0,2,col], test_predictions[0,3,col]]

        #Estos elementos generados de las predicciones están normalizados, por tanto se desnormalizan en el método
        denormalized_predictions = denormalize_data(list_predictions, i)
        
        prediction_iterator = 0
        for prediction in denormalized_predictions:
            df_append.at[prediction_iterator, f"{i}-pred"] = prediction
            prediction_iterator = prediction_iterator+1


    #una vez se han generado todas las nuevas predicciones, se hace una llamada al método value_comparison para almacenar las nuevas predicciones para la última hora en el archivo que será utilizado
    #para generar el JSON
    #el segundo parámetro en True indica que se trata de predicciones.
    value_comparison(hour_datetime, True, df_append)

    #una vez se han guardado los datos de las nuevas predicciones, se hace una llamada al método para crear el nuevo JSON con los datos actualizados que serán representados en la página web
    create_JSON()


    


