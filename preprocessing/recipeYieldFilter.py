import pandas as pd
import unicodedata as ud

EN_NUMBER = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
]


def normalize(y):
    if pd.isnull(y):
        return y  # 欠損値
    return ud.normalize('NFKC', y)  # 全角数字を半角数字へ
    # ((要修正: 漢数字は非対応, 欠損値になってしまう))

# 何人分のためのレシピであるかを得る関数


def getYield(sr):
    for item in sr:
        print(item)
    sr = sr.map(normalize)
    return sr.str.extract('(?P<yield>\d+)人', expand=False)


def kanji_numbers(nums):
