"""
ユーザーの指定した材料が含まれるレシピのurlを返すプログラム
ユーザーインプットは1つの材料のみである
"""

import sys

import pandas as pd
import ast

from modules.search_engine import SearchEngine


search_engine = SearchEngine()


if __name__ == '__main__':
    args = sys.argv

    data_path = args[1]
    target = search_engine.get_target_readings(args[2])

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

    ids = search_engine.get_url(yomi_list, recipe_id, target)
    print(ids)
