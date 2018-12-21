import sqlite3
import functools

def search(Alst, dbcur):
	if(len(Alst) < 1):
		return []
	elif(len(Alst) == 1):
		dbcur.execute("select recipe_id from ingredients where name = '" + Alst[0] + "'")
	elif(len(Alst) > 1):
		dbcur.execute("select i1.recipe_id from "
			+ functools.reduce(
				lambda x,y : x + ', ' + y,
				["(select distinct recipe_id from ingredients where name = '" + x + "') i" + str(i)
					for i, x in zip(range(1, len(Alst) + 1), Alst)])
				+ " where "
				+ functools.reduce(
					lambda x,y : x + ' and ' + y,
					["i" + str(i) + ".recipe_id = i" + str(i+1) + ".recipe_id"
						for i in range(1, len(Alst))]))
	return [item[0] for item in dbcur.fetchall()]


if __name__ == '__main__':
	# DBとの接続
	dbname = 'coqua.db'
	dbconn = sqlite3.connect(dbname)
	dbcur  = dbconn.cursor()
	# debug用
	dbconn.set_trace_callback(print)
	# 検索
	print(search(['白菜'], dbcur))
	print(search(['大根'], dbcur))
	print(search(['白菜', '大根'], dbcur))
	# コミット
	dbconn.commit()
	# データベースを閉じる
	dbconn.close()
