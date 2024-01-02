import pandas
import sqlite3

database = sqlite3.connect("data.db")
database.isolation_level = None

dataframe1 = pandas.read_excel('test.xlsx')
kunta = -1
print([dataframe1.loc[4][1:].to_numpy()])
for i in range(1,10815):
	if type(dataframe1.loc[i][0]) != float:
		kunta = dataframe1.loc[i][0] 
		kunta = kunta.replace(" ","")
		kunta = kunta.replace("-","")
		database.execute(
		f"INSERT INTO {kunta} (vuosi, Tyovoima, Tyolliset, Tyottomat, Tyovoiman_ulkopuolella,"+
		"alle_viisitoista, TyovoimaA, TyollisetA, TyottomatA, Tyovoiman_ulkopuolellaA,"+
		"alle_viisitoistaA, TyovoimaB, TyollisetB, TyottomatB, Tyovoiman_ulkopuolellaB,"+
		"TyovoimaC, TyollisetC, TyottomatC, Tyovoiman_ulkopuolellaC) values "+
		"(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", dataframe1.loc[i][1:].to_numpy())
	elif kunta != -1:
		database.execute(
		f"INSERT INTO {kunta} (vuosi, Tyovoima, Tyolliset, Tyottomat, Tyovoiman_ulkopuolella,"+
		"alle_viisitoista, TyovoimaA, TyollisetA, TyottomatA, Tyovoiman_ulkopuolellaA,"+
		"alle_viisitoistaA, TyovoimaB, TyollisetB, TyottomatB, Tyovoiman_ulkopuolellaB,"+
		"TyovoimaC, TyollisetC, TyottomatC, Tyovoiman_ulkopuolellaC) values "+
		"(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", dataframe1.loc[i][1:].to_numpy())


print(dataframe1.info())