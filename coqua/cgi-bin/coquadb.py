import sqlite3
import coquasql as CQL
import MeCab
import os
import sys

class CoquaDB:
	def __init__(self, dbname):
		# DBオブジェクトを作成し，接続を行う
		self.__con = sqlite3.connect(dbname)
		self.__cur = self.__con.cursor()
		if(os.path.exists('/usr/lib/mecab/dic/mecab-ipadic-neologd')):
			self.__mecab = MeCab.Tagger('-Oyomi -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
		elif(os.path.exists('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')):
			self.__mecab = MeCab.Tagger('-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
		else:
			sys.exit(1)

	def debug_mode(self, x):
		# デバッグ出力のON/OFFをする
		self.__con.set_trace_callback(print if bool(x) else None)

	def commit(self):
		self.__con.commit()

	def close(self):
		self.__con.close()

	def execute(self,s):
		self.__cur.execute(s)

	def fetchAll(self):
		return self.__cur.fetchall()

	def table_list(self):
		self.execute("SELECT name\n  FROM sqlite_master\n WHERE type='table'")
		return self.fetchAll()

	def ingredients_search(self, Alst, Nlst, sortrule, checklst):
		# Alst,Nlstのカナ化
		Alst = list(map(lambda x : self.__mecab.parse(x).strip(), Alst))
		Nlst = list(map(lambda x : self.__mecab.parse(x).strip(), Nlst))
		# ソート規則
		ruledict = {'repo': ['cooktimes',    'cooktime', 'asc'],
		            'time': ['cooktimes',    'cooktime', 'asc'],
		            'date': ['publications', 'count',    'desc']}
		# 検索クエリの生成
		Qlst = []
		if Alst != []:
			Qlst += CQL.ingredients_ids3(Alst, Nlst)
		if checklst != []:
			if Qlst != []:
				Qlst = CQL.filter_ids(checklst, Qlst)
			else:
				Qlst = CQL.pref_bits(checklst)
		if sortrule in ruledict:
			rules = ruledict[sortrule]
			Qlst = CQL.sort_ids(Qlst, rules[0], rules[1], rules[2])
		else:
			Qlst = CQL.recipe_data(Qlst)
		# 検索の実行と結果
		query = CQL.decode_query(Qlst)
		if query != None:
			self.execute(query)
			self.last = query # debug用
			return self.fetchAll()
		else:
			self.last = ""
			return []

	def name(self, num):
		self.execute("select name from names where recipe_id = " + str(num) + ";")
		return self.fetchAll()

