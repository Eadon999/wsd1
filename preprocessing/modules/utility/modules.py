import pandas as pd
import unicodedata as ud


class UtilityModules(object):

    def normalize(self, y):
        """
        全角数字を半角数字に変換する関数
        """
        if pd.isnull(y):
            return y  # 欠損値
        return ud.normalize('NFKC', y)  # 全角数字を半角数字へ

    def get_yield(self, sr):
        items = sr.values.tolist()
        # result = [item for item in items if not isinstance(item, float)]
        # sr = pd.Series(result)
        sr = pd.Series(items)  # 欠損値を除去しない (行数は不可変)
        sr = sr.map(self.normalize)
        return sr.str.extract('(?P<yield>\d+)人', expand=False)

    def mixedfraction_to_float(self, matchobj):
        """
        帯分数を小数へ
        """
        i0 = int(matchobj.group(1))
        i1 = int(matchobj.group(2))
        i2 = int(matchobj.group(3))
        s0 = str(round(i0+i1/i2, 2))
        return s0

    def fraction_to_float(self, matchobj):
        """
        分数を小数へ
        """
        i0 = int(matchobj.group(1))
        i1 = int(matchobj.group(2))
        s0 = str(round(i0/i1, 2))
        return s0

    def bunsu_to_float(self, matchobj):
        """
        分数 (日本語) を小数へ
        """
        i0 = int(matchobj.group(1))
        i1 = int(matchobj.group(2))
        s0 = str(round(i1/i0, 2))  # (「2分の1」など)
        return s0
