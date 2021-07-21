import os
import datetime

import IPython
import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['axes.grid'] = False


from keras.datasets import imdb
from keras import models, layers, optimizers
import numpy as np


clear = lambda: os.system('Clear')

class WindowPredictions():
    def __init__(self, input_width,
                data_df,
                label_columns=None):
        # Store the raw data.
        self.data_df = data_df.tail(n = input_width)

        # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in
                                        enumerate(label_columns)}
        self.column_indices = {name: i for i, name in
                            enumerate(data_df.columns)}

        # Work out the window parameters.
        self.input_width = input_width
        self.input_slice = slice(0, input_width)

    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        inputs.set_shape([None, self.input_width, None])
        return inputs


    def make_dataset(self, data):
        data = np.array(data, dtype=np.float32)
        ds = tf.keras.preprocessing.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.input_width,
            sequence_stride=1,
            shuffle=True,
            batch_size=1,)

        ds = ds.map(self.split_window)

        return ds

    @property
    def data(self):
        return self.make_dataset(self.data_df)
