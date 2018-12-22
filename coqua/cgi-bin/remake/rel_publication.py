import pandas as pd
import ast
import string
import sqlite3
import datetime

def make_rel_publication(tablename, dbcur, df):
	dbcur.execute("drop table if exists " + tablename)
	dbcur.execute("create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ "date TEXT,"
			+ "year INTEGER,"
			+ "month INTEGER,"
			+ "day INTEGER,"
			+ "count INTEGER)")
	for i, row in df.iterrows():
		date = datetime.datetime.strptime(row['datePublished'], '%Y-%m-%d')
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ','
				+ '"' + row['datePublished'] + '",'
				+ str(date.year) + ',' 
				+ str(date.month) + ','
				+ str(date.day) + ','
				+ str((date - datetime.datetime(2000,1,1,0,0)).days) + ')')
