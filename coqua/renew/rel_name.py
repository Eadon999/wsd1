import pandas as pd
import sqlite3

def make_rel_name(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	dbcur.execute(F"drop table if exists {tablename}")
	dbcur.execute(
			F"create table {tablename} ("
			+ "recipe_id INTEGER,"
			+ "name TEXT"
			+ ", primary key(recipe_id))")
	for i, row in df.iterrows():
		dbcur.execute(F"insert into {tablename} values("
				+ str(row['recipe_id']) + ", "
				+ "'" + str(row['name']) + "')")
	dbcur.execute(F"create index idx_name_recipe_id on {tablename}(recipe_id)")
