import numpy as np
import random
from services.data_fetching import *


def get_data():
	data= []
	output_data = []
	input_data = []
	municipality_ids = get_wanted_municipality_ids()
	for i in municipality_ids:
		kunta_id = "'"+i[0]+"'"
		new_data = fetch_data(kunta_id)
		data = data + new_data
	random.shuffle(data)
	for i in data:
		output_data.append(i[-3:])
		input_data.append(i[:-3])
	dt=np.dtype('int')
	input_data = np.asarray(input_data,dtype=dt)
	output_data = np.asarray(output_data)
	return (input_data, output_data)


#Tähän huomiona, että kun rupee löytymään käytettävää mallia, niin tarvitaan myös muuttujat mean ja std talteen käyttöä varten
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


