import pandas as pd
import re
import sys

pt0 = '\[\'|\, \'|[ ]+\'\, \'|\'\]'  # 書式

# 開き括弧以降, 空白以降, 「または」以降
pt1 = '（.*|\(.*| .*|または.*|又は.*|or.*'

# 記号 (かな, カナ, アルファベット, 数字, 漢字以外)
pt2 = '[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９]+|u3000'

# 文字列からなる
# ある1列 (pandas.Series) のすべての要素に対して
# 正規表現による置換をおこなう関数


def regexFilter(pattern, repl, sr):
    return sr.replace(pattern, repl, regex=True)

# 配列書式の文字列からなる
# ある1列のすべての要素に対して
# 文字列の配列への変換をおこなう関数


def toListFilter(sr):
    return regexFilter(pt0, '', sr).str.split('\'')

# 文字列の配列からなる
# ある1列のすべての配列の要素に対して
# 正規表現による置換をおこなう関数


def regexListFilter(pattern, repl, sr):
    return [[re.sub(pattern, repl, i) for i in lst] for lst in sr]

# 文字列の配列からなる
# ある1列のすべての配列の要素に対して
# 出力をおこなう関数


def printList(sr):
    print()
    [print(lst) for lst in sr]

# 材料リストを得る関数


def getIngredientList(sr):
    printList(sr)  # 配列書式の文字列
    print(type(sr[0]))  # 型

    sr = toListFilter(sr)
    printList(sr)  # 文字列の配列
    print(type(sr[0]))

    sr = regexListFilter(pt1, '', sr)
    printList(sr)  # 分量無し材料リスト
    print(type(sr[0]))

    sr = regexListFilter(pt2, '', sr)
    printList(sr)  # 記号除去済み分量無し材料リスト
    print(type(sr[0]))
    return sr
