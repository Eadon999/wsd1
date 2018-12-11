import charFilters as cf
import pandas as pd
import re
import sys

pt3 = '\[\[|\, \[|\]\]'  # 組の配列の書式

# 組の書式の文字列から組へ変換する関数
def toPair(i):
    return [j.strip('\'') for j in i.split(', ')]

# 組の配列の書式の文字列からなる
# ある1列のすべての要素に対して
# 文字列の組の配列への変換をおこなう関数
def toPairListFilter(sr):
    sr = cf.regexFilter(pt3, '', sr).str.split('\]')
    return [[toPair(i) for i in lst] for lst in sr]

# 組の指定した要素に対して
# 正規表現による置換をおこなう関数
def regexPairFilter(pattern, repl, j, pair):
    pair[j] = re.sub(pattern, repl, pair[j])
    return pair

# 文字列の組の配列からなる
# ある1列のすべての指定した組の要素に対して
# 正規表現による置換をおこなう関数
def regexPairListFilter(pattern, repl, j, sr):  # j は 0 または 1
    return [[regexPairFilter(pattern, repl, j, pair) for pair in lst] for lst in sr]

# 材料と分量の組のリストを得る関数
def getIngredientPairList(sr):
    cf.printList(sr)  # 組の配列の書式の文字列
    print(type(sr[0]))  # 型

    sr = toPairListFilter(sr)
    cf.printList(sr)  # 文字列の組の配列
    print(type(sr[0]))

    sr = regexPairListFilter(cf.pt2, '', 0, sr)
    cf.printList(sr)  # 記号除去済みの材料と分量の組のリスト
    print(type(sr[0]))
    return sr
