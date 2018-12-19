import pandas as pd
import sys
import string
import functools
import sqlite3

def pref_bits(row, pref_words):
	def is_pattern_in_row(itr, s):
		try:
			return True if next(itr) in s else is_pattern_in_row(itr, s)
		except StopIteration:
			return False
	lst = [is_pattern_in_row(iter(pattern),
					str(row['name']) + str(row['history']) + str(row['description']))
				for pattern in pref_words]
	return lst


def make_rel_pref(dbname, datpath):
	df = pd.read_csv(
		datpath, 
		usecols = [
			'recipe_id',
			'name',
			'history',
			'description'])
	# 嗜好リスト
	pref_words = [
			['簡単', '時短', '手軽', 'シンプル'],
			['子', '息子', '娘'],
			['ヘルシー', '野菜', 'カロリー', 'ダイエット'],
			['弁当'],
			['ボリューム'],
			['節約', '安い'],
			['おつまみ', '居酒屋'],
			['殿堂入り']]
	# データベース作成
	dbname = 'db.db'
	dbconn = sqlite3.connect(dbname)
	dbcur  = dbconn.cursor()
	tablename = 'preferable_bits'
	# すでにテーブルがあれば削除する
	dbcur.execute("drop table if exists " + tablename)
	# 嗜好bitのテーブルを作成
	dbcur.execute(
			"create table " + tablename + " ("
			+ "recipe_id INTEGER,"
			+ functools.reduce(
				lambda x,y : x + ", " + y,
				["pref" + str(i) + " INTEGER"
					for i in range(1, len(pref_words) + 1)])
			+ ", primary key(recipe_id))")
	# タプルの挿入
	for i, row in df.iterrows():
		dbcur.execute("insert into " + tablename + " values("
				+ str(row['recipe_id']) + ", "
				+ functools.reduce(
					lambda x,y : x + ", " + y,
					map(lambda x : "1" if x else "0",
						pref_bits(row, pref_words)))
				+ ")")
	# コミット
	dbconn.commit()
	# データベースを閉じる
	dbconn.close()


if __name__ == '__main__':
	args = sys.argv
	path = args[1]
	make_rel_pref('db.db', path)

