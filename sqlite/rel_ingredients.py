import pandas as pd
import string
import functools
import sqlite3

# １つのレシピの材料リストを返す
# [['大根', '１切れ'], ['白菜', '1/8玉']] のようになる
def ingredients_list(row):
	tmp = str.split(row['recipeIngredient'][1:-1], ",")
	tmp = map(lambda x : x.strip("' "), tmp)
	tmp = map(lambda x : str.split(x, " "), tmp)
	tmp = filter(lambda x : len(x) == 2, tmp)
	return list(tmp)


# 材料のリレーションをリメイクする
def make_rel_ingredients(tablename, dbcur, df):
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# 材料のテーブルを作成
	dbcur.execute(
			"create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ "name TEXT,"
			+ "amount TEXT)")
	# タプルの挿入
	for i, row in df.iterrows():
		for tup in ingredients_list(row):
			dbcur.execute(
					"insert into " + tablename + " values("
					+ str(row['recipe_id']) + ','
					+ "'" + str(tup[0]) + "',"
					+ "'" + str(tup[1]) + "')")
