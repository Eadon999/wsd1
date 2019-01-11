import pandas as pd
import string
import functools
import sqlite3
import ast

# 材料のリレーションをリメイクする
def make_rel_ingredients(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# 材料のテーブルを作成
	dbcur.execute(
			F"create table {tablename} ("
			+ "recipe_id INTEGER,"
			+ "name TEXT,"
			+ "pron TEXT,"
			+ "amount TEXT)")
	# タプルの挿入
	for i, row in df.iterrows():
		lst = list(zip(
			ast.literal_eval(row['ingredients']),
			ast.literal_eval(row['ingredients_yomi']),
			ast.literal_eval(row['amount'])))
		for tup in lst:
			dbcur.execute(
					"insert into " + tablename + " values("
					+ str(row['recipe_id']) + ','
					+ "'" + str(tup[0]) + "',"
					+ "'" + str(tup[1]) + "',"
					+ "'" + str(tup[2]) + "')")
	dbcur.execute(F"create index idx_ingredients_recipe_id on {tablename}(recipe_id)")
	dbcur.execute(F"create index idx_ingredients_name on {tablename}(name)")
	dbcur.execute(F"create index idx_ingredients_pron on {tablename}(pron)")

