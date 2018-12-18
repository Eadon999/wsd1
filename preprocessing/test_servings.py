import sys

import pandas as pd

from modules.regex import RegexModules
from modules.formatter import FormatModules
from modules.utility import UtilityModules

args = sys.argv
data_path = args[1]

regex = RegexModules()
formatter = FormatModules()
utility = UtilityModules()

if __name__ == '__main__':
    df = pd.read_csv(
        data_path,
        usecols=[
            'recipeYield',  # 何人分
            'recipeIngredient',  # 材料
        ],
        nrows=10,  # 行数
    )

    ingredients = formatter.convert_str_list(
        (df.recipeIngredient).map(formatter.normalize))
    servings = utility.get_yield(df.recipeYield).values.tolist()

    # 帯分数を小数へ
    ingredients = regex.replace_pat_in_array(
        '(\d)と(\d)\/(\d)', utility.mixedfraction_to_float, ingredients)
    print(ingredients)

    # 分数を小数へ
    ingredients = regex.replace_pat_in_array(
        '(\d)\/(\d)', utility.fraction_to_float, ingredients)

    print(ingredients)

    # 分数 (日本語) を小数へ
    ingredients = regex.replace_pat_in_array(
        '(\d)分の(\d)', utility.bunsu_to_float, ingredients)
    print(ingredients)
