import sys

import pandas as pd
import ast
import re
import MeCab

from modules.regex import RegexModules
from modules.formatter import FormatModules
from modules.utility import UtilityModules


pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定
symbol_pattern = '[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９.~～〜()（）/\w]+|u3000'
mecab = MeCab.Tagger('-Oyomi')

regex = RegexModules()
formatter = FormatModules()
utility = UtilityModules()


def parse_ingredients(lst):
    result = [[mecab.parse(item).replace('\n', '')
               for item in recipe] for recipe in lst]
    return result


def cal_functions(lst):
    # 帯分数を小数へ
    result = regex.replace_pat_in_array(
        '(\d)と(\d)\/(\d)', utility.mixedfraction_to_float, lst)

    # 分数を小数へ
    result = regex.replace_pat_in_array(
        '(\d)\/(\d)', utility.fraction_to_float, result)

    # 分数 (日本語) を小数へ
    result = regex.replace_pat_in_array(
        '(\d)分の(\d)', utility.bunsu_to_float, result)

    return result


if __name__ == '__main__':
    args = sys.argv
    data_path = args[1]

    # Read 'recipeIngredient' as str
    df = pd.read_csv(
        data_path,
        usecols=[
            'recipeIngredient',  # 材料
            'recipeYield',
            'recipe_id',
            # 'rankings',
        ],
        # nrows=10,  # 行数
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()

    # recipeIngredientを材料と量に前処理をし、分割する
    ingredients = formatter.convert_str_list(
        (df.recipeIngredient).map(formatter.normalize))
    ingredients = cal_functions(ingredients)
    ingredients = regex.replace_pat_in_array(symbol_pattern, '', ingredients)
    ingredients, amount = formatter.convert_2darray_to_lists(ingredients)
    amount = [[formatter.kanji_numbers(item)
               for item in lst] for lst in amount]

    # 人数を取得する
    servings = utility.get_yield(df.recipeYield)  # 人数の大きい方を抽出
    servings = servings.values.tolist()  # リストに変換

    # 材料の読みを取得する
    readings = parse_ingredients(ingredients)

    # For debugging
    # output = [
    #     recipe_id,
    #     ingredients,
    #     readings,
    #     amount,
    #     servings,
    # ]
    # print(output)

    df = pd.DataFrame(
        list(
            zip(
                *[
                    recipe_id,
                    ingredients,
                    readings,
                    amount,
                    servings,
                ])),
        columns=[
            'recipe_id',
            'ingredients',
            'ingredients_yomi',
            'amount',
            'serving',
        ])

    # print('Converting to csv...')
    df.to_csv('./preprocessed/filtered_ingredient.csv')
