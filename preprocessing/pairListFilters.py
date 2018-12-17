import charFilters as cf
import pandas as pd
import re
import sys
import unicodedata as ud

# 記号 (かな, カナ, 数字, 漢字以外)
pt2a = '[^ぁ-んァ-ンー0-9一-龠０-９]+'

pt3 = '\[\[|\, \[|\]\]'  # 組の配列の書式

# 組の書式の文字列から組へ変換する関数


def toPair(i):
    return [j.strip('\'') for j in i.split(', ')]

# 組の配列の書式の文字列からなる
# ある1列のすべての要素に対して
# 文字列の組の配列への変換をおこなう関数


def toPairListFilter(sr):
    sr = cf.regexFilter('\\\\u3000|\\\\xa0', ' ', sr)  # 全角空白, 固定空白を半角空白へ置換
    sr = cf.regexFilter('\\\\uf87f', '', sr)  # グラム記号の私用領域を除去
    sr = cf.regexFilter(pt3, '', sr).str.split('\]')
    sr = [[ud.normalize('NFKC', i) for i in lst] for lst in sr]
    return [[toPair(i) for i in lst] for lst in sr]

# 組の指定した要素に対して
# 正規表現による置換をおこなう関数


def regexPairFilter(pattern, repl, j, pair):
    if len(pair) <= j:
        return pair
    pair[j] = re.sub(pattern, repl, pair[j]).strip()
    return pair

# 文字列の組の配列からなる
# ある1列のすべての指定した組の要素に対して
# 正規表現による置換をおこなう関数


def regexPairListFilter(pattern, repl, j, sr):  # j は 0 または 1
    return [[regexPairFilter(pattern, repl, j, pair) for pair in lst] for lst in sr]

# 材料と分量の組のリストを得る関数


def getIngredientPairList(sr):
    # cf.printList(sr)  # 組の配列の書式の文字列
    # print(type(sr[0]))  # 型

    sr = toPairListFilter(sr)
    # cf.printList(sr)  # 文字列の組の配列
    # print(type(sr[0]))

    sr = regexPairListFilter(pt2a, ' ', 0, sr)
    cf.printList(sr)  # 記号除去済みの材料と分量の組のリスト
    # print(type(sr[0]))

    # sr = regexPairListFilter(cf.)
    return sr
