# テスト実行例
import pairListFilters as plf
import pandas as pd
import sys

pd.set_option("display.max_colwidth", 200)  # 列ごとの最大表示幅設定

args = sys.argv
path = args[1]

df = pd.read_csv(
    path,
    usecols=[
        'recipeIngredient',  # 材料
    ],
    nrows=1,  # 行数
)
print(df)
print(type(df.iat[0, 0]))

df.recipeIngredient = plf.getIngredientPairList(df.recipeIngredient)
print(df)
print(type(df.iat[0, 0]))
