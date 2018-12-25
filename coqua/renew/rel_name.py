import pandas as pd
import functools
import sqlite3

def make_rel_name(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	dbcur.execute("drop table if exists " + tablename)
	dbcur.execute(
			"create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ "name TEXT"
			+ ", primary key(recipe_id))")
	for i, row in df.iterrows():
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ", "
				+ "'" + str(row['name']) + "')")
