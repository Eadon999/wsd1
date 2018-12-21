import pairListFilters as plf
import pandas as pd
import re

from modules.utility import UtilityModules

num = 0  # 何人分か

# 帯分数を小数へ


def mixedFractionToFloat(matchobj):
    i0 = int(matchobj.group(1))
    i1 = int(matchobj.group(2))
    i2 = int(matchobj.group(3))
    s0 = str(round(i0+i1/i2, 2))
    # print('mixedFractionToFloat: ' + s0)
    return s0

# 分数を小数へ


def fractionToFloat(matchobj):
    i0 = int(matchobj.group(1))
    i1 = int(matchobj.group(2))
    s0 = str(round(i0/i1, 2))
    # print('fractionToFloat: ' + s0)
    return s0

# 分数 (日本語) を小数へ


def bunsuToFloat(matchobj):
    i0 = int(matchobj.group(1))
    i1 = int(matchobj.group(2))
    s0 = str(round(i1/i0, 2))  # (「2分の1」など)
    # print('bunsuToFloat: '+str(i0)+'分の'+str(i1)+' -> '+s0)
    return s0

# 1人あたり


def div(matchobj):
    f0 = float(matchobj.group(1))
    s0 = str(round(f0/num, 2))
    # print('div (' + str(num) + '): ' + s0)
    return s0

# 材料と分量の組に対して, 何人分かから
# 1人分の材料と分量の組を得る関数


def getServingPair(pair):
    if len(pair) < 2:
        return pair
    pair[1] = re.sub('(\d+(\.\d+)?)', div, pair[1])
    return pair


def getServingPairList(sr):
    if pd.isnull(sr['yield']):
        return sr
    global num
    num = int(sr['yield'])
    sr['recipeIngredient'] = [getServingPair(
        pair) for pair in sr['recipeIngredient']]
    return sr

# 1人分の分量を得る前処理フィルタ


def servingFilter(df):
    utility = UtilityModules()
    # 材料と分量の組のリストを得る
    df.recipeIngredient = plf.getIngredientPairList(df.recipeIngredient)

    # 何人分かを得る
    df = pd.concat([df, utility.get_yield(df.recipeYield)], axis=1)

    # 帯分数を小数へ
    df.recipeIngredient = plf.regexPairListFilter(
        '(\d)と(\d)\/(\d)', mixedFractionToFloat, 1, df.recipeIngredient)

    # 分数を小数へ
    df.recipeIngredient = plf.regexPairListFilter(
        '(\d)\/(\d)', fractionToFloat, 1, df.recipeIngredient)

    # 分数 (日本語) を小数へ
    df.recipeIngredient = plf.regexPairListFilter(
        '(\d)分の(\d)', bunsuToFloat, 1, df.recipeIngredient)

    for i in df.index:
        df.iloc[i] = getServingPairList(df.iloc[i])  # 1人あたり
    return df
