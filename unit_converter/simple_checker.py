import ast
import MeCab
import pandas as pd
import re
import sys

mecab = MeCab.Tagger(
    '-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'  # NEologd
)

def simple_check(target, id_list, ingredients, yomi_list, amount, converted):
    index_list = []  # 行番号リスト
    print('行番号: レシピID: 材料 / カタカナ読み / 分量 / 換算値')

    for i, yomi_sublist in enumerate(yomi_list):
        for j, item in enumerate(yomi_sublist):
            if target in item:
                # 行番号, レシピID, 材料, カタカナ読み, 分量, 換算値 を出力
                print(f'{i:4}: {recipe_id[i]:>7}: {ingredients[i][j]} / {yomi_sublist[j]} / {amount[i][j]} / {converted[i][j]}')
                
                index_list.append(i)  # 部分一致したら行番号を追加

    print('検索結果 ' + str(len(index_list)) + ' 件 ')  # 確認用


if __name__ == '__main__':
    args = sys.argv

    data_path = '../preprocessed/converted_ingredient.csv'
    # Searching term
    target = mecab.parse(args[1]).replace('\n', '')

    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',  # レシピID
            'ingredients',  # 材料
            'ingredients_yomi',  # カタカナ読み
            'amount',  # 分量
            'converted',  # 換算値
        ],
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    ingredients = [ast.literal_eval(column) for column in df.ingredients]
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]
    amount = [ast.literal_eval(column) for column in df.amount]
    converted = [ast.literal_eval(column) for column in df.converted]

    # 簡易確認
    simple_check(target, recipe_id, ingredients, yomi_list, amount, converted)
