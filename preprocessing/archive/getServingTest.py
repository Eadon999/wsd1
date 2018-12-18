# テスト実行例
import pandas as pd
import servingFilters as sf
import sys

args = sys.argv
path = args[1]

df = pd.read_csv(
    path,
    usecols=[
        'recipeYield',  # 何人分
        'recipeIngredient',  # 材料
    ],
    nrows=10,  # 行数
)
# print(df)

df = sf.servingFilter(df)
# cf.printList(df.recipeIngredient)

# CSV ファイルとして出力
# df.recipeIngredient.to_csv("output_0.csv")
