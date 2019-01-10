import ast
import pandas as pd
import re
import sys

# 数値と比率から新単位での値を計算
def calc(matchobj, ratio):
    return str(round(float(matchobj.group(1))*ratio, 4))  # 4桁に丸める

# 特定の分量を単位換算
def unit_conversion(yomi, table, amount):
    if not isinstance(amount, str):
        print('  注: ' + str(amount) + str(type(amount)) + ' からは単位が得られません. ')
        return '不可'
    for row in table:
        # 単位換算テーブルの 1行は ['[個こコつヶケ]', 1] のような
        # 単位の正規表現パターンと換算比率の組とする
        
        matchobj = re.search('(\d+(\.\d+)?)'+row[0], amount)
        if matchobj: return calc(matchobj, row[1])+yomi  # 「1.0タマゴ」など
    return '不明';

if __name__ == '__main__':
    data_path = '../preprocessed/filtered_ingredient.csv'

    df = pd.read_csv(
        data_path,
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

    # 換算値リスト
    # すべての要素が空列で埋められた, 分量リストと同じ長さの配列として初期化
    converted = [['' for i in lst] for lst in amount]

    # タマゴ
    t_tamago = [
        ['[個こコつヶケ]', 1], 
    ]

    # Table of Unit Conversion Table / 単位換算テーブルの表
    t_uct = [
        ['タマゴ', t_tamago, 'ウズラ'], 
    ]

    for row in t_uct:
        # 単位換算テーブルの表の 1行は ['タマゴ', t_tamago, 'ウズラ'] のような
        # カタカナ読みと対応する単位換算テーブルと例外の配列とする

        index_list = []  # 行番号リスト
        for i, yomi_sublist in enumerate(yomi_list):
            for j, item in enumerate(yomi_sublist):
                if row[0] in item:
                    if row[2] in item:
                        converted[i][j] = '不適'  # 例外
                        continue
                    converted[i][j] = unit_conversion(row[0], row[1], amount[i][j])

                    # 行番号, レシピID, 材料, カタカナ読み, 分量, 換算値 を出力
                    print(f'{i:4}: {recipe_id[i]:>7}: {ingredients[i][j]} / {yomi_sublist[j]} / {amount[i][j]} / {converted[i][j]}')

                    index_list.append(i)  # 部分一致したら行番号を追加

        print('検索結果 ' + str(len(index_list)) + ' 件 ')  # 確認用

    df = pd.DataFrame(
        list(zip(*[
            recipe_id, 
            ingredients, 
            yomi_list, 
            amount, 
            converted, 
            servings, 
        ])),
        columns=[
            'recipe_id',  # レシピID
            'ingredients',  # 材料
            'ingredients_yomi',  # カタカナ読み
            'amount',  # 分量
            'converted',  # 換算値
            'servings',  # 何人分
        ])

    df.to_csv('../preprocessed/converted_ingredient.csv')
