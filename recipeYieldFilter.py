import pandas as pd
import re
import unicodedata as ud

def normalize(y):
    if pd.isnull(y): return y  # 欠損値
    return ud.normalize('NFKC', y)  # 全角数字を半角数字へ
    # ((要修正: 漢数字は非対応, 欠損値になってしまう))

# 何人分のためのレシピであるかを得る関数
def getYield(sr):
    sr = sr.map(normalize)
    return sr.str.extract('(?P<yield>\d+)人', expand=False)
