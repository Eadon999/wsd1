import pandas as pd
import math
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

JP_NUMBER = [
    '０',
    '一',
    '二',
    '三',
    '四',
    '五',
    '六',
    '七',
    '八',
    '九',
]


def normalize(y):
    if pd.isnull(y):
        return y  # 欠損値
    return ud.normalize('NFKC', y)  # 全角数字を半角数字へ
    # ((要修正: 漢数字は非対応, 欠損値になってしまう))

# 何人分のためのレシピであるかを得る関数


def getYield(sr):
    items = sr.values.tolist()
    result = []
    for item in items:
        if not isinstance(item, float):
            item = kanji_numbers(item)
        result.append(item)

    sr = pd.Series(result)
    sr = sr.map(normalize)
    return sr.str.extract('(?P<yield>\d+)人', expand=False)


def kanji_numbers(string):
    # nanを無視する
    result = ''
    for word in string:
        if word in JP_NUMBER:
            for index, num in enumerate(JP_NUMBER):
                if num == word:
                    result += EN_NUMBER[index]
        else:
            result += word

    return result
