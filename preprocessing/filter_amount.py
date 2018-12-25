import re


conversion_table = {
    '大さじ': 3,
    '小さじ': 1,
    '大匙': 3,
    '小匙': 1,
}


def get_single_amount_list(data):
    result = []  # 編集済み結果を格納

    for lst in data:
        filtered = []  # 編集した単語を格納
        for item in lst:
            # 分量を決める単語を抽出
            method = re.search(r'[ぁ-んァ-ン 一-龥]+', item)

            if method is not None and method.group(0) in conversion_table:
                # 単語がテーブルにあった時

                # 分量をとってくる
                amount = re.search(r'(\d+(\.\d+)?)', item)
                if amount is not None:
                    # テーブルをもとに分量を統一する
                    filtered.append(
                        conversion_table[method.group(0)] * float(amount.group(0)))
                else:
                    filtered.append(item)
            else:
                filtered.append(item)
        result.append(filtered)

    return result
