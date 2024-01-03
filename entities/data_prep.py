import numpy as np
import sqlite3
import random

def get_data():
	db = sqlite3.connect("masterdb.db")
	data= []
	output_data = []
	input_data = []
	municipality_ids = get_wanted_municipality_ids()
	for i in municipality_ids:
		kunta_id = "'"+i[0]+"'"
		sql1, sql2, sql3, sql4 = queries_for_two_years_of_data_and_three_next_for_targets(kunta_id)
		db.execute(sql1)
		db.commit()
		db.execute(sql2)
		db.commit()
		for i in sql3:
			db.execute(i)
		db.commit()
		result =db.execute(sql4).fetchall()
		db.commit()
		# suodatan pois ne rivit, joissa on None-arvoja, toistaiseksi rikkovat mallin. Ekalla testillä niitä oli ~ 4 / 3000
		result = list(filter(lambda x: x.count(None) == 0, result))
		for i in result:
			data.append(i)
	random.shuffle(data)
	for i in data:
		output_data.append(i[-3:])
		input_data.append(i[:-3])
	dt=np.dtype('int')
	input_data = np.asarray(input_data,dtype=dt)
	output_data = np.asarray(output_data)
	return (input_data, output_data)


#Tätä voi varmasti laajentaa esim tekemään halutut rajaukset parametrien avulla
def get_wanted_municipality_ids():
	db = sqlite3.connect("masterdb.db")
	sql = "SELECT kunta_id FROM Asukasluku WHERE Asukasluvun_ka < 15000"
	municipality_ids = db.execute(sql).fetchall()
	return municipality_ids


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


