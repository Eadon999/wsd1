import ast
import MeCab
import pandas as pd
import re
import sys

mecab = MeCab.Tagger(
    '-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd'  # NEologd
)

def get_unit(unit_set, amount):
    l = len(amount)
    for match in re.finditer('(\d+(\.\d+)?)', amount):  # 小数が見つかれば
        i = match.end()
        if i < l:
            unit_set.add(amount[i])  # 直後の1文字を単位候補集合に追加
    return unit_set

def simple_search(target, id_list, ingredients, yomi_list, amount):
    index_list = []  # 行番号リスト
    unit_set = set([])  # 単位候補集合
    print('行番号: レシピID: 材料 / カタカナ読み / 分量')

    for i, yomi_sublist in enumerate(yomi_list):
        for j, item in enumerate(yomi_sublist):
            if target in item:
                # レシピID, 材料, カタカナ読み, 分量 を出力
                print(f'{i:4}: {id_list[i]:>7}: {ingredients[i][j]} / {yomi_sublist[j]} / {amount[i][j]}')
                
                index_list.append(i)  # 部分一致したら行番号を追加
                unit_set = get_unit(unit_set, amount[i][j])  # 単位候補集合を更新

    print('検索結果 ' + str(len(index_list)) + ' 件 ')  # 確認用
    
    unit_set = unit_set - set(['(', '（', '-', 'ー', '~', '〜'])  # 単位候補から除去
    print('単位候補集合 ' + str(unit_set))


if __name__ == '__main__':
    args = sys.argv

    data_path = '../preprocessed/filtered_ingredient.csv'
    # Searching term
    target = mecab.parse(args[1]).replace('\n', '')

    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',  # レシピID
            'ingredients',  # 材料
            'ingredients_yomi',  # カタカナ読み
            'amount',  # 分量
        ],
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    ingredients = [ast.literal_eval(column) for column in df.ingredients]
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]
    amount = [ast.literal_eval(column) for column in df.amount]

    # 簡易検索
    simple_search(target, recipe_id, ingredients, yomi_list, amount)
