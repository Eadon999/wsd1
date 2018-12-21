import sys

import pandas as pd
import ast
import MeCab

mecab = MeCab.Tagger('-Oyomi')


def search_target(target, id_list, yomi_list):
    for index, ingredients in enumerate(yomi_list):
        if target in ingredients:
            print(id_list[index])


if __name__ == '__main__':
    args = sys.argv

    data_path = args[1]
    # Searching term
    target = mecab.parse(args[2]).replace('\n', '')

    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',
            'ingredients',
            'ingredients_yomi',
            # 'amount'
        ],
        # nrows=1,  # 行数
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    # ingredients_list = [ast.literal_eval(column)
    #                     for column in df.ingredients]
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]

    search_target(target, recipe_id, yomi_list)
