import sys

import pandas as pd
import ast
import MeCab

import list_operations as op

mecab = MeCab.Tagger('-Oyomi')


def search_target(target, id_list, yomi_list):
    index_list = []  # 行番号リスト
    
    for index, ingredients in enumerate(yomi_list):
        for item in ingredients:
            if target in item:
                print(f'{id_list[index]} : {item}')
                index_list.append(index)  # 部分一致したら行番号を追加
                
    print('\nHit: ' + str(index_list) + '\n')  # 確認用
    
    return index_list  # 検索にヒットしたレシピの行番号を返す


def print_id_and_yomi_list(index_list, id_list, yomi_list):
    index_list.sort()  # 行番号を昇順に整列
    
    print('\n検索結果 (' + str(len(index_list)) + ' 件) ')
    for i in index_list:
        print(f'{i:4}: {id_list[i]:7}: {yomi_list[i]}')  # 各行を出力
        
    return index_list  # 整列済みの行番号リストを返す


if __name__ == '__main__':
    args = sys.argv

    data_path = args[1]
    # Searching term
    target = mecab.parse(args[2]).replace('\n', '')

    # NOT 検索の入力
    # 最終的なユーザインターフェースは適当に変えてください
    # 除去したい単語の入力欄など
    print('NOT 検索: 検索結果から除外したい単語を入力してください ')
    print('(除外したい単語が無い場合は何も入力せずにenterキーを押してください). ')
    str0 = input()
    if str0:
        # 検索結果から除外したい単語
        exception = mecab.parse(str0).replace('\n', '')

    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',
            'ingredients_yomi',
        ],
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]

    # 検索したい語にヒットしたレシピの行番号
    result_t = search_target(target, recipe_id, yomi_list)
    
    if str0:
        # 検索結果から除外したい語にヒットしたレシピの行番号
        result_e = search_target(exception, recipe_id, yomi_list)
        
        # 最終結果: リストの差 (差集合から) 
        final_result = op.l_diff(result_t, result_e)
    else:
        final_result = result_t
    
    # 最終結果を出力
    print_id_and_yomi_list(final_result, recipe_id, yomi_list)
