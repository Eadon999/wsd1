import coquadb
cdb = coquadb.CoquaDB(':memory:')
print(cdb.decode_query(cdb.query_cond(['あ','い'],['う','え'],[1,2])))
