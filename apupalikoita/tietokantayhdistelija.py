import sqlite3

vaestotietokanta = sqlite3.connect("vaestorakenne_ja_tyollisuus.db")
vuosikatekanta = sqlite3.connect("vuosikate.db")
yhdistettykanta = sqlite3.connect("masterdb.db")

def select_all(sql, taulunnimi):
    cursor = sql.cursor()
    cursor.execute(f'SELECT * From "{taulunnimi}"')
    return cursor.fetchall()

# vaestocursor = vaestotietokanta.cursor()
# vaestocursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# vaestotaulutx = vaestocursor.fetchall()
# vaestotauluty = []
# for i in vaestotaulutx:
#     vaestotauluty.append(i[0])

vuosikatecursor = vuosikatekanta.cursor()
vuosikatecursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
vuosikatetaulutx = vuosikatecursor.fetchall()
vuosikatetauluty = []
for i in vuosikatetaulutx:
    vuosikatetauluty.append(i[0])

# kolumnit = vaestotietokanta.execute("PRAGMA table_info('005');").fetchall()
# print(len(kolumnit))
# for i in kolumnit:
#     print(i[1])
# for i in vuosikatetauluty:
#     yhdistettykanta.execute(
#                 f"CREATE TABLE if not exists vuosikate{i} (id INTEGER PRIMARY KEY, vuosi INTEGER,"+
#                 "toimintakate, vuosikate)")
    
# for i in vaestotauluty:
#     yhdistettykanta.execute(
#         f"CREATE TABLE if not exists vaestorakenne{i} (id INTEGER PRIMARY KEY, vuosi, NuoretYhteensa, "+
#             "TyovoimaN, TyollisetN, TyottomatN, TyonvoimanulkopuolellaolevatN, AlleViisitoista,OpiskelijatN, "+
#             "VarusmiehetN, ElakelaisetN, MuutTyovoimanUlkopuolellaN, Aikuiset, TyovoimaA, TyollisetA, "+
#             "TyottomatA, TyonvoimanulkopuolellaolevatA, OpiskelijatA, VarusmiehetA, ElakelaisetA, "+
#             "MuutTyovoimanUlkopuolellaA, Iakkaat, TyovoimaI, TyollisetI, TyottomatI, TyonvoimanulkopuolellaolevatI, "+
#             "OpiskelijatI, ElakelaisetI, MuutTyovoimanUlkopuolellaI)"), 

# for i in vaestotauluty:
#     print("\n"+ f"vaestorakenne"+i+"\n")
#     taulu = select_all(vaestotietokanta,i)
#     cur = yhdistettykanta.cursor()
#     for ii in taulu:
#         print(ii)
#         cur.execute(f'INSERT INTO "vaestorakenne{i}" (vuosi, NuoretYhteensa, '+
#             "TyovoimaN, TyollisetN, TyottomatN, TyonvoimanulkopuolellaolevatN, AlleViisitoista,OpiskelijatN, "+
#             "VarusmiehetN, ElakelaisetN, MuutTyovoimanUlkopuolellaN, Aikuiset, TyovoimaA, TyollisetA, "+
#             "TyottomatA, TyonvoimanulkopuolellaolevatA, OpiskelijatA, VarusmiehetA, ElakelaisetA, "+
#             "MuutTyovoimanUlkopuolellaA, Iakkaat, TyovoimaI, TyollisetI, TyottomatI, TyonvoimanulkopuolellaolevatI, "+
#             "OpiskelijatI, ElakelaisetI, MuutTyovoimanUlkopuolellaI) values "+
#             "(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", ii[1:])
#     yhdistettykanta.commit()
#     cur.close()

for i in vuosikatetauluty:
    taulu = select_all(vuosikatekanta,i)
    cur = yhdistettykanta.cursor()
    for ii in taulu:
        cur.execute(f'INSERT INTO "vuosikate{i}" (vuosi, toimintakate, vuosikate) values (?,?,?);', ii[1:])
    yhdistettykanta.commit()
    cur.close()