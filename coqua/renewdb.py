import pandas as pd
import sqlite3
from renew import make_rel_name
from renew import make_rel_pref
from renew import make_rel_image
from renew import make_rel_author
from renew import make_rel_publication
from renew import make_rel_ingredients
from renew import make_rel_yield
from renew import make_rel_cooktime

def renewdb(dbcur):
	# データベースを再構築します
	# テーブルの作成
	make_rel_name('names', dbcur, 'formatted.csv')
	make_rel_pref('preferable_bits', dbcur, 'formatted.csv')
	make_rel_image('images', dbcur, 'formatted.csv')
	make_rel_author('authors', dbcur, 'formatted.csv')
	make_rel_publication('publications', dbcur, 'formatted.csv')
	make_rel_ingredients('ingredients', dbcur, '../preprocessed/filtered_ingredient.csv')
	make_rel_ingredients('ingredients', dbcur, '../preprocessed/filtered_ingredient.csv')
	make_rel_cooktime('cooktimes', dbcur, '../preprocessed/cookTime_num.csv')

if __name__ == '__main__':
	dbconn = sqlite3.connect('coqua.db')
	dbcur  = dbconn.cursor()
	dbconn.set_trace_callback(print)
	renewdb(dbcur)
	dbconn.commit()
	dbconn.close()

