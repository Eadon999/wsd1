# [調査] 漢数字を検索するだけの
import pandas as pd
import recipeYieldFilter as ryf
import sys

pd.set_option("display.max_colwidth", 130)  # 列ごとの最大表示幅設定

# ある1列 (pandas.Series) 内で
# 単語リスト中の単語を順に検索して
# それぞれの単語を含む要素を出力する関数
def searchAndPrintElem(wordList, sr):
    print('\npandas.Series の「' + sr.name + '」列内で')
    for word in wordList:
        print('\n「' + word + '」を検索. ')
        print(sr[sr.str.contains(word, na=False)])

if __name__ == '__main__':
    args = sys.argv
    path = args[1]
    
    df = pd.read_csv(
        path,
        usecols=[
            'ingredients',  # 材料
            'amount',  # 分量
        ],
        # nrows = 10,  # 行数
    )
    # print(df)
    
    # 「分量」データ列内で漢数字を検索して要素を出力
    searchAndPrintElem(ryf.JP_NUMBER, df.amount)
    
    # 「材料」データ列内で漢数字を検索して要素を出力
    searchAndPrintElem(ryf.JP_NUMBER, df.ingredients)
