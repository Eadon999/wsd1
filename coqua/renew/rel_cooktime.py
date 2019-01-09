import pandas as pd
import sqlite3

def make_rel_cooktime(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# 材料のテーブルを作成
	dbcur.execute(
			"create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ "cooktime INTEGER)")
	# タプルの挿入
	for i, row in df.iterrows():
		dbcur.execute(
				"insert into " + tablename + " values("
				+ str(row['recipe_id']) + ','
				+ str(row['cookTime']) + ")")
