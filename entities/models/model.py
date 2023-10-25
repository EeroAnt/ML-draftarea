import os
from keras import layers
from keras import models
import numpy as np
import sqlite3
import random

def get_data():
        database = sqlite3.connect("masterdb.db")
        data= []
        output_data = []
        input_data = []
        for i in range(1000):
            if i <10:
                number = f"00{i}"
            elif i <100:
                number = f"0{i}"
            else:
                number = str(i)
            if database.execute(f"SELECT * FROM sqlite_master WHERE name ='vaestorakenne{number}' and type='table';").fetchall() != []:
                rows_to_add = database.execute(f"SELECT * From vaestorakenne{number} as A LEFT JOIN vuosikate{number} as B ON "+
                                               "A.vuosi = B.vuosi where A.id is not NULL and B.id is not null and b.vuosikate is not NULL;").fetchall()
                data = data+rows_to_add
        random.shuffle(data)
        for i in data:
            output_data.append(i[-1])
            input_data.append(i[:-2])
        dt=np.dtype('int')
        input_data = np.asarray(input_data,dtype=dt)
        return (input_data, output_data)

def normalize(data):
    mean = data.mean(axis=0)
    data = data - mean
    std = data.std(axis=0)
    np.seterr(divide='ignore', invalid='ignore')
    data = data / std
    return data

def prep_data():
    (train_data, train_targets) = get_data()
    data = normalize(train_data)
    return data, train_targets

def build_model(train_data):
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',
                           input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model