# Ja sitten hiukan sql:ää.
# Tehdään väliaikainen taulu, jossa on kaikki tarvittavat tiedot. Tämän jälkeen poistetaan turhat sarakkeet ja
# palautetaan taulu. Aloitetaan poistamalla vanha taulu, jos sellainen on olemassa. Tässä varmasti optimoitavaa. Sitten joskus (tm)
def queries_for_two_years_of_data_and_three_next_for_targets(kunta_id):
	
	sql1 = "DROP TABLE IF EXISTS TEMP_TABLE;"
	
	sql2 = ("CREATE TABLE TEMP_TABLE AS SELECT * FROM (SELECT "+
			"t1.vuosi AS vuosi, t1.Toinen24, t1.Toinen34, t1.Toinen44, t1.Toinen54, t1.Toinen64, t1.Toinen74, "+
			"t1.Alin24, t1.Alin34, t1.Alin44, t1.Alin54, t1.Alin64, t1.Alin74, "+
			"t1.Ylempi24, t1.Ylempi34, t1.Ylempi44, t1.Ylempi54, t1.Ylempi64, t1.Ylempi74, "+
			"t1.Ei24, t1.Ei34, t1.Ei44, t1.Ei54, t1.Ei64, t1.Ei74, "+
			"t2.Toinen24, t2.Toinen34, t2.Toinen44, t2.Toinen54, t2.Toinen64, t2.Toinen74, "+
			"t2.Alin24, t2.Alin34, t2.Alin44, t2.Alin54, t2.Alin64, t2.Alin74, "+
			"t2.Ylempi24, t2.Ylempi34, t2.Ylempi44, t2.Ylempi54, t2.Ylempi64, t2.Ylempi74, "+
			"t2.Ei24, t2.Ei34, t2.Ei44, t2.Ei54, t2.Ei64, t2.Ei74, "+
			"t3.BKT, "+
			"t4.Nuoria_yhteensa, t4.Tyovoima_nuoret, t4.Alle_15, t4.Opiskelijat_nuoret, t4.Elake_nuoret, "+
			"t4.Aikuisia_yhteensa, t4.Tyovoima_aikuiset, t4.Tyolliset_aikuiset, t4.Opiskelijat_aikuiset, t4.Varusmiehet_aikuiset, t4.Elake_aikuiset, "+
			"t4.Iakkaat_yhteensa, t4.Tyovoima_iakkaat, t4.Tyolliset_iakkaat, t4.Opiskelijat_iakkaat, t4.Elake_iakkaat, "+
			"t5.vuosikate "+
			"FROM Asuinkunnassa t1 "+
			"LEFT JOIN Pendeloivat t2 ON t1.vuosi = t2.vuosi "+
			"LEFT JOIN BKT t3 ON t1.vuosi = t3.vuosi "+
			"LEFT JOIN Vaestorakenne t4 ON t1.vuosi = t4.vuosi "+
			"LEFT JOIN Vuosikate t5 ON t1.vuosi = t5.vuosi "+
			f"WHERE t1.kunta_id = {kunta_id} AND t2.kunta_id ={kunta_id} AND t4.kunta_id={kunta_id} AND t5.kunta_id={kunta_id}) AS A "+
			"LEFT JOIN (SELECT "+
			"t1.vuosi AS vuosi, t1.Toinen24, t1.Toinen34, t1.Toinen44, t1.Toinen54, t1.Toinen64, t1.Toinen74, "+
			"t1.Alin24, t1.Alin34, t1.Alin44, t1.Alin54, t1.Alin64, t1.Alin74, "+
			"t1.Ylempi24, t1.Ylempi34, t1.Ylempi44, t1.Ylempi54, t1.Ylempi64, t1.Ylempi74, "+
			"t1.Ei24, t1.Ei34, t1.Ei44, t1.Ei54, t1.Ei64, t1.Ei74, "+
			"t2.Toinen24, t2.Toinen34, t2.Toinen44, t2.Toinen54, t2.Toinen64, t2.Toinen74, "+
			"t2.Alin24, t2.Alin34, t2.Alin44, t2.Alin54, t2.Alin64, t2.Alin74, "+
			"t2.Ylempi24, t2.Ylempi34, t2.Ylempi44, t2.Ylempi54, t2.Ylempi64, t2.Ylempi74, "+
			"t2.Ei24, t2.Ei34, t2.Ei44, t2.Ei54, t2.Ei64, t2.Ei74, "+
			"t3.BKT, "+
			"t4.Nuoria_yhteensa, t4.Tyovoima_nuoret, t4.Alle_15, t4.Opiskelijat_nuoret, t4.Elake_nuoret, "+
			"t4.Aikuisia_yhteensa, t4.Tyovoima_aikuiset, t4.Tyolliset_aikuiset, t4.Opiskelijat_aikuiset, t4.Varusmiehet_aikuiset, t4.Elake_aikuiset, "+
			"t4.Iakkaat_yhteensa, t4.Tyovoima_iakkaat, t4.Tyolliset_iakkaat, t4.Opiskelijat_iakkaat, t4.Elake_iakkaat, "+
			"t5.vuosikate "+
			"FROM Asuinkunnassa t1  "+
			"LEFT JOIN Pendeloivat t2 ON t1.vuosi = t2.vuosi "+
			"LEFT JOIN BKT t3 ON t1.vuosi = t3.vuosi "+
			"LEFT JOIN Vaestorakenne t4 ON t1.vuosi = t4.vuosi "+
			"LEFT JOIN Vuosikate t5 ON t1.vuosi = t5.vuosi "+
			f"WHERE t1.kunta_id = {kunta_id} AND t2.kunta_id ={kunta_id} AND t4.kunta_id={kunta_id} AND t5.kunta_id={kunta_id}) AS B "+
			"ON A.vuosi = B.vuosi-1 "+
			"LEFT JOIN (SELECT "+
			"t1.vuosi AS vuosi, t1.Toinen24, t1.Toinen34, t1.Toinen44, t1.Toinen54, t1.Toinen64, t1.Toinen74, "+
			"t1.Alin24, t1.Alin34, t1.Alin44, t1.Alin54, t1.Alin64, t1.Alin74, "+
			"t1.Ylempi24, t1.Ylempi34, t1.Ylempi44, t1.Ylempi54, t1.Ylempi64, t1.Ylempi74, "+
			"t1.Ei24, t1.Ei34, t1.Ei44, t1.Ei54, t1.Ei64, t1.Ei74, "+
			"t2.Toinen24, t2.Toinen34, t2.Toinen44, t2.Toinen54, t2.Toinen64, t2.Toinen74, "+
			"t2.Alin24, t2.Alin34, t2.Alin44, t2.Alin54, t2.Alin64, t2.Alin74, "+
			"t2.Ylempi24, t2.Ylempi34, t2.Ylempi44, t2.Ylempi54, t2.Ylempi64, t2.Ylempi74, "+
			"t2.Ei24, t2.Ei34, t2.Ei44, t2.Ei54, t2.Ei64, t2.Ei74, "+
			"t3.BKT, "+
			"t4.Nuoria_yhteensa, t4.Tyovoima_nuoret, t4.Alle_15, t4.Opiskelijat_nuoret, t4.Elake_nuoret, "+
			"t4.Aikuisia_yhteensa, t4.Tyovoima_aikuiset, t4.Tyolliset_aikuiset, t4.Opiskelijat_aikuiset, t4.Varusmiehet_aikuiset, t4.Elake_aikuiset, "+
			"t4.Iakkaat_yhteensa, t4.Tyovoima_iakkaat, t4.Tyolliset_iakkaat, t4.Opiskelijat_iakkaat, t4.Elake_iakkaat, "+
			"t5.vuosikate "+
			"FROM Asuinkunnassa t1  "+
			"LEFT JOIN Pendeloivat t2 ON t1.vuosi = t2.vuosi "+
			"LEFT JOIN BKT t3 ON t1.vuosi = t3.vuosi "+
			"LEFT JOIN Vaestorakenne t4 ON t1.vuosi = t4.vuosi "+
			"LEFT JOIN Vuosikate t5 ON t1.vuosi = t5.vuosi "+
			f"WHERE t1.kunta_id = {kunta_id} AND t2.kunta_id ={kunta_id} AND t4.kunta_id={kunta_id} AND t5.kunta_id={kunta_id}) AS C "+
			"ON A.vuosi = C.vuosi-2 "+
			"LEFT JOIN Vuosikate D "+
			"ON A.vuosi = D.vuosi-3 "+
			"LEFT JOIN Vuosikate E "+
			"ON A.vuosi = E.vuosi-4 "+
			f"WHERE D.kunta_id = {kunta_id} AND E.kunta_id={kunta_id} AND E.vuosi is not NULL;")
	
	sql3 = ["ALTER TABLE TEMP_TABLE DROP COLUMN vuosi;",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'vuosi:1';",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'vuosi:2';",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'vuosi:3';",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'vuosi:4';",
			"ALTER TABLE TEMP_TABLE DROP COLUMN id;",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'id:1';",
			"ALTER TABLE TEMP_TABLE DROP COLUMN toimintakate;",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'toimintakate:1';",
			"ALTER TABLE TEMP_TABLE DROP COLUMN kunta_id;",
			"ALTER TABLE TEMP_TABLE DROP COLUMN 'kunta_id:1';"]
	
	sql4 = "SELECT * FROM TEMP_TABLE"
	
	return sql1, sql2, sql3, sql4
	