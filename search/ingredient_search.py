import sys

import pandas as pd
import ast


def search_target(target, id_list, ingredients_list):
    for index, ingredients in enumerate(ingredients_list):
        if target in ingredients:
            print(id_list[index])


if __name__ == '__main__':
    args = sys.argv

    data_path = args[1]
    # Searching term
    target = args[2]

    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',
            'ingredients',
            # 'amount'
        ],
        # nrows=1,  # 行数
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    ingredients_list = [ast.literal_eval(column)
                        for column in df.ingredients]

    search_target(target, recipe_id, ingredients_list)
