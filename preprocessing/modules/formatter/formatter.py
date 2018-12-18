import ast
import pandas as pd
import unicodedata as ud

EN_NUMBER = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
]

JP_NUMBER = [
    '０',
    '一',
    '二',
    '三',
    '四',
    '五',
    '六',
    '七',
    '八',
    '九',
]


class FormatModules(object):
    """
    データ整形用のクラス
    """

    def convert_str_list(self, string):
        """return list object
        リストの形をした文字列を受け取り、リストとして返す
        ex:
        '[['test', 'test'], ['test', 'test']]' --> [['test', 'test'], ['test', 'test']]
        """
        return [ast.literal_eval(item) for item in string]

    def convert_series_list(self, sr):
        """
        pandas.Series型のオブジェクトをリストとして返す
        """
        return sr.values.tolist()

    def normalize(self, y):
        """
        全角数字を半角数字に変換する関数
        """
        if pd.isnull(y):
            return y  # 欠損値
        return ud.normalize('NFKC', y)  # 全角数字を半角数字へ

    def kanji_numbers(self, string):
        """
        漢数字を英数字に変換する関数
        """
        # nanを無視する
        result = ''
        for word in string:
            if word in JP_NUMBER:
                for index, num in enumerate(JP_NUMBER):
                    if num == word:
                        result += EN_NUMBER[index]
            else:
                result += word

        return result

    def convert_2darray_to_lists(self, array):
        """
        行列を列に分割する関数
        """
        lst_1 = [lst[0] for lst in array]
        lst_2 = [lst[1] for lst in array]

        return lst_1, lst_2
