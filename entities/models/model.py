from keras import layers
from keras import models
import pandas
import numpy as np

def get_data(name_of_file):
        data = pandas.read_excel(name_of_file, engine="odf")
        output = data.output1
        data = data.drop(['output1'],axis=1)
        data = np.asarray(data)
        return (data, output)

def normalize(data):
    mean = data.mean(axis=0)
    data = data - mean
    std = data.std(axis=0)
    data = data / std
    return data

(train_data, train_targets) = get_data('randomtestdata.ods')
data = normalize(train_data)

def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model