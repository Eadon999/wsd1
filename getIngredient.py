import pandas as pd
import re
import sys

# 配列書式の文字列から配列へ変換する関数
def toList(s):
	p0 = '\[\'|\, \'|[ ]+\'\, \'|\'\]'  # 書式
	# print('置換前: ' + s)
	s = re.sub(p0, '', s)
	# print('置換後: ' + s)
	return s.split('\'')

args = sys.argv
path = args[1]

df = pd.read_csv(
	path, 
	usecols = ['recipeIngredient'],  # 材料
	# nrows = 15,  # 行数
)
# df = df.iloc[95:96]  # 特定の範囲
# print(df)
# print(df.T)  # transpose
# print(df.dtypes)  # 型

# 開き括弧以降, 空白以降, 「または」以降
reg1 = re.compile('（.*|\(.*| .*|または.*|又は.*|or.*')

# 記号 (かな, カナ, アルファベット, 数字, 漢字以外) 
reg2 = re.compile('[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９]+|u3000')

for row in df.recipeIngredient:
	# print(row)  # 1行 (配列書式の文字列)
	iList = toList(row)
	# print(iList)  # 1行 (配列)
	iList = [reg1.sub('', i) for i in iList]
	# print(iList)  # 分量無し材料リスト
	iList = [reg2.sub('', i) for i in iList]
	print(iList)  # 記号除去済み分量無し材料リスト