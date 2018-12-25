import sys

import pandas as pd

from filter_recipeIngredient import get_ingredient_amount_list
from filter_recipeYield import get_yield_list
from filter_readings import get_readings_array
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
        # nrows=1,  # 行数
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    ingredients, amount = get_ingredient_amount_list(df.recipeIngredient)
    readings = get_readings_array(ingredients)
    amount = get_single_amount_list(amount)

    for index_list, ingredient_list in enumerate(ingredients):
        for index_item, ingredient in enumerate(ingredient_list):
            if index_list == 0 and index_item == 0:
                df = pd.DataFrame({
                    'recipe_id': recipe_id[index_list],
                    'ingredient': ingredient,
                    'readings': readings[index_list][index_item],
                    'amount': amount[index_list][index_item],
                }, index=[0])
            else:
                df = df.append({
                    'recipe_id': recipe_id[index_list],
                    'ingredient': ingredient,
                    'readings': readings[index_list][index_item],
                    'amount': amount[index_list][index_item],
                }, ignore_index=True)
        print(f'{index_list} Done!')
    df.to_csv('./preprocessed/db_ingredients.csv')
