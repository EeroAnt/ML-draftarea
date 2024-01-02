import pandas
import sqlite3
import os
import csv
import numpy as np 
## Täällä kun kahtoo parametrit kohdilleen, niin saa lisättyä excel_into_dp.py ajamalla asioita master-tietokantaan. Ei pidä ajaa turhaan, tulee harmeja.

def read_excel(name):
	dataframe = pandas.read_excel(os.path.realpath(f"exceleita/{name}.xlsx"))
	# näillä voi tutkia taulukon rakennetta
	# print(dataframe.loc[2].to_numpy())
	# print(dataframe.info())
	# print(dataframe[2:-39])
	return dataframe[2:-39]

def insert_from_excel(dataframe):
	db = sqlite3.connect("masterdb.db")
	db.isolation_level = None
	kuntakoodit = municipality_codes()
	for i in range(2,311):
		data = dataframe.loc[i].to_numpy()
		sql = ("INSERT INTO Asukasluku ("+
		 		"kunta_id, "+
				"Asukasluvun_ka) "+
				"values (?,?);"
				)
		db.execute(sql,(kuntakoodit[data[0]],int(data[-1])))
		db.commit()
		# if type(data[0]) == str:
		# 	kunta = kuntakoodit[data[0]]
		# sql_query_insert = tuple(data[1:])+tuple([kunta])
		# sql=(f"INSERT INTO Pendeloivat ("+
		# 		"vuosi,"+
		# 		"Toinen24,"+
		# 		"Toinen34,"+
		# 		"Toinen44,"+
		# 		"Toinen54,"+
		# 		"Toinen64,"+
		# 		"Toinen74,"+
		# 		"Alin24,"+
		# 		"Alin34,"+
		# 		"Alin44,"+
		# 		"Alin54,"+
		# 		"Alin64,"+
		# 		"Aline74,"+
		# 		"Ylempi24,"+
		# 		"Ylempi34,"+
		# 		"Ylempi44,"+
		# 		"Ylempi54,"+
		# 		"Ylempi64,"+
		# 		"Ylempi74,"+
		# 		"Ei24,"+
		# 		"Ei34,"+
		# 		"Ei44,"+
		# 		"Ei54,"+
		# 		"Ei64,"+
		# 		"Ei74,"+
		# 		"kunta_id) "+
		# 		"values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);")
		# db.execute(sql, sql_query_insert)
		# db.commit()

def municipality_codes():
	kuntakoodit = {}
	with open("exceleita/kuntatunnukset.csv", mode='r',encoding='cp1250',newline='') as csv_file:
		csv_read = csv.DictReader(csv_file,delimiter=";")
		for row in csv_read:
			if row["classificationItemName"]!='Vĺrdö':
				kuntakoodit[row["classificationItemName"]]=row["code"][1:-1]
			else:
				kuntakoodit['Vårdö']=row["code"][1:-1]
	return kuntakoodit

def remove_numbered_tables():
	db = sqlite3.connect("masterdb.db")
	db.isolation_level = None
	for i in range(999):
		if i<10:
			kunta ="00"+str(i)
		elif i<100:
			kunta ="0"+str(i)
		else:
			kunta =str(i)
		db.execute(f"DROP TABLE if exists vaestorakenne{kunta};")
		db.commit()

def add_table(name):
	db = sqlite3.connect("masterdb.db")
	db.isolation_level = None
	sql =(f"CREATE Table if not exists {name} ("+
			"id INTEGER PRIMARY KEY, "+
			"kunta_id, "+
			"Asukasluvun_ka);")
	db.execute(sql)

def null_mapper(x):
	if type(x) in [int, float, np.int64, np.float64, np.float32, np.float16] :
		return x
	else:
		return '.'

def insert_from_numbered_table():
	db = sqlite3.connect("masterdb.db")
	db.isolation_level = None
	for i in range(1000):
		if i<10:
			kunta ="00"+str(i)
		elif i<100:
			kunta ="0"+str(i)
		else:
			kunta =str(i)
		sql_check = (f"SELECT name FROM sqlite_master WHERE type='table' AND name='vaestorakenne{kunta}';")
		if db.execute(sql_check).fetchall():
			sql_get_data = (
				"SELECT "+
				"vuosi, "+
				"NuoretYhteensa, "+
				"TyovoimaN, "+
				"TyollisetN, "+
				"AlleViisitoista, "+
				"OpiskelijatN, "+
				"ElakelaisetN, "+
				"Aikuiset, "+
				"TyovoimaA, "+
				"TyollisetA, "+
				"OpiskelijatA, "+
				"VarusmiehetA, "+
				"ElakelaisetA, "+
				"Iakkaat, "+
				"TyovoimaI, "+
				"TyollisetI, "+
				"OpiskelijatI, "+
				"ElakelaisetI "+
				f"FROM vaestorakenne{kunta};")
			data = db.execute(sql_get_data).fetchall()
			for i in data:
				data_to_insert = tuple(map(null_mapper,i))+(kunta,)
				sql_query_insert = (f"INSERT INTO Vaestorakenne ("+
						"vuosi, "+
						"Nuoria_yhteensa, "+
						"Tyovoima_nuoret, "+
						"Tyolliset_nuoret, "+
						"Alle_15, "+
						"Opiskelijat_nuoret, "+
						"Elake_nuoret, "+
						"Aikuisia_yhteensa, "+
						"Tyovoima_aikuiset, "+
						"Tyolliset_aikuiset, "+
						"Opiskelijat_aikuiset, "+
						"Varusmiehet_aikuiset, "+
						"Elake_aikuiset, "+
						"Iakkaat_yhteensa, "+
						"Tyovoima_iakkaat, "+
						"Tyolliset_iakkaat, "+
						"Opiskelijat_iakkaat, "+
						"Elake_iakkaat, "+
						"Kunta_id)"
						f"values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);")
				db.execute(sql_query_insert, data_to_insert)
				db.commit()