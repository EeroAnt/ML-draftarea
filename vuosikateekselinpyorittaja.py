import pandas
import sqlite3
import os

dataframe = pandas.read_excel(os.path.realpath("talousdata/katteet2020.xlsx"))
db = sqlite3.connect("vuosikate.db")
db.isolation_level = None

#aja ensiksi vain nämä. Tarkista taulukon koko ja rivien rakenne
print(dataframe.loc[2].to_numpy())
print(dataframe.info())

# seuraava pätkä yhdistää uuden excelin datan olemassaolevaan tietokantaan.
kunta = -1
for i in range(310):
    data = dataframe.loc[i].to_numpy()
    if data[0]>0:
        if data[0]<10:
            kunta ="`00"+str(int(data[0]))+"`"
        elif data[0]<100:
            kunta ="`0"+str(int(data[0]))+"`"
        else:
            kunta ="`"+str(int(data[0]))+"`"
        # print(kunta)
        # db.execute(
        #         f"CREATE TABLE if not exists {kunta} (id INTEGER PRIMARY KEY, vuosi INTEGER,"+
        #         "toimintakate, vuosikate)")
    # print(dataframe.loc[i][1],dataframe.loc[i][2],dataframe.loc[i][3])
    db.execute(
        f"INSERT INTO {kunta}(vuosi, toimintakate, vuosikate) values"+
        "(?,?,?);", [int(dataframe.loc[i][1]),int(dataframe.loc[i][2]),int(dataframe.loc[i][3])])
