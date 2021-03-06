import json
import glob
import sqlite3
import datetime
import pandas as pd
import ast
import os
import MeCab
import re

def init_tables(cdb): # テーブルの初期化
	# infos(レシピ情報)
	cdb.drop('infos')
	cdb.execute("CREATE TABLE infos ("
			"recipe_id INTEGER,"
			"name TEXT,"
			"author TEXT,"
			"image TEXT,"
			"thumbnail TEXT,"
			"date TEXT,"
			"year INTEGER,"
			"month INTEGER,"
			"day   INTEGER,"
			"count INTEGER,"
			"cooktime INTEGER,"
			"yield REAL,"
			"repo INTEGER,"
			"PRIMARY KEY(recipe_id))")
	cdb.execute("CREATE INDEX idx_info_recipe_id ON infos(recipe_id)")
	cdb.execute("CREATE INDEX idx_info_name      ON infos(name)")
	cdb.execute("CREATE INDEX idx_info_author    ON infos(author)")
	cdb.execute("CREATE INDEX idx_info_count     ON infos(count)")
	cdb.execute("CREATE INDEX idx_info_cooktime  ON infos(cooktime)")
	cdb.execute("CREATE INDEX idx_info_yield     ON infos(yield)")
	cdb.execute("CREATE INDEX idx_info_repo      ON infos(repo)")
	# names
	cdb.drop('names')
	cdb.execute("CREATE TABLE names (recipe_id INTEGER, tail TEXT)")
	cdb.execute("CREATE INDEX idx_name_recipe_id ON names(recipe_id)")
	cdb.execute("CREATE INDEX idx_name_tail      ON names(tail)")
	# filter_bits
	cdb.drop('filter_bits')
	filter_len = 9
	cdb.execute("CREATE TABLE filter_bits (recipe_id INTEGER,"
			+ ','.join(map(lambda x : F"bit{x} INTEGER", range(1,filter_len+1))) + ")")
	cdb.execute("CREATE INDEX idx_filter_recipe_id ON filter_bits(recipe_id)")
	for i in range(1,filter_len+1):
		cdb.execute(F"CREATE INDEX idx_filter_bit{i} ON filter_bits(bit{i})")
	# ingredients (材料名)
	cdb.drop('ingredients')
	cdb.execute("CREATE TABLE ingredients (recipe_id INTEGER, name TEXT, pron TEXT, amount TEXT, converted REAL, unit TEXT)")
	cdb.execute("CREATE INDEX idx_ingredient_recipe_id ON ingredients(recipe_id)")
	cdb.execute("CREATE INDEX idx_ingredient_name ON ingredients(name)")
	cdb.execute("CREATE INDEX idx_ingredient_pron ON ingredients(pron)")
	cdb.commit()


def insert_records(cdb):
	jlst = glob.glob("recipe0115/*")
	df_i = pd.read_csv("../preprocessed/db_ingredients_2.csv")
	df_f = pd.read_csv("filter_bit.csv")
	# filter_bits
	for i, row in df_f.iterrows():
		cdb.execute('INSERT INTO filter_bits VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
				% (row['recipe_id'], row['easy'], row['child'], row['beauty'], row['lunchbox'], row['volume'],
					row['lunch'], row['nutrition'], row['cheap'], row['snack']))
	cdb.commit()
	# ingredients(材料)
	dict_yield = {}
	for i, row in df_i.iterrows():
		cdb.execute('INSERT INTO ingredients VALUES(%s, "%s", "%s", "%s", %s, %s)' %
				(row['recipe_id'], row['name'], row['pron'], row['amount'],
					"null" if pd.isnull(row['converted']) else row['converted'],
					"null" if pd.isnull(row['unit'])      else '"' + str(row['unit'])  + '"'))
		if pd.isnull(row['servings']) == False:
			# dict_yieldはinfosのレコードに用いる
			dict_yield[str(row['recipe_id'])] = str(row['servings'])
	cdb.commit()
	# infos, names
	if(os.path.exists('/usr/lib/mecab/dic/mecab-ipadic-neologd')):
		mecab = MeCab.Tagger('-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
	elif(os.path.exists('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')):
		mecab = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
	for x in jlst:
		with open(x) as f:
			# json ファイルを１つ読んでいってそれぞれにレコードを登録
			j = json.load(f)
			rid = j['recipe_id']
			# infos
			date = datetime.datetime.strptime(j['datePublished'], '%Y-%m-%d')
			cdb.execute('INSERT INTO infos VALUES(%s, "%s", "%s", "%s", "%s", "%s", %s, %s, %s, %s, %s, %s, %s)' %
					(rid,
						str(j['name']).replace("'",'').replace('"',''),
						str(j['author']['name']).replace("'", '').replace('"', ''),
						re.sub('https://[^/]*/[^/]*/[^/]*/[^/]*/','',j['image']),
						re.sub('https://[^/]*/[^/]*/[^/]*/[^/]*/','',j['thumbnail']),
						j['datePublished'],
						str(date.year),
						str(date.month),
						str(date.day),
						str((date - datetime.datetime(2000,1,1,0,0)).days),
						j['cookTime'][2:-1] if bool(j['cookTime']) else "null",
						dict_yield[rid]     if rid in dict_yield   else "null",
						j['tsukurepo_count']))
			# names
			tmp = mecab.parse(j['name'].replace("'","").replace('"',"")).split("\n")[:-2]
			tmp = [x.split("\t") for x in tmp]
			tmp = [[x[1],x[3].split("-")[0]] for x in tmp]
			tmp = [''.join(map(lambda x:x[0], tmp[i:]))
						for i in range(len(tmp))
						if tmp[i][1] == "名詞"]
			for y in tmp:
				cdb.execute('INSERT INTO names VALUES(%s, "%s")' % (rid, y))
			
	cdb.commit()


def renewdb(cdb):
	# テーブルの初期化
	init_tables(cdb)
	# レコードの登録
	insert_records(cdb)


if __name__ == '__main__':
	cdb = __import__("cgi-bin.coquadb").coquadb.CoquaDB('coqua.db')
	cdb.debug_mode(True)
	renewdb(cdb)
	cdb.commit()
	cdb.close()
