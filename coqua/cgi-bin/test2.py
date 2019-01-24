import coquadb
import coquasql as CQL
import time

# CoquaDB Object
cdb = coquadb.CoquaDB('coqua.db')
start = time.time()
query = CQL.decode_query(
		CQL.sort_ids(
			CQL.filter_ids(
				[1,2],
				CQL.ingredients_ids3(['ショウユ', 'サトウ', 'ミソ'], ['トウフ', 'ハクサイ', 'ネギ'])),
		'cooktimes',
		'cooktime',
		'asc'))
cdb.execute(query)
t = time.time() - start
print(query)
print(str(round(t,5)) + '(' + str(len(cdb.fetchAll())) + ')')

