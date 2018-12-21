# テスト実行例
import sys

import pandas as pd

from modules.regex import RegexModules
from modules.formatter import FormatModules

pat_symbols = '[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９()（）\w~〜]+|u3000'
pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定
args = sys.argv
path = args[1]
regex = RegexModules()
formatter = FormatModules()


if __name__ == '__main__':

    df = pd.read_csv(
        path,
        usecols=[
            'recipeIngredient',  # 材料
        ],
        nrows=2,  # 行数
    )

    print('Converting to list...')
    ingredients = formatter.convert_str_list(df.recipeIngredient)
    print(ingredients)

    print('\nRemoving symbols...')
    ingredients = regex.replace_pat_in_array(pat_symbols, '', ingredients)
    print(ingredients)
