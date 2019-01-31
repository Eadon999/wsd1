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
			self.mecab = MeCab.Tagger('-Oyomi -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
		elif(os.path.exists('/usr/local/lib/mecab/dic/mecab-ipadic-neologd')):
			self.mecab = MeCab.Tagger('-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
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

	def fetch(self):
		return self.__cur.fetchone()

	def fetchAll(self):
		return self.__cur.fetchall()

	def table_list(self):
		self.execute("SELECT name FROM sqlite_master WHERE type='table'")
		return self.fetchAll()

	def drop(self, tablename):
		self.execute(F'DROP TABLE IF EXISTS {tablename}')

	# リストで渡されたSQLクエリを文字列にする（整形が目的）
	def decode_query(self,querylst):
		if querylst in [None, []]:
			return None
		return '\n'.join(querylst)

	# リストで渡されたSQLクエリにインデントをしたあと最初と最後に文字列を付加
	def indent_query(self,querylst, first, last):
		if querylst == []:
			return []
		if len(querylst) == 1:
			lst = [first + querylst[0] + last]
		else:
			lst = [first + querylst[0]]
			ind = ' ' * len(first)
			for i in querylst[1:-1]:
				lst.append(ind + i)
			lst.append(ind + querylst[-1] + last)
		return lst

	def ingredients_search(self, Alst, Nlst, sortrule, orderrule, checklst, limit, offset):
		# Alst,Nlstのカナ化
		kana = lambda x : self.mecab.parse(x).strip()
		Alst = list(map(kana, Alst))
		Nlst = list(map(kana, Nlst))
		# ソート規則
		ruledict = {'repo': 'repo', 'time': 'cooktime', 'date': 'count'}
		# WHERE句の生成
		Qcond = self.query_cond(Alst, Nlst, checklst)
		# クエリの生成
		Qlst = ['SELECT DISTINCT',\
		        '       recipe_id,',\
		        '       name,',\
		        '       thumbnail',\
		        '  FROM infos']\
		       + Qcond +\
		       [' ORDER BY %s %s' % (ruledict[sortrule], orderrule),\
		        ' LIMIT %s'       % limit,\
		        'OFFSET %s'       % offset]
		Clst = ['SELECT DISTINCT',\
		        '       COUNT(recipe_id)',\
		        '       FROM infos']\
		        + Qcond
		# クエリの実行
		self.execute(self.decode_query(Clst))
		count = self.fetch()[0]
		query = self.decode_query(Qlst)
		self.last = query # debug用
		self.execute(query)
		data = self.fetchAll()
		return count, data

	def query_cond(self, Alst, Nlst, checklst):
		lsts = []
		### ANDlist
		for x in Alst:
			lst = ['IN',\
			      ['SELECT recipe_id',\
			       '  FROM ingredients',\
			       ' WHERE pron = "%s"' % x,\
			       '',\
			       ' UNION',\
			       '',\
			       'SELECT recipe_id',\
			       '  FROM names',\
			       ' WHERE tail like "%s%%"' % x]]
			lsts.append(lst)
		### NOTlist
		if Nlst != []:
			lst = ['NOT IN',\
			      ['SELECT recipe_id',\
			       '  FROM ingredients',\
			       ' WHERE pron = "%s"' % Nlst[0]]\
			    + ['    OR pron = "%s"' % x for x in Nlst[1:]] +\
			      ['',\
			       ' UNION',\
			       '',\
			       'SELECT recipe_id',\
			       '  FROM names',\
			       ' WHERE tail like "%s%%"' % Nlst[0]]\
			    + ['    OR tail like "%s%%"' % x for x in Nlst[1:]]]
			lsts.append(lst)
		### filter
		if checklst != []:
			lst = ['IN',\
			      ['SELECT recipe_id',\
			       '  FROM filter_bits',\
			       ' WHERE bit%s = 1' % checklst[0]]\
			    + ['   AND bit%s = 1' % x for x in checklst[1:]]]
			lsts.append(lst)
		###
		lst = []
		for i in range(len(lsts)):
			if i == 0:
				lst += self.indent_query(lsts[i][1], ' WHERE recipe_id %s (' % lsts[i][0], ')')
			else:
				lst += self.indent_query(lsts[i][1], '   AND recipe_id %s (' % lsts[i][0], ')')
		return lst


