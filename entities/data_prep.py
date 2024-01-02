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
		if number in ["049", "091","092","564","837","853"]:
			pass
		elif database.execute(f"SELECT * FROM sqlite_master WHERE name ='vaestorakenne{number}' and type='table';").fetchall() != []:
			# Haetaan kunnan väestörakenne, vuosikate ja suomen bkt ja joinataan ne vuoden perusteella
			rows_to_add = database.execute(f"SELECT * From (SELECT * From vaestorakenne{number} as A LEFT JOIN vuosikate{number} as B ON A.vuosi = B.vuosi where A.id is not NULL and B.id is not null and b.vuosikate is not NULL) as C LEFT JOIN BKT WHERE C.vuosi = BKT.vuosi;").fetchall()
			for i in range(2,len(rows_to_add)-2):
				# Tässä yhdistetään 3 peräkkäistä vuotta, otetaan turhat sarakkeet pois ja järjestetään vuosikate (eli output) viimeiseksi alkioksi
				row_to_add = rows_to_add[i-2][2:-7]+(rows_to_add[i-2][-1],)+(rows_to_add[i-2][-4],)+rows_to_add[i-1][2:-7]+(rows_to_add[i-1][-1],)+(rows_to_add[i-1][-4],)+rows_to_add[i][2:-7]+(rows_to_add[i][-1],)+(rows_to_add[i][-4],)
				data.append(row_to_add)
	random.shuffle(data)
	for i in data:
		output_data.append(i[-1])
		input_data.append(i[:-1])
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