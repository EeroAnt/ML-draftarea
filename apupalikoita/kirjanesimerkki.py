import numpy as np
#datan preppaaminen
from keras.datasets import boston_housing

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()

mean = train_data.mean(axis=0)
train_data = train_data - mean
std = train_data.std(axis=0)
train_data = train_data/std

test_data = test_data - mean
test_data = test_data / std

# Mallin luominen, 2 piilotettua kerrosta leveydellä 64.
# Vähemmän dataa -> enemmän overfittausta, pienempi verkko -> vähemmän overfittausta
# mse = mean square error, mae = mean absolute error. esimerkissä mae = 0,5 kääntyisi keskimäärin 500$ heitoksi

from keras import models
from keras import layers

def build_model():
	model = models.Sequential()
	model.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
	model.add(layers.Dense(64, activation='relu'))
	model.add(layers.Dense(1))
	model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
	return model

# k-fold validation. Vähän datan vuoksi, kaikkea dataa käytetään sekä kouluttamiseen, että validointiin.
# jaetaan data k osaan ja jokaista osaa käytetään vuorollaan validointiin, kun verkko koulutettu muilla osilla.

k = 4
num_val_samples = len(train_data) // 4
num_epochs = 100
all_scores = []

for i in range(k):
	print('prosessing fold #', i)
	val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
	val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

	partial_train_data = np.concatenate(
		[train_data[:i * num_val_samples],
		 train_data[(i + 1) * num_val_samples:]],
		axis=0)
	partial_train_targets = np.concatenate(
		[train_targets[:i * num_val_samples],
		 train_targets[(i + 1) * num_val_samples:]],
		axis=0)

	model = build_model()
	model.fit(partial_train_data, partial_train_targets,
			  epochs=num_epochs, batch_size=1, verbose=0)
	val_mse, val_mae = model.evaluate(val_data,val_targets,verbose=0)
	all_scores.append(val_mae)

print(all_scores)
print(np.mean(all_scores))

# tutkitaan epochien määrän merkitystä ja etsitään overfittauksen alkamista:

num_epochs = 500
all_mae_histories = []

for i in range(k):
	print('prosessing fold #', i)
	val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
	val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

	partial_train_data = np.concatenate(
		[train_data[:i * num_val_samples],
		 train_data[(i + 1) * num_val_samples:]],
		axis=0)
	partial_train_targets = np.concatenate(
		[train_targets[:i * num_val_samples],
		 train_targets[(i + 1) * num_val_samples:]],
		axis=0)

	model = build_model()
	history = model.fit(partial_train_data, partial_train_targets,
						validation_data=(val_data, val_targets),
						epochs=num_epochs, batch_size=1, verbose=0)
	mae_history = history.history['val_mae']
	all_mae_histories.append(mae_history)

# jokaisen epochin keskiarvot
average_mae_history = [
	np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

# plottausta

import matplotlib.pyplot as plt

plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

# plotti on haastavaa luettavaa. Poistetaan ensimmäiset 10 datapistettä ja smoothataan

def smooth_curve(points, factor=0.9):
	smoothed_points=[]
	for point in points:
		if smoothed_points:
			previous = smoothed_points[-1]
			smoothed_points.append(previous*factor+ point*(1-factor))
		else:
			smoothed_points.append(point)
	return smoothed_points

smooth_mae_history = smooth_curve(average_mae_history[10:])

plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

#paras tulos näytti olevan epochilla nro aprrox 60
#training the final model

model = build_model()
model.fit(train_data, train_targets, epochs=60, batch_size=16,verbose=0)
test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)

print(test_mae_score)