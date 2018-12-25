# テスト実行例
import sys

import pandas as pd

from modules.formatter import FormatModules

pd.set_option('display.max_rows', 5000)  # 最大表示行数設定

args = sys.argv
path = args[1]

formatter = FormatModules()

if __name__ == '__main__':

    df = pd.read_csv(
        path,
        usecols=[
            'recipeYield',  # 何人分
        ],
        # nrows=100,  # 行数
        nrows=10,
    )

    recipe_yield = formatter.convert_series_list(df.recipeYield)
    # recipe_yield = [
        # item for item in recipe_yield if not isinstance(item, float)]
    sr = pd.Series(recipe_yield)
    sr = sr.map(formatter.normalize)
    
    # 何人分かの数字を漢数字から英数字に変換
    for i in sr.index:
        if not isinstance(sr[i], float):  # 欠損値でなければ
            sr[i] = formatter.kanji_numbers(sr[i])
    
    recipe_yield = sr.str.extract('(?P<yield>\d+)人', expand=False)
    print(recipe_yield)
