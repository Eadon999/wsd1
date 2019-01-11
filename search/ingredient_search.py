import sys

import pandas as pd
import ast

from modules import SearchEngine, Formatter

search_engine = SearchEngine()
formatter = Formatter()

if __name__ == '__main__':
    args = sys.argv

    data_path = args[1]

    df = pd.read_csv(
        data_path,
        usecols=[
            'recipe_id',
            'ingredients_yomi',
            'amount',
        ],
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]
    amount_list = [ast.literal_eval(column) for column in df.amount]

    include = input('検索する材料名をスペース区切りで入力してください： ')
    exclude = input('検索から省く材料名をスペース区切りで入力してください： ')
    chck_amount = input('余剰材料検索を行いますか？(y / n)： ')

    # 文字列をリストに変換
    include = formatter.convert_str_to_list(include, ' ')
    exclude = formatter.convert_str_to_list(exclude, ' ')

    indexes = search_engine.get_indexes(yomi_list, recipe_id, include, exclude)
    ids = search_engine.get_ids(recipe_id, indexes)

    if chck_amount == 'y':
        pair = search_engine.get_pairing_element(
            include, ids, yomi_list, amount_list, indexes)
        print(pair)
        search_engine.get_combination_sum(2, include, pair)
    else:
        print(ids)
