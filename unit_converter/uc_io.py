import ast
import pandas as pd

def data_in():
    df = pd.read_csv(
        '../preprocessed/filtered_ingredient.csv',
        usecols=[
            'recipe_id',  # レシピID
            'ingredients',  # 材料
            'ingredients_yomi',  # カタカナ読み
            'amount',  # 分量
            'servings',  # 何人分
        ],
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    ingredients = [ast.literal_eval(column) for column in df.ingredients]
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]
    amount = [ast.literal_eval(column) for column in df.amount]
    servings = df.servings.values.tolist()

    return recipe_id, ingredients, yomi_list, amount, servings

def data_out(recipe_id, ingredients, yomi_list, amount, converted, new_unit, servings):
    df = pd.DataFrame(
        list(zip(*[
            recipe_id, 
            ingredients, 
            yomi_list, 
            amount, 
            converted, 
            new_unit, 
            servings, 
        ])),
        columns=[
            'recipe_id',  # レシピID
            'ingredients',  # 材料
            'ingredients_yomi',  # カタカナ読み
            'amount',  # 分量
            'converted',  # 換算値
            'new_unit',  # 新単位
            'servings',  # 何人分
        ])

    df.to_csv('../preprocessed/converted_ingredient.csv')
