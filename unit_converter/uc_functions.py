import re
import sys

# 数値と比率から新単位での値を計算
def calc(matchobj, ratio):
    return str(round(float(matchobj.group(1))*ratio, 4))  # 4桁に丸める

# 特定の分量を単位換算
def unit_conversion(yomi, table, amount):
    if not isinstance(amount, str):
        print('  注: ' + str(amount) + str(type(amount)) + ' からは単位が得られません. ')
        return '不可'
    for row in table:
        # 単位換算テーブルの 1行は ['[個こコつヶケ]', 1] のような
        # 単位の正規表現パターンと換算比率の組とする
        
        matchobj = re.search('(\d+(\.\d+)?)'+row[0], amount)
        if matchobj: return calc(matchobj, row[1])+yomi  # 「1.0タマゴ」など
    return '不明';
