import numpy as np
import time
from entities.models import model as m
from services.data_prep import prep_data
from apupalikoita.mapping import elementwise_error_approximation
from apupalikoita.time_formatting import time_formatter

def test_with_plots(num_epochs:int, k:int, network_structure:list):
	## Isompi, 1000 epochin testi, tulosteiden kanssa
	# tutkitaan epochien määrän merkitystä ja etsitään overfittauksen alkamista:

	start = time.time()

	(train_data,train_targets) = prep_data()

	all_mae_histories = []
	all_elementwise_error_approximations = []
	num_val_samples = len(train_data) // k

	average_norm_of_train_targets = np.average(list(map(np.linalg.norm,train_targets)))
	average_value_of_vector_element = np.average(list(map(np.average,train_targets)))

	print("-------------------")
	print(f"Data prepped. Time elapsed: {time_formatter(time.time()-start)}")
	print(f"Average norm of train targets: {'{:.2f}'.format(average_norm_of_train_targets)}")
	print(f"Average value of train target elements: {'{:.2f}'.format(average_value_of_vector_element)}")
	temp_time = time.time()
	
	for i in range(k):
		print("-------------------")
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

		model = m.build_model(train_data, network_structure)
		history = model.fit(partial_train_data, partial_train_targets,
							validation_data=(val_data, val_targets),
							epochs=num_epochs, batch_size=1, verbose=0)
		mae_history = history.history['val_mae']
		
		all_mae_histories.append(mae_history)
		elementwise_error_approximations = [[x, len(train_targets[0])] for x in mae_history]
		all_elementwise_error_approximations.append(list(map(elementwise_error_approximation,elementwise_error_approximations)))
		
		print(f"Fold {i+1} done. Time elapsed: {time_formatter(time.time()-temp_time)}")
		print(f"MAE : {'{:.2f}'.format(np.average(mae_history))}")
		print(f"Elementwise error approximation : {'{:.2f}'.format(np.average(all_elementwise_error_approximations[-1]))}")
		temp_time = time.time()
	
	# jokaisen epochin keskiarvot
	average_mae_history = [
		np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

	finish = time.time()
	print("-------------------")
	print(f"Full time of the test: {time_formatter(finish-start)}")

	# plottausta
	import matplotlib.pyplot as plt

	average_mae_history = np.asarray(average_mae_history)
	plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
	plt.xlabel('Epochs')
	plt.ylabel('Validation MAE')
	plt.show()

	# plotti on haastavaa luettavaa*. Poistetaan ensimmäiset 10 datapistettä ja smoothataan
	# * kirjan esimerkissä oli, meillä ei aina välttämättä
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



def light_test_with_no_plots(k):
	num_epochs = 100
	all_scores = []

	(train_data,train_targets) = prep_data()

	num_val_samples = len(train_data) // k

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
		model.fit(partial_train_data, partial_train_targets,
				epochs=num_epochs, batch_size=1, verbose=0)
		val_mse, val_mae = model.evaluate(val_data,val_targets,verbose=0)
		all_scores.append(val_mae)

	print(all_scores)
	print(np.mean(all_scores))
