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
        ],
        dtype=str,
    )

    recipe_id = df.recipe_id.values.tolist()
    yomi_list = [ast.literal_eval(column) for column in df.ingredients_yomi]

    include = input('検索する材料名をスペース区切りで入力してください： ')
    exclude = input('検索から省く材料名をスペース区切りで入力してください： ')

    # 文字列をリストに変換
    include = formatter.convert_str_to_list(include, ' ')
    exclude = formatter.convert_str_to_list(exclude, ' ')

    result = search_engine.get_ids(yomi_list, recipe_id, include, exclude)
    print(result)
