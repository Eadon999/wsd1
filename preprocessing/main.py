import sys

import pandas as pd

from filter_recipeIngredient import get_ingredient_amount_list
from filter_recipeYield import get_yield_list
from filter_readings import get_readings_list
from filter_amount import get_single_amount_list


pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定

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
    ingredients, amount = get_ingredient_amount_list(df.recipeIngredient)
    servings = get_yield_list(df.recipeYield)
    readings = get_readings_list(ingredients)
    amount = get_single_amount_list(amount)

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
            'servings',
        ])

    df.to_csv('./preprocessed/filtered_ingredient.csv')
