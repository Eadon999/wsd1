import coquadb
import coquasql as CQL
import time

# CoquaDB Object
cdb = coquadb.CoquaDB('coqua.db')
# テーブルのリストを表示
# cdb.table_list()
# デバックモードを入に
# cdb.debug_mode(True)
lst = []
# ids > ids2 > ids3 と実行時間が短くなる
lst.append(lambda:CQL.sort_ids(CQL.ingredients_ids(['ダイコン','ニンジン'],['ショウユ', 'ミソ']), 'cooktimes', 'cooktime', 'asc'))
lst.append(lambda:CQL.sort_ids(CQL.ingredients_ids2(['ダイコン','ニンジン'],['ショウユ', 'ミソ']), 'cooktimes', 'cooktime', 'asc'))
lst.append(lambda:CQL.sort_ids(CQL.ingredients_ids3(['ダイコン','ニンジン'],['ショウユ', 'ミソ']), 'cooktimes', 'cooktime', 'asc'))
lst.append(lambda:CQL.ingredients_ids3(['トウフ','ショウユ','ミソ'],['ダイコン']))
lst.append(lambda:CQL.ingredients_ids2(['トウフ','ショウユ','ミソ'],['ダイコン']))
lst.append(lambda:CQL.ingredients_ids(['トウフ','ショウユ','ミソ'],['ダイコン']))
lst.append(lambda:CQL.pref_bits([1]))
for i in lst:
	start = time.time()
	cdb.execute(CQL.decode_query(i()))
	t = time.time() - start
	print(str(round(t,5)) + '(' + str(len(cdb.fetchAll())) + ')')

