import pandas
import sqlite3
import os

def read_excel(name):
    dataframe = pandas.read_excel(os.path.realpath(f"talousdata/{name}.xlsx"))
    # print(dataframe.loc[2].to_numpy())
    # print(dataframe.info())
    # print(dataframe[1:-3])
    return dataframe[1:-3]

def add_to_db(dataframe):
    db = sqlite3.connect("masterdb.db")
    db.isolation_level = None
    db.execute("CREATE TABLE if not exists BKT (id INTEGER PRIMARY KEY, vuosi INTEGER,BKT INTEGER);")
    for i in range(1,48):
        data = dataframe.loc[i].to_numpy()
        db.execute("INSERT INTO BKT (vuosi, BKT) values(?,?);", [data[0],data[1]])
        

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
