import pandas as pd
import ast
import string
import sqlite3

def make_rel_image(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	dbcur.execute("drop table if exists " + tablename)
	dbcur.execute("create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ "url TEXT)")
	for i, row in df.iterrows():
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ','
				+ '"' + str(row['image']) + '")')
