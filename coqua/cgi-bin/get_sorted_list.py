import coquadb
import MeCab
import sys

# 二次元配列の行と列を入れ替える (転置) 関数
def transpose(l):
    return [list(j) for j in zip(*l)]

# 検索語のカタカナ読みを新単位とする行を
# 換算値の降順に整列した二次元配列を得る関数
def get_sorted_list(cdb, yomi):
    cdb.execute(
         'SELECT   recipe_id, converted ' 
         'FROM     ingredients ' 
        F'WHERE    unit = "{yomi}" ' 
         'ORDER BY converted DESC;'
    )
    return transpose(cdb.fetchAll())


if __name__ == '__main__':
    args = sys.argv

    cdb = coquadb.CoquaDB('coqua.db')
    
    mecab = cdb.mecab
    yomi = mecab.parse(args[1]).replace('\n', '')
    print(get_sorted_list(cdb, yomi))

    cdb.close()
