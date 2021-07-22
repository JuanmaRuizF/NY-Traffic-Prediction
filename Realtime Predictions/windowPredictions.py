import pandas as pd
import numpy as np
import os
from datetime import timedelta as timedelta
from datetime import datetime as dt

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


"""
Adaptación de la clase de WindowGenerator para hacer las predicciones en tiempo real y reentrenar el modelo
En este caso sólo recibe un dataframe que contendrá los últimos valores necesarios para hacer la ventana de datos
"""
class WindowPredictions():
    def __init__(self, input_width, label_width, shift,
                data_df, 
                label_columns=None):
        # Almacenamiento de los conjuntos
        self.data_df = data_df.tail(input_width+label_width)

        # Índice de la columna de la etiqueta
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in
                                        enumerate(label_columns)}
        self.column_indices = {name: i for i, name in
                            enumerate(data_df.columns)}

        # Parámetros de las ventanas
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift

        self.total_window_size = input_width + shift

        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]

        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])

    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tf.stack(
                [labels[:, :, self.column_indices[name]] for name in self.label_columns],
                axis=-1)

        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])

        return inputs, labels

    def make_dataset(self, data):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
                data=data,
                targets=None,
                sequence_length=self.total_window_size,
                sequence_stride=1,
                shuffle=True,
                batch_size=1,)  
        ds = ds.map(self.split_window)

        return ds

    @property
    def data(self):
        return self.make_dataset(self.data_df)