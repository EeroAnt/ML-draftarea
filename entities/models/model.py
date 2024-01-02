from keras import layers
from keras import models

def build_model(train_data):
	model = models.Sequential()
	model.add(layers.Dense(120, activation='relu',
			  input_shape=(train_data.shape[1],)))
	model.add(layers.Dense(120, activation='relu'))
	model.add(layers.Dense(120, activation='relu'))
	model.add(layers.Dense(3))
	model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'], run_eagerly=True)
	return model