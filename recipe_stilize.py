import pandas as pd
import re
import sys

def toList(s):
    p0 = '\[\'|\, \'|[ ]+\'\, \'|\'\]'  # 書式
    # print('置換前: ' + s)
    s = re.sub(p0, '', s)
    # print('置換後: ' + s)
    return s.split('\'')

args = sys.argv
path = args[1]

df_raw = pd.read_csv(path)
df = df_raw.copy()

# print(df["@context"].unique())
# print(df["@type"].unique())
# 上を実行すると分かるが値が全て同じ
df = df.drop(["@context","@type"],axis=1)

#print(df.isnull().sum())
#欠損値をunknownで埋める。上で確認できる

df["recipeYield"] = df["recipeYield"].fillna("unknown")
df["cookTime"] = df["cookTime"].fillna("unknown")
df["advice"] = df["advice"].fillna("unknown")
df["rankings"] = df["rankings"].fillna("unknown")

df = df[0:5]

l = [df.recipeIngredient,df.recipeInstructions,df.rankings]
for x in l:
    for row in x:
        #print(row)  # 1行 (配列書式の文字列)
        #print(type(row))
        row = toList(row)
        #print(row)  # 1行 (配列)
        #print(type(row))
