from keras import layers
from keras import models

def build_model(train_data, network_structure):
	model = models.Sequential()
	model.add(layers.Dense(network_structure[0][0], activation=network_structure[0][1],
			  input_shape=(train_data.shape[1],)))
	for i in range(1,len(network_structure)-1):
		model.add(layers.Dense(network_structure[i][0], activation=network_structure[i][1]))
	model.add(layers.Dense(network_structure[-1]))
	model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'], run_eagerly=True)
	return model