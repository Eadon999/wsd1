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
		return self.__cur.fetchall()

	def table_list(self):
		self.execute("select name from sqlite_master where type='table';")
		return self.fetchAll()

	def ingredients_search(self, Alst, Nlst, sortrule, checklst):
		# Alst,Nlstのカナ化
		Alst = map(lambda x : self.__mecab.parse(x).strip(), Alst)
		Nlst = map(lambda x : self.__mecab.parse(x).strip(), Nlst)
		# NOT AND 検索 
		if Alst != []:
			tmp = '\nintersect\n'.join(
					map(lambda x : F'select distinct recipe_id from ingredients where pron = "{x}"', Alst))
			if Nlst != []:
				tmp += ''.join(
						map(lambda x : F'\nexcept\nselect distinct recipe_id from ingredients where pron = "{x}"', Nlst))
			# filter
			if checklst != []:
				checklst = list(map(lambda x : F" pref{x} = 1 ", checklst)) 
				tmp += "\nintersect\n"
				tmp += "select ingredients.recipe_id\n"
				tmp += "from ingredients join preferable_bits\n"
				tmp += "on ingredients.recipe_id = preferable_bits.recipe_id\n"
				tmp += "where" + " and ".join(checklst)
			# ソート規則ごとに文を変更
			if sortrule == 'time':
				sent = "select names.recipe_id, names.name, images.url\n"\
				       "from names join images join cooktimes\n"\
				       "on names.recipe_id = images.recipe_id and names.recipe_id = cooktimes.recipe_id\n"\
				       "where names.recipe_id\n"\
				       F"in ({tmp})\n"\
				       "order by cooktimes.cooktime"
			elif sortrule == 'date':
				sent = "select names.recipe_id, names.name, images.url\n"\
				       "from names join images join publications\n"\
				       "on names.recipe_id = images.recipe_id and names.recipe_id = publications.recipe_id\n"\
				       "where names.recipe_id\n"\
				       F"in ({tmp})\n"\
				       "order by publications.count desc"
			else:
				sent = "select names.recipe_id, names.name, images.url\n"\
				       "from names join images\n"\
				       "on names.recipe_id = images.recipe_id\n"\
				       "where names.recipe_id\n"\
				       F"in ({tmp})"
			# 実行
			self.execute(sent)
			self.last = sent # debug用
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
	cdb.ingredients_search(['玉葱'],[])
	cdb.ingredients_search(['玉葱', '人参'],[])
	cdb.ingredients_search(['玉葱', '人参', '醤油'],[])
	cdb.ingredients_search(['玉葱', '人参', '醤油'],['塩'])
	cdb.ingredients_search(['玉葱', '人参', '醤油'],['塩', '砂糖'])



