import json
import glob
import sqlite3
import datetime
import coquadb
import pandas as pd
import ast

def init_tables(cdb): # テーブルの初期化
	# names(料理名)
	cdb.drop('names')
	cdb.execute("CREATE TABLE names (recipe_id INTEGER, name TEXT, PRIMARY KEY(recipe_id))")
	cdb.execute("CREATE INDEX idx_name_recipe_id ON names(recipe_id)")
	# author(作者)
	cdb.drop('authors')
	cdb.execute("CREATE TABLE authors (recipe_id INTEGER, author TEXT, PRIMARY KEY(recipe_id))")
	cdb.execute("CREATE INDEX idx_author_recipe_id ON authors(recipe_id)")
	# images(画像URL)
	cdb.drop('images')
	cdb.execute("CREATE TABLE images (recipe_id INTEGER, url TEXT, PRIMARY KEY(recipe_id))")
	cdb.execute("CREATE INDEX idx_image_recipe_id ON images(recipe_id)")
	# publications(公開日時)
	cdb.drop('publications')
	cdb.execute("CREATE TABLE publications (recipe_id INTEGER, date TEXT, year INTEGER, month INTEGER, day INTEGER, count INTEGER, PRIMARY KEY(recipe_id))")
	cdb.execute("CREATE INDEX idx_publication_recipe_id ON publications(recipe_id)")
	# ingredients (材料名)
	cdb.drop('ingredients')
	cdb.execute("CREATE TABLE ingredients (recipe_id INTEGER, name TEXT, pron TEXT, amount TEXT, converted REAL, unit TEXT)")
	cdb.execute("CREATE INDEX idx_ingredient_recipe_id ON ingredients(recipe_id)")
	cdb.execute("CREATE INDEX idx_ingredient_name ON ingredients(name)")
	cdb.execute("CREATE INDEX idx_ingredient_pron ON ingredients(pron)")
	# cooktime(調理時間)
	cdb.drop('cooktimes')
	cdb.execute("CREATE TABLE cooktimes (recipe_id INTEGER, cooktime INTEGER, PRIMARY KEY(recipe_id))")
	cdb.execute("CREATE INDEX idx_cooktime_recipe_id ON cooktimes(recipe_id)")
	# categories(カテゴリ分け)
	# yields(何人分か)
	cdb.drop('yields')
	cdb.execute("CREATE TABLE yields (recipe_id INTEGER, yield TEXT)") # PRIMARYキー指定ないのはUNIQUE成約を満たせないから
	cdb.execute("CREATE INDEX idx_yield_recipe_id ON yields(recipe_id)")


def insert_records(cdb):
	# jsonファイルから
	jlst = glob.glob("../../../recipe0115/*")
	for x in jlst:
		with open(x) as f:
			j = json.load(f)
			rid = j['recipe_id']
			# name(料理名)
			cdb.execute('INSERT INTO names values(%s,"%s")' % (rid, j['name'].replace('"', '')))
			# author(作者)
			cdb.execute('INSERT INTO authors values(%s, "%s")' % (rid, j['author']['name'].replace('"', '')))
			# images(画像URL)
			cdb.execute('INSERT INTO images values(%s, "%s")' % (rid, j['image']))
			# publications(公開日時)
			date = datetime.datetime.strptime(j['datePublished'], '%Y-%m-%d')
			cdb.execute('INSERT INTO publications values(%s, "%s", %s, %s, %s, %s)'
				% (rid, j['datePublished'], str(date.year), str(date.month), str(date.day), str((date - datetime.datetime(2000,1,1,0,0)).days)))
			# cooktimes(調理時間)
			cdb.execute('INSERT INTO cooktimes values(%s, %s)' % (rid, j['cooktime'][2:-2]))
	# 各CSVファイルから
	# ingredients(材料) yields
	#df = pd.read_csv("../preprocessed/filtered_ingredient.csv")
	#for i, row in df.iterrows():
	#	lst = list(zip(
	#		ast.literal_eval(row['ingredients']),
	#		ast.literal_eval(row['ingredients_yomi']),
	#		ast.literal_eval(row['amount'])))
	#	for tup in lst:
	#		cdb.execute("INSERT INTO ingredients values(" + str(row['recipe_id']) + ','
	#				+ "'" + str(tup[0]) + "','" + str(tup[1]) + "','" + str(tup[2]).replace("'",'').replace('"','') + "')")
	#		if pd.isnull(row['servings']) == False:
	#			cdb.execute("INSERT INTO yields values(" + str(row['recipe_id']) + ',' + str(row['servings']) + ")")
	df = pd.read_csv("../preprocessed/db_ingredients.csv")
	for i, row in df.iterrows():
		cdb.execute('INSERT INTO ingredients values(%s, "%s", "%s", "%s", %s, %s)' %
				(row['recipe_id'], row['name'], row['pron'], row['amount'],
					"null" if pd.isnull(row['converted']) else row['converted'],
					"null" if pd.isnull(row['unit'])      else '"' + str(row['unit'])  + '"'))
		if pd.isnull(row['servings']) == False:
			cdb.execute("INSERT INTO yields values(" + str(row['recipe_id']) + ',' + str(row['servings']) + ")")


def renewdb(cdb):
	# テーブルの初期化
	init_tables(cdb)
	# レコードの登録
	insert_records(cdb)

if __name__ == '__main__':
	cdb = coquadb.CoquaDB('coqua.db')
	cdb.debug_mode(True)
	renewdb(cdb)
	cdb.commit()
	cdb.close()
