# テスト実行例
import charFilters as cf
import pandas as pd
import re
import sys

pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定

args = sys.argv
path = args[1]

df = pd.read_csv(
	path, 
	usecols = [
		'recipeIngredient',  # 材料
	],
	nrows = 1,  # 行数
)
print(df)
print(type(df.iat[0, 0]))

df.recipeIngredient = cf.getIngredientList(df.recipeIngredient)
print(df)
print(type(df.iat[0, 0]))
