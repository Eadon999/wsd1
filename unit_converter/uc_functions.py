import re
import sys

# 配列の要素のいずれかが部分一致するか調べる関数
def match(lst, string):
    for i in lst:
        if i in string: return True  # 少なくとも 1つは部分一致する
    return False  # 1つも部分一致しない

# 数値と比率から新単位での値を計算
def calc(matchobj, ratio):
    return str(round(float(matchobj.group(1))*ratio, 4))  # 4桁に丸める

# 特定の分量を単位換算
def unit_conversion(yomi, table, amount):
    if not isinstance(amount, str):
        print('  注: ' + str(amount) + str(type(amount)) + ' からは単位が得られません. ')
        # return 'NaN', '不可'  # 換算不可
        return str(amount), '小さじ'  # 要検証: 換算不可のものはすべて小さじに換算済み??
    if 'さじ' in amount or '匙' in amount:
        return 'NaN', '不可'  # 換算不可
    for row in table:
        # 単位換算テーブルの 1行は ['[個こコつヶケ]', 1] のような
        # 単位の正規表現パターンと換算比率の組とする
        
        # 半角コンマ「,」や全角中黒「・」は半角ピリオド「.」として読む
        matchobj = re.search('(\d+(\.\d+)?)'+row[0], re.sub('[,・]', '.', amount))
        if matchobj: return calc(matchobj, row[1]), yomi  # 換算値と新単位
    return 'NaN', '不明'  # 単位不明
