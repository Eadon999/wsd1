import sys

import MeCab
import pandas as pd
import ast


args = sys.argv
data_path = args[1]
mecab = MeCab.Tagger('-Oyomi')


def parse_ingredients(lst):
    result = [[mecab.parse(item).replace('\n', '')
               for item in recipe] for recipe in lst]
    return result


if __name__ == '__main__':

    # Read 'recipeIngredient' as str
    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',
            'ingredients',
        ],
        nrows=10,  # 行数
        dtype=str,
    )

    ingredients_list = [ast.literal_eval(column)
                        for column in df.ingredients]
    print(parse_ingredients(ingredients_list))
