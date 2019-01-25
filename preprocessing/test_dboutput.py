import sys

import pandas as pd
import ast


from modules.formatter import FormatModules
from filter_recipeIngredient import get_ingredient_amount_list
from filter_recipeYield import get_yield_list
from filter_readings import get_readings_array
from filter_amount import get_single_amount_list


formatter = FormatModules()
pd.set_option("display.max_colwidth", 100)  # 列ごとの最大表示幅設定

if __name__ == '__main__':
    args = sys.argv
    data_path = args[1]

    # Read 'recipeIngredient' as str
    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',
            'ingredients',  # 材料
            'ingredients_yomi',  # 材料
            'amount',
            'converted',
            'new_unit',
            'servings',
            # 'recipeYield',
            # 'rankings',
        ],
        # nrows=2,  # 行数
        dtype=str,
    )

    # print(df)
    recipe_id = df.recipe_id.values.tolist()
    ingredients = [ast.literal_eval(column) for column in df.ingredients]
    ingredients_yomi = [ast.literal_eval(column)
                        for column in df.ingredients_yomi]
    amount = [ast.literal_eval(column) for column in df.amount]
    converted = [ast.literal_eval(column) for column in df.converted]
    new_unit = [ast.literal_eval(column) for column in df.new_unit]
    servings = df.servings.values.tolist()

    for index_list, ingredient_list in enumerate(ingredients):
        for index_item, ingredient in enumerate(ingredient_list):
            if index_list == 0 and index_item == 0:
                df = pd.DataFrame({
                    'recipe_id': recipe_id[index_list],
                    'name': ingredient,
                    'pron': ingredients_yomi[index_list][index_item],
                    'amount': amount[index_list][index_item],
                    'converted': converted[index_list][index_item],
                    'unit': new_unit[index_list][index_item],
                    'servings': servings[index_list],
                }, index=[0])
                print('Done')
            else:
                df = df.append({
                    'recipe_id': recipe_id[index_list],
                    'name': ingredient,
                    'pron': ingredients_yomi[index_list][index_item],
                    'amount': amount[index_list][index_item],
                    'converted': converted[index_list][index_item],
                    'unit': new_unit[index_list][index_item],
                    'servings': servings[index_list],
                }, ignore_index=True)
        print(f'{index_list} Done!')
    df.to_csv('./preprocessed/db_ingredients.csv')
