import pandas as pd
import functools
import sqlite3

# 嗜好bitのリストを返す
# [True, False, ..., True]のようなものを返す
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
	pref_words = [
			['簡単', '時短', '手軽', 'シンプル'],
			['子', '息子', '娘'],
			['ヘルシー', '野菜', 'カロリー', 'ダイエット'],
			['弁当'],
			['ボリューム'],
			['節約', '安い'],
			['おつまみ', '居酒屋'],
			['殿堂入り']]
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# 嗜好bitのテーブルを作成
	dbcur.execute(
			"create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ functools.reduce(
				lambda x,y : x + ", " + y,
				["pref" + str(i) + " INTEGER" for i in range(1, len(pref_words) + 1)]
				) + ", primary key(recipe_id))")
	# タプルの挿入
	for i, row in df.iterrows():
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ", "
				+ functools.reduce(
					lambda x,y : x + ", " + y,
					map(lambda x : "1" if x else "0",
						pref_bits(row, pref_words)))
					+ ")")
	dbcur.execute(F"create index idx_pref_recipe_id on {tablename}(recipe_id)")
	dbcur.execute(F"create index idx_pref_bit1 on {tablename}(pref1)")
	dbcur.execute(F"create index idx_pref_bit2 on {tablename}(pref2)")
	dbcur.execute(F"create index idx_pref_bit3 on {tablename}(pref3)")
	dbcur.execute(F"create index idx_pref_bit4 on {tablename}(pref4)")
	dbcur.execute(F"create index idx_pref_bit5 on {tablename}(pref5)")
	dbcur.execute(F"create index idx_pref_bit6 on {tablename}(pref6)")
	dbcur.execute(F"create index idx_pref_bit7 on {tablename}(pref7)")
	dbcur.execute(F"create index idx_pref_bit8 on {tablename}(pref8)")
