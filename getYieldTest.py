# テスト実行例
import recipeYieldFilter as ryf
import pandas as pd
import sys

pd.set_option('display.max_rows', 5000)  # 最大表示行数設定

args = sys.argv
path = args[1]

df = pd.read_csv(
    path, 
    usecols = [
        'recipeYield',  # 何人分
    ],
    nrows = 64,  # 行数
)
# print(df)
# print(type(df.iat[0, 0]))  # 型

df = pd.concat([df, ryf.getYield(df.recipeYield)], axis=1)
print(df)
print(type(df.iat[0, 0]))
print(type(df.iat[0, 1]))
