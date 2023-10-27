import pandas
import sqlite3
import os
import csv 
## Täällä kun kahtoo parametrit kohdilleen, niin saa lisättyä excel_into_dp.py ajamalla asioita master-tietokantaan. Ei pidä ajaa turhaan, tulee harmeja.

def read_excel(name):
    dataframe = pandas.read_excel(os.path.realpath(f"talousdata/{name}.xlsx"))
    # print(dataframe.loc[2].to_numpy())
    # print(dataframe.info())
    # print(dataframe[5:-35])
    return dataframe[5:-35]

def add_to_db(dataframe):
    db = sqlite3.connect("vuosikate.db")
    db.isolation_level = None
    kuntakoodit = municipality_codes()
    for i in range(5,10820):
        data = dataframe.loc[i].to_numpy()
        sql_query_insert = tuple(data[1:])
        if type(data[0]) == str:
            kunta = kuntakoodit[data[0]]
            db.execute(f"CREATE Table if not exists Kuntaan_toihin_tulevat{kunta} (id INTEGER PRIMARY KEY, vuosi INTEGER, ToinenA INTEGER, AlinA INTEGER, YlempiA INTEGER, EiA INTEGER, ToinenB INTEGER, AlinB INTEGER, YlempiB INTEGER, EiB INTEGER, ToinenC INTEGER, AlinC INTEGER, YlempiC INTEGER, EiC INTEGER, ToinenD INTEGER, AlinD INTEGER, YlempiD INTEGER, EiD INTEGER, ToinenE INTEGER, AlinE INTEGER, YlempiE INTEGER, EiE INTEGER, ToinenF INTEGER, AlinF INTEGER, YlempiF INTEGER, EiF INTEGER);")
        db.execute(f"INSERT INTO Kuntaan_toihin_tulevat{kunta} (vuosi, ToinenA, AlinA, YlempiA, EiA, ToinenB, AlinB, YlempiB, EiB, ToinenC, AlinC, YlempiC, EiC, ToinenD, AlinD, YlempiD, EiD, ToinenE, AlinE, YlempiE, EiE, ToinenF, AlinF, YlempiF, EiF) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", sql_query_insert)
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
# #aja ensiksi vain nämä. Tarkista taulukon koko ja rivien rakenne
# print(dataframe.loc[2].to_numpy())
# print(dataframe.info())

# # seuraava pätkä yhdistää uuden excelin datan olemassaolevaan tietokantaan.
# kunta = -1
# for i in range(310):
#     data = dataframe.loc[i].to_numpy()
#     if data[0]>0:
#         if data[0]<10:
#             kunta ="`00"+str(int(data[0]))+"`"
#         elif data[0]<100:
#             kunta ="`0"+str(int(data[0]))+"`"
#         else:
#             kunta ="`"+str(int(data[0]))+"`"
#         # print(kunta)
#         # db.execute(
#         #         f"CREATE TABLE if not exists {kunta} (id INTEGER PRIMARY KEY, vuosi INTEGER,"+
#         #         "toimintakate, vuosikate)")
#     # print(dataframe.loc[i][1],dataframe.loc[i][2],dataframe.loc[i][3])
#     db.execute(
#         f"INSERT INTO {kunta}(vuosi, toimintakate, vuosikate) values"+
#         "(?,?,?);", [int(dataframe.loc[i][1]),int(dataframe.loc[i][2]),int(dataframe.loc[i][3])])
