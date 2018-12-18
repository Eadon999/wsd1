import sys

import pandas as pd
import ast
import re

import recipeYieldFilter as ryf


pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定
symbol_pattern = '[^ぁ-んァ-ンー0-9一-龠０-９〜()\w/~]+|3000'


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
            'recipeYield',
            'recipe_id',
            # 'rankings',
        ],
        nrows=10,  # 行数
        dtype=str,
    )

    print('Preprocessing...')
    # print(df.rankings)
    recipe_id = df.recipe_id.values.tolist()
    # Conver 'recipeIngredient' into list
    ingredients_list = [ast.literal_eval(column)
                        for column in (df.recipeIngredient).map(ryf.normalize)]

    filtered_ingredient, filtered_amount = filter_symbols(ingredients_list)
    filtered_number = ryf.getYield(df.recipeYield)
    filtered_number = filtered_number.values.tolist()

    # output = [recipe_id, filtered_ingredient, filtered_amount, filtered_number]

    print('Preprocess done!')
    df = pd.DataFrame(
        list(
            zip(
                *[
                    recipe_id,
                    filtered_ingredient,
                    filtered_amount,
                    filtered_number,
                ])),
        columns=[
            'recipe_id',
            'ingredients',
            'amount',
            'serving',
        ])

    print('Converting to csv...')
    df.to_csv('./preprocessed/filtered_ingredient.csv')
