import os
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model

from WindowGenerator import WindowGenerator

#Características de entrenamiento del modelo. Realiza 50 iteraciones pero utiliza early stopping con una paciencia de 2, por lo que normalmente la ejecución del modelo serán muchas menos iteraciones

def compile_and_fit(model, window, patience=2, MAX_EPOCHS = 50):
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                        patience=patience,
                                                        mode='min')

    model.compile(loss=tf.losses.MeanSquaredError(),
                    optimizer=tf.optimizers.Adam(),
                    metrics=[tf.metrics.MeanAbsoluteError()])

    history = model.fit(window.train, epochs=MAX_EPOCHS,
                        validation_data=window.val,
                        callbacks=[early_stopping])
    return history


#Creación del modelo. Se le pasa por parámetro una lista con aquellas calles que no tengan un modelo generado
def ModelCreation(number_unique_streets):

    file_location =  os.getcwd() + "/data/historical_data/historical_1_hora.csv"    
    df_historical = pd.read_csv(file_location, low_memory=False)    #se carga el archivo de los datos hitóricos preprocesados

    save_location = os.getcwd() + "/traffic_models/"    #directorio donde serán guardados los modelos


    mean_std_location = os.getcwd() + "/data/data_for_predictions"  #localización para la media y la desviación estándar

    label = 'relative_speed'    #característica a predecir

    df_mean = pd.DataFrame()    

    df_std = pd.DataFrame()


    for street_number in number_unique_streets: #recorre la lista con el número de las calles de los modelos que faltan por generar
        
        df = df_historical.loc[df_historical.loc[:, 'link_name'] == street_number]  #se acota el dataframe histórico para que sólo contengan los valores de la calle seleccionada

        df = df.drop(["link_name"],axis=1)  #como solo se encuentran datos de una calle, no tiene sentido mantener esta columna

        #se eliminan los posibles datos atípicos
        df = df.drop(df[ df['AQI_PM2.5'] == -999.0].index)
        df = df.drop(df[ df['travel_time'] > 10000.0].index)
        df = df.drop(df[ df['Value_PM2.5'] == -0.30].index)

        #se convierte la columna de datetime a segundos para generar dos columnas nuevas con las señales de seno y coseno con periodo de un día
        date_time = pd.to_datetime(df.pop('datetime'), format='%Y-%m-%dT%H:%M:%S')
        timestamp_s = date_time.map(pd.Timestamp.timestamp)
        day = 24*60*60
        df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        
        #división de los datos en los conjuntos de entrenamiento, validación y prueba
        n = len(df)
        train_df = df[0:int(n*0.7)]
        val_df = df[int(n*0.7):int(n*0.9)]
        test_df = df[int(n*0.9):]
 
        num_features = df.shape[1]

        #valores de la media y la desviación estándar. Se añaden a los dataframe en cuestión
        train_mean = train_df.mean()
        train_std = train_df.std()

        df_mean[street_number] = train_mean
        df_std[street_number] = train_std

        #se hace la normalización de los datos
        train_df = (train_df - train_mean) / train_std
        val_df = (val_df - train_mean) / train_std
        test_df = (test_df - train_mean) / train_std

        #ventana de datos. Recibe 12 entradas y genera 4 predicciones/salidas
        OUT_STEPS = 4
        multi_window = WindowGenerator(input_width=12,
                                    label_width=OUT_STEPS,
                                    shift=OUT_STEPS,
                                    train_df = train_df,
                                    val_df = val_df,
                                    test_df = test_df)

        #modelo creado. es un RNN con una capa LSTM que es la que caracteriza a las RNN y una capa densa. Finalmente, devuelve en una capa reshape el número de predicciones que desean
        RNN_model = tf.keras.Sequential([
            tf.keras.layers.LSTM(24, return_sequences=False),
            tf.keras.layers.Dense(OUT_STEPS*num_features,
                                kernel_initializer=tf.initializers.zeros()),
            tf.keras.layers.Reshape([OUT_STEPS, num_features])
        ])

        #compila el modelo utilizando la ventana de datos creada pasándosela al modelo RNN
        history = compile_and_fit(RNN_model, multi_window)

        #El nombre del modelo a guardar. Contiene el número de la calle para poder distinguirla y utilizarla
        location = save_location + f'RNN_{label}_street_{street_number}.h5'

        #se guarda el modelo en el directorio deseado
        RNN_model.save(location)

    #una vez se hayan generado todos los modelos, se guarda en un CSV el dataframe que contiene los datos de la media y la desviación estándar de cada uno de los modelos.
    df_mean.to_csv(mean_std_location+"/models_mean.csv", index=True)
    df_std.to_csv(mean_std_location+"/models_std.csv", index=True)

