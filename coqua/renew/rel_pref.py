import pandas as pd
import functools
import sqlite3

# 嗜好bitのリストを返す
# [True, False, ..., True]のようなものを返す
# 現在は使われていないめう
def pref_bits(row, pref_words):
	def is_pattern_in_row(itr, s):
		try:
			return True if next(itr) in s else is_pattern_in_row(itr, s)
		except StopIteration:
			return False
	lst = [is_pattern_in_row(iter(pattern), str(row['name']) + str(row['history']) + str(row['description'])) for pattern in pref_words]
	return lst


# 嗜好bitのリレーションをリメイクする
# 嗜好に当てはまるなら1, あてはまらないなら0を格納する
def make_rel_pref(tablename, dbcur, csvpath):
	df = pd.read_csv(csvpath)
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# カテゴリ数
	num_cat = 10
	# 嗜好bitのテーブルを作成
	dbcur.execute(
			"create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ functools.reduce(
				lambda x,y : x + ", " + y,
				["pref" + str(i) + " INTEGER" for i in range(1, num_cat + 1)]
				) + ", primary key(recipe_id))")
	# タプルの挿入
	for i, row in df.iterrows():
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ", "
				+ functools.reduce(
					lambda x,y : str(x) + ", " + str(y),
					[row[i] for i in range(1, num_cat + 1)])
					+ ")")
	dbcur.execute(F"create index idx_pref_recipe_id on {tablename}(recipe_id)")
	for i in range(1, cum_cat + 1):
		dbcur.execute(F"create index idx_pref_bit{i} on {tablename}(pref{i})")
