import os
import datetime

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.models import load_model

from WindowGenerator import WindowGenerator


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



def ModelCreation(number_unique_streets):

    file_location =  os.getcwd() + "/data/historical_data/historical_1_hora.csv"

    save_location = os.getcwd() + "/traffic_models/"

    df_historical = pd.read_csv(file_location, low_memory=False)

    mean_std_location = os.getcwd() + "/data/data_for_predictions"

    label = 'relative_speed'

    df_mean = pd.DataFrame()

    df_std = pd.DataFrame()


    # for street_number in range(number_unique_streets):
    for street_number in number_unique_streets:
        
        df = df_historical.loc[df_historical.loc[:, 'link_name'] == street_number]

        df = df.drop(["link_name"],axis=1)

        date_time = pd.to_datetime(df.pop('datetime'), format='%Y-%m-%dT%H:%M:%S')

        df = df.drop(df[ df['AQI_PM2.5'] == -999.0].index)

        df = df.drop(df[ df['travel_time'] > 10000.0].index)
        
        df = df.drop(df[ df['Value_PM2.5'] == -0.30].index)

        timestamp_s = date_time.map(pd.Timestamp.timestamp)

        day = 24*60*60

        df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        
    

        n = len(df)
        train_df = df[0:int(n*0.7)]
        val_df = df[int(n*0.7):int(n*0.9)]
        test_df = df[int(n*0.9):]
 

        num_features = df.shape[1]

        train_mean = train_df.mean()
        train_std = train_df.std()

        df_mean[street_number] = train_mean
        df_std[street_number] = train_std


        # train_mean_df.to_csv(save_location, index=False)
        # train_std_df.to_csv(save_location, index=False)



        train_df = (train_df - train_mean) / train_std
        val_df = (val_df - train_mean) / train_std
        test_df = (test_df - train_mean) / train_std

        
        OUT_STEPS = 4
        multi_window = WindowGenerator(input_width=12,
                                    label_width=OUT_STEPS,
                                    shift=OUT_STEPS,
                                    train_df = train_df,
                                    val_df = val_df,
                                    test_df = test_df)



        RNN_model = tf.keras.Sequential([

            tf.keras.layers.LSTM(24, return_sequences=False),
            tf.keras.layers.Dense(OUT_STEPS*num_features,
                                kernel_initializer=tf.initializers.zeros()),

            tf.keras.layers.Reshape([OUT_STEPS, num_features])
        ])


        history = compile_and_fit(RNN_model, multi_window)

        # print(train_df.columns)
        # print(RNN_model.evaluate(multi_window.val))
        # print(RNN_model.evaluate(multi_window.test, verbose=0))


        # print('Input shape:', multi_window.example[0].shape)
        # print('Output shape:', RNN_model(multi_window.example[0]).shape)
        # train_df = np.reshape(train_df, (train_df.shape[0], 12, train_df.shape[1]))

        # print(RNN_model.predict(train_df[0:24]))

        location = save_location + f'RNN_{label}_street_{street_number}.h5'


        RNN_model.save(location)

    df_mean.to_csv(mean_std_location+"/models_mean.csv", index=True)
    df_std.to_csv(mean_std_location+"/models_std.csv", index=True)


# file_location =  os.getcwd().split("\TFG")[0] + "/TFG/data/historical_data/historical_1_hora.csv"

# df_historical = pd.read_csv(file_location, low_memory=False)

# number_unique_streets = df_historical['link_name'].unique().size


# ModelCreation()