import re


class RegexModules(object):
    # def __init__(self):

    def replace_pat_in_array(self, pat, repl, lst):
        """
        2重リストの要素全てに対して正規表現による置換をおこなう関数
        """
        result = [[self.replace_pat_in_list(pat, repl, items)
                   for items in recipe] for recipe in lst]
        return result

        # return [[re.sub(pattern, repl, item) for item in lst] for lst in sr]

    def replace_pat_in_list(self, pat, repl, lst):
        """
        リストの全要素に対して正規表現による置換を行う関数
        """
        return [re.sub(pat, repl, item) for item in lst]

    def replace_lst_member(self, pattern, repl, index, lst):
        """ return list
        リストの指定した要素に対して正規表現による置換をおこなう関数
        """

        if len(lst) <= index:
            print(f'List does not have {index} items')
            return lst
        else:
            lst[index] = re.sub(pattern, repl, lst[index]).strip()
            return lst

    def replace_array_member(self, pattern, repl, index, sr):
        """ return sr
        2重リスト内のリストのindexメンバに対して正規表現による置換を行う関数
        """
        result = [
            [
                self.replace_lst_member(pattern, repl, index, pair)
                for pair in lst
            ] for lst in sr
        ]
        return result

    def replace_pat_in_series(self, pattern, repl, sr):
        """
        pandas.Seriesに対して正規表現による置換を行う関数
        """
        return sr.replace(pattern, repl, regex=True)
