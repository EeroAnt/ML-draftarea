from queries.queries import *
from sqlite3 import connect

def fetch_data(kunta_id):
	data = []
	db = connect("masterdb.db")
	drop_temp_table, initial_query, drop_columns, final_query = sql_for_two_years_of_data_and_three_next_for_targets(kunta_id)
	db.execute(drop_temp_table)
	db.commit()
	db.execute(initial_query)
	db.commit()
	for i in drop_columns:
		db.execute(i)
		db.commit()
	result = db.execute(final_query).fetchall()
	db.commit()
	# suodatan pois ne rivit, joissa on None-arvoja, toistaiseksi rikkovat mallin. Ekalla testillä niitä oli ~ 4 / 3000
	result = list(filter(lambda x: x.count(None) == 0, result))
	for i in result:
		data.append(i)
	return data


#Tätä voi varmasti laajentaa esim tekemään halutut rajaukset parametrien avulla
def get_wanted_municipality_ids():
	db = connect("masterdb.db")
	sql = municipality_id_filter()
	municipality_ids = db.execute(sql).fetchall()
	return municipality_ids