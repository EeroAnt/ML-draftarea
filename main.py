import entities.models.model as m
import numpy as np
import entities.data_prep as data_prep
import time

start = time.time()
(train_data,train_targets) = data_prep.prep_data()

train_targets = train_targets/1000

k = 4
num_val_samples = len(train_data) // 4
num_epochs = 100
all_scores = []

for i in range(k):
	print('prosessing fold #', i)
	val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
	val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]
	val_data = np.array(val_data)
	val_targets = np.array(val_targets)

	partial_train_data = np.concatenate(
		[train_data[:i * num_val_samples],
		train_data[(i + 1) * num_val_samples:]],
		axis=0)
	partial_train_targets = np.concatenate(
		[train_targets[:i * num_val_samples],
		train_targets[(i + 1) * num_val_samples:]],
		axis=0)

	model = m.build_model(train_data)
	model.fit(partial_train_data, partial_train_targets,
			 epochs=num_epochs, batch_size=1, verbose=0)
	val_mse, val_mae = model.evaluate(val_data,val_targets,verbose=0)
	all_scores.append(val_mae)

# print(all_scores)
# print(np.mean(all_scores))


# tutkitaan epochien määrän merkitystä ja etsitään overfittauksen alkamista:

num_epochs = 1000
all_mae_histories = []

for i in range(k):
	print('prosessing fold #', i+1)
	val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
	val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]
	val_data = np.array(val_data)
	val_targets = np.array(val_targets)

	partial_train_data = np.concatenate(
		[train_data[:i * num_val_samples],
		train_data[(i + 1) * num_val_samples:]],
		axis=0)
	partial_train_targets = np.concatenate(
		[train_targets[:i * num_val_samples],
		train_targets[(i + 1) * num_val_samples:]],
		axis=0)

	model = m.build_model(train_data)
	history = model.fit(partial_train_data, partial_train_targets,
						validation_data=(val_data, val_targets),
						epochs=num_epochs, batch_size=1, verbose=0)
	mae_history = history.history['val_mae']
	all_mae_histories.append(mae_history)

# jokaisen epochin keskiarvot
average_mae_history = [
	np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

# plottausta

finish = time.time()

print(f"Koulutukseen kului {finish-start} sekuntia")
print(f"Tulosteiden keskiarvo on {sum(train_targets*1000)/len(train_targets)}")
import matplotlib.pyplot as plt

average_mae_history = np.asarray(average_mae_history)
average_mae_history = average_mae_history * 1000
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