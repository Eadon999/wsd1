import uc_functions as fn
import uc_io as io
import uc_tables as tb

recipe_id, ingredients, yomi_list, amount, servings = io.data_in()  # 入

# 換算値リスト
# すべての要素が空列で埋められた, 分量リストと同じ長さの配列として初期化
converted = [['' for i in lst] for lst in amount]

for row in tb.t_uct:
    # 単位換算テーブルの表の 1行は ['タマゴ', t_tamago, 'ウズラ'] のような
    # カタカナ読みと対応する単位換算テーブルと例外の配列とする

    index_list = []  # 行番号リスト
    for i, yomi_sublist in enumerate(yomi_list):
        for j, item in enumerate(yomi_sublist):
            if row[0] in item:
                if row[2] in item:
                    converted[i][j] = '不適'  # 例外
                    continue
                converted[i][j] = fn.unit_conversion(row[0], row[1], amount[i][j])

                # 行番号, レシピID, 材料, カタカナ読み, 分量, 換算値 を出力
                print(f'{i:4}: {recipe_id[i]:>7}: {ingredients[i][j]} / {yomi_sublist[j]} / {amount[i][j]} / {converted[i][j]}')

                index_list.append(i)  # 部分一致したら行番号を追加

    print('検索結果 ' + str(len(index_list)) + ' 件 ')  # 確認用

io.data_out(recipe_id, ingredients, yomi_list, amount, converted, servings)  # 出
