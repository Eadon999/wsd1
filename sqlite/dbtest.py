import sys
import sqlite3

args = sys.argv
name = args[1]
dbconn = sqlite3.connect('db.db')
dbcur  = dbconn.cursor()
dbcur.execute("select recipe_id from ingredients where name = '" + name + "';")
ids = dbcur.fetchall()
print([item[0] for item in ids])
