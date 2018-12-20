import pandas as pd
import re
import sys
import string
import functools
import sqlite3
from rel_pref        import make_rel_pref
from rel_author      import make_rel_author
from rel_ingredients import make_rel_ingredients
from rel_yield       import make_rel_yield

if __name__ == '__main__':
	args = sys.argv
	path = args[1]
	# csvを読み込む
	df = pd.read_csv(
			path,
			usecols = [
				'recipe_id',
				'author',
				'name',
				'history',
				'description',
				'advice',
				'categories',
				'related_keywords',
				'datePublished',
				'recipeYield',
				'recipeIngredient'])
	# データベースの作成
	dbname = 'db.db'
	dbconn = sqlite3.connect(dbname)
	dbcur  = dbconn.cursor()
	# debug用
	dbconn.set_trace_callback(print)
	# テーブルの作成
	make_rel_pref('preferable_bits', dbcur, df)
	make_rel_author('authour', dbcur, df)
	make_rel_ingredients('ingredients', dbcur, df)
	make_rel_yield('yields', dbcur, df)
	# コミット
	dbconn.commit()
	# データベースを閉じる
	dbconn.close()

