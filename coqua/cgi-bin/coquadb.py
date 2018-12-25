import string
import functools
import sqlite3
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
			sys.exiti(1)
	def debug_mode(self, x):
		# デバッグ出力のON/OFFをする
		if(bool(x)):
			self.__con.set_trace_callback(print)
		else:
			self.__con.set_trace_callback(None)
	def commit(self):
		self.__con.commit()
	def close(self):
		self.__con.close()
	def execute(self,s):
		self.__cur.execute(s)
	def fetchAll(self):
		return [item[0] for item in self.__cur.fetchall()]
	def table_list(self):
		self.execute("select name from sqlite_master where type='table';")
		return self.fetchAll()
	def ingredients_list(self, Alst, Nlst):
		Alst = map(lambda x : self.__mecab.parse(x).strip(), Alst)
		Nlst = map(lambda x : self.__mecab.parse(x).strip(), Nlst)
		# NOT AND 検索 
		if Alst != []:
			tmp = functools.reduce(lambda x,y : x + ' intersect ' + y,
						map(lambda x : 'select distinct recipe_id from ingredients where pron = "' + x + '"', Alst))
			if Nlst != []:
				for x in Nlst:
					tmp += 'except select distinct recipe_id from ingredients where name = "' + x + '"'
			self.execute(tmp)
		return self.fetchAll()
	def name(self, num):
		self.execute("select name from names where recipe_id = " + str(num) + ";")
		return self.fetchAll()


if __name__ == '__main__':
	# CoquaDB Object
	cdb = CoquaDB('coqua.db')
	# デバックモードを入に
	cdb.debug_mode(True)
	# tableのリスト
	print(cdb.table_list())
	# 材料検索
	print(cdb.ingredients_list([],[]))
	print(cdb.ingredients_list(['玉葱'],[]))
	print(cdb.ingredients_list(['玉葱', '人参'],[]))
	print(cdb.ingredients_list(['玉葱', '人参', '醤油'],[]))
	print(cdb.ingredients_list(['玉葱', '人参', '醤油'],['塩']))
	print(cdb.ingredients_list(['玉葱', '人参', '醤油'],['塩', '砂糖']))



