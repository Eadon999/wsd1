import pandas as pd
import re
import sys

def toList(df):
    p0 = '\[\'|\, \'|[ ]+\'\, \'|\'\]'  # 書式
    # print('置換前: ' + s)
    df.str.replace(p0, '')
    # print('置換後: ' + s)
    return df.str.split('\'')

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

# print df["cookTime".unique()
# cookTime は皆PTxxMでxx分を表しているようなのでPT,Mを消す
df["cookTime"].str.strip("PT").str.strip("M")
#authorをname,typeに分離
df_author = df["author"].str.replace("\', \'name\': \'",",").str.lstrip("{\'@type\':\ '").str.rstrip("\'}")
df_author = df_author.str.split(",",expand=True)
df_author.columns = ["author_type","author_name"]
#typeはPersonとOrganizationの２種
df = df.drop(["author"],axis=1)
df = pd.concat([df,df_author],axis=1)

df_categories = df.categories.str.lstrip("[").str.rstrip("]")
#df_categories = df_categories.str.split(",",expand=True)
#print(df_categories)
#categoryは5つまであった。カテゴリーがないのには何も入っていないのに注意
#df_categories.columns = ["category1","category2","category3","category4","category5"]
#df = df.drop(["categories"],axis=1)
#df = pd.concat([df,df_categories],axis=1)
#noneで埋める
#df["category1"] = df["category1"].fillna("none")
#df["category2"] = df["category2"].fillna("none")
#df["category3"] = df["category3"].fillna("none")
#df["category4"] = df["category4"].fillna("none")
#df["category5"] = df["category5"].fillna("none")

#df_recipeInstructions = df.recipeIngredient.str.lstrip("[").str.rstrip("]")
#df_recipeInstructions = df_recipeInstructions.str.split(",",expand=True)
#print(df_recipeInstructions)
#categoryは39まであった。カテゴリーがないのには何も入っていないのに注意
#df_categories.columns = ["category1","category2","category3","category4","category5"]
#df = df.drop(["categories"],axis=1)
#df = pd.concat([df,df_categories],axis=1)
## df["category1"] = df["category1"].fillna("none")
#df["category2"] = df["category2"].fillna("none")
#df["category3"] = df["category3"].fillna("none")
#df["category4"] = df["category4"].fillna("none")
