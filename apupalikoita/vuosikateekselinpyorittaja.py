import pandas
import sqlite3
import os
import csv
import numpy as np 
## Täällä kun kahtoo parametrit kohdilleen, niin saa lisättyä excel_into_dp.py ajamalla asioita master-tietokantaan. Ei pidä ajaa turhaan, tulee harmeja.

def read_excel(name):
	dataframe = pandas.read_excel(os.path.realpath(f"talousdata/{name}.xlsx"))
	# näillä voi tutkia taulukon rakennetta
	# print(dataframe.loc[2].to_numpy())
	# print(dataframe.info())
	# print(dataframe[5:-35])
	return dataframe[5:-35]

def add_to_db(dataframe):
	db = sqlite3.connect("masterdb.db")
	db.isolation_level = None
	sql =(f"CREATE Table if not exists Pendeloivat ("+
			"id INTEGER PRIMARY KEY,"+
			"vuosi INTEGER,"+
			"Toinen24 INTEGER,"+
			"Toinen34 INTEGER,"+
			"Toinen44 INTEGER,"+
			"Toinen54 INTEGER,"+
			"Toinen64 INTEGER,"+
			"Toinen74 INTEGER,"+
			"Alin24 INTEGER,"+
			"Alin34 INTEGER,"+
			"Alin44 INTEGER,"+
			"Alin54 INTEGER,"+
			"Alin64 INTEGER,"+
			"Aline74 INTEGER,"+
			"Ylempi24 INTEGER,"+
			"Ylempi34 INTEGER,"+
			"Ylempi44 INTEGER,"+
			"Ylempi54 INTEGER,"+
			"Ylempi64 INTEGER,"+
			"Ylempi74 INTEGER,"+
			"Ei24 INTEGER,"+
			"Ei34 INTEGER,"+
			"Ei44 INTEGER,"+
			"Ei54 INTEGER,"+
			"Ei64 INTEGER,"+
			"Ei74 INTEGER,"+
			"kunta_id);")
	db.execute(sql)
	kuntakoodit = municipality_codes()
	for i in range(5,10820):
		data = dataframe.loc[i].to_numpy()
		if type(data[0]) == str:
			kunta = kuntakoodit[data[0]]
		sql_query_insert = tuple(data[1:])+tuple([kunta])
		sql=(f"INSERT INTO Pendeloivat ("+
				"vuosi,"+
				"Toinen24,"+
				"Toinen34,"+
				"Toinen44,"+
				"Toinen54,"+
				"Toinen64,"+
				"Toinen74,"+
				"Alin24,"+
				"Alin34,"+
				"Alin44,"+
				"Alin54,"+
				"Alin64,"+
				"Aline74,"+
				"Ylempi24,"+
				"Ylempi34,"+
				"Ylempi44,"+
				"Ylempi54,"+
				"Ylempi64,"+
				"Ylempi74,"+
				"Ei24,"+
				"Ei34,"+
				"Ei44,"+
				"Ei54,"+
				"Ei64,"+
				"Ei74,"+
				"kunta_id)"+
				"values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);")
		db.execute(sql, sql_query_insert)
		db.commit()

def municipality_codes():
	kuntakoodit = {}
	with open("talousdata/kuntatunnukset.csv", mode='r',encoding='cp1250',newline='') as csv_file:
		csv_read = csv.DictReader(csv_file,delimiter=";")
		for row in csv_read:
			if row["classificationItemName"]!='Vĺrdö':
				kuntakoodit[row["classificationItemName"]]=row["code"][1:-1]
			else:
				kuntakoodit['Vårdö']=row["code"][1:-1]
	return kuntakoodit

def remove_tables():
	db = sqlite3.connect("masterdb.db")
	db.isolation_level = None
	for i in range(999):
		if i<10:
			kunta ="00"+str(i)
		elif i<100:
			kunta ="0"+str(i)
		else:
			kunta =str(i)
		db.execute(f"DROP TABLE if exists Kuntaan_toihin_tulevat{kunta};")
		db.commit()
