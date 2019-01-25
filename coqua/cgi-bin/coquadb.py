import sqlite3
#import coquasql as CQL
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
		self.execute("SELECT name\n  FROM sqlite_master\n WHERE type='table'")
		return self.fetchAll()

	def drop(self, tablename):
		self.execute(F'DROP TABLE IF EXISTS {tablename}')

	def ingredients_search(self, Alst, Nlst, sortrule, checklst, limit, offset):
		# Alst,Nlstのカナ化
		kana = lambda x : self.mecab.parse(x).strip()
		Alst = list(map(kana, Alst))
		Nlst = list(map(kana, Nlst))
		# ソート規則
		ruledict = {'repo': {'col':'repo',    'order':'asc'},
		            'time': {'col':'cooktime','order':'asc'},
		            'date': {'col':'count',   'order':'desc'}}
		# 材料検索クエリの生成
		Qlst = []
		if Alst != []:
			Qlst += CQL.ingredients_ids(Alst, Nlst)
		if checklst != []:
			if Qlst != []:
				Qlst = CQL.filter_ids(checklst, Qlst)
			else:
				Qlst = CQL.filter_bits(checklst)
		# 検索件数
		self.execute(CQL.count_query(Qlst))
		count = self.fetch()[0]
		# ソートと表示件数しぼりこみのクエリ生成
		if sortrule in ruledict:
			rules = ruledict[sortrule]
			query = CQL.recipe_query(Qlst, rules['col'], rules['order'], limit, offset)
		else:
			return 0, []
		# 検索の実行と結果
		if query != None:
			self.execute(query)
			self.last = query # debug用
			data = self.fetchAll()
			return count, data
		else:
			self.last = ""
			return 0, []

	def name(self, num):
		self.execute("select name from names where recipe_id = " + str(num) + ";")
		return self.fetchAll()

# SQL文を生成する
class CQL:
	# リストで渡されたSQLクエリを文字列にする（整形が目的）
	def decode_query(querylst):
		if querylst in [None, []]:
			return None
		return '\n'.join(querylst)

	# リストで渡されたSQLクエリにインデントをしたあと最初と最後に文字列を付加
	def indent_query(querylst, first, last):
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

	# フィルターを通るrecipe_idのリストを要求するクエリ
	def filter_bits(checklst):
		if checklst == []:
			return None
		lst = [ 'SELECT recipe_id',
		        '  FROM filter_bits',
		       F' WHERE bit{checklst[0]} = 1']
		for i in checklst[1:]:
			# 2つ目以降のフィルタの条件を付加していく
			lst.append(F'   AND bit{i} = 1')
		return lst

	# NOT検索のSQLクエリを生成
	# NOTリストをORでつないで得られた結果を除外する
	def notlst_ids(Nlst):
		if Nlst == []:
			return None
		lst =  [    'SELECT recipe_id',
		            '  FROM ingredients',
		           F' WHERE pron = "{Nlst[0]}"']
		for i in Nlst[1:]:
			lst += [F'    OR pron = "{i}"']
		return lst

	# AND検索のSQLクエリを生成
	# ANDリストを再帰的に読んでいき，絞り込んでいく
	# こうすることでINTERSECTよりも高速に実行できる
	def andlst_ids(Alst):
		lst =     [ 'SELECT recipe_id']
		lst +=    [ '  FROM ingredients']
		lst +=    [F' WHERE pron = "{Alst[0]}"']
		if Alst[1:] != []:
			lst += [ '   AND recipe_id IN']
			lst += CQL.indent_query(CQL.andlst_ids(Alst[1:]), '       (',')')
		return lst

	# ANDとNOTのリストから材料名検索
	def ingredients_ids(Alst, Nlst):
		if Alst == []:
			return None
		lst = CQL.andlst_ids(Alst)
		if Nlst != []:
			lst.extend(['','EXCEPT',''] + notlst_ids(Nlst))
		return lst

	# 材料名クエリに絞り込みのクエリを追加
	# Qlst:材料名クエリ Plst:フィルタークエリ
	def filter_ids(checklst, Qlst):
		if Qlst == None:
			return None
		if checklst != []:
			Plst = CQL.filter_bits(checklst)
			if Plst != []:
				Qlst = Plst + ['','INTERSECT',''] + Qlst
		return Qlst

	# ソートして表示件数分だけ取得
	def recipe_query(Qlst, col, order, limit, offset):
		if Qlst in [[], None]:
			return None
		lst = [     'SELECT DISTINCT',
		            '       recipe_id,',
		            '       name,',
		            '       image',
		            '  FROM infos']
		lst +=    [ ' WHERE recipe_id IN']
		lst +=  CQL.indent_query(Qlst, '       (', ')')
		lst +=    [F' ORDER BY {col}' + (' DESC' if offset == 'desc' else '')]
		lst +=    [F' LIMIT {limit}']
		lst +=    [F'OFFSET {offset}']
		return CQL.decode_query(lst)
	
	# クエリリストの件数を返す
	def count_query(Qlst):
		if Qlst in [[], None]:
			return 0
		lst = [     'SELECT DISTINCT',
		            '       COUNT(recipe_id)',
		            '  FROM infos']
		lst +=    [ ' WHERE recipe_id IN']
		lst +=  CQL.indent_query(Qlst, '       (', ')')
		return CQL.decode_query(lst)
