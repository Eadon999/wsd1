import sys

import pandas as pd
import ast
import re

import charFilters as cf


pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定
symbol_pattern = '[^ぁ-んァ-ンー0-9一-龠０-９〜()\w]+|3000'


def regexListFilter(pat, repl, lst):
    # 文字列の配列からなる
    # ある1列のすべての配列の要素に対して
    # 正規表現による置換をおこなう関数

    result = [[[re.sub(pat, repl, item) for item in ingredients]
               for ingredients in recipe] for recipe in lst]
    return result


def filter_symbols(lst):
    cleaned = regexListFilter(symbol_pattern, '', lst)
    ingredients = [recipe[0] for recipe in cleaned]
    amount = [recipe[1] for recipe in cleaned]

    return ingredients, amount


if __name__ == '__main__':
    args = sys.argv
    data_path = args[1]

    # Read 'recipeIngredient' as str
    df = pd.read_csv(
        data_path,
        usecols=[
            'recipeIngredient',  # 材料
            'recipe_id',
        ],
        # nrows=1,  # 行数
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    # Conver 'recipeIngredient' into list
    ingredients_list = [ast.literal_eval(column)
                        for column in df.recipeIngredient]

    filtered_ingredient, filtered_amount = filter_symbols(ingredients_list)

    # output = [recipe_id, filtered_ingredient, filtered_amount]

    df = pd.DataFrame(
        list(
            zip(
                *[
                    recipe_id,
                    filtered_ingredient,
                    filtered_amount,
                ])),
        columns=[
            'recipe_id',
            'ingredients',
            'amount',
        ])

    df.to_csv('./preprocessed/filtered_ingredient.csv')
