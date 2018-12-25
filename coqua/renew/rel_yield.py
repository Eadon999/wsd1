import pandas as pd
import string
import sqlite3

# 何人分かのリレーションをリメイクする
def make_rel_yield(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# 料理の分量テーブルを作成
	dbcur.execute("create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ "yield TEXT"
			+ ", primary key(recipe_id))")
	# タプルの挿入
	for i, row in df.iterrows():
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ", "
				+ "'" + str(row['servings']) + "'"
				+ ")")
