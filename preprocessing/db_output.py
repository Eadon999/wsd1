import ast
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv(
        '../preprocessed/converted_ingredient.csv',
        usecols=[
            'recipe_id',         # レシピID
            'ingredients',       # 材料
            'ingredients_yomi',  # カタカナ読み
            'amount',            # 分量
            'converted',         # 換算値
            'new_unit',          # 新単位
            'servings',          # 何人分
        ], 
        dtype=str, 
    )

    recipe_id   = df.recipe_id.values.tolist()
    ingredients = [ast.literal_eval(column) for column in df.ingredients]
    yomi_list   = [ast.literal_eval(column) for column in df.ingredients_yomi]
    amount      = [ast.literal_eval(column) for column in df.amount]
    converted   = [ast.literal_eval(column) for column in df.converted]
    new_unit    = [ast.literal_eval(column) for column in df.new_unit]
    servings    = df.servings.values.tolist()

    path = '../preprocessed/db_ingredients_2.csv'
    with open(path, 'w') as f:  # 書き込み専用
        f.write(',recipe_id,name,pron,amount,converted,unit,servings')

    with open(path, 'a') as f:  # 追記用
        n=0
        for i in range(len(recipe_id)):
            for j in range(len(ingredients[i])):
                f.write(F'\n{n},{recipe_id[i]},{ingredients[i][j]},{yomi_list[i][j]},{amount[i][j]},{converted[i][j]},{new_unit[i][j]},')
                if pd.notnull(servings[i]):  # 欠損値でないならば
                    f.write(F'{servings[i]}')
                print(F'{n} Done!')
                n+=1
