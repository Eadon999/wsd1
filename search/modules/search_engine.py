import MeCab


mecab = MeCab.Tagger('-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


class SearchEngine(object):

    def get_url(self, readings, ids, include, exclude):
        """
        includeが含まれるレシピのurlをリスト化し、返す
        """
        result = [{index: f'https://cookpad.com/recipe/{ids[index]}'}
                  for index, lst in enumerate(readings)
                  if self.check_list_included(include, lst)
                  and not self.check_list_similarity(exclude, lst)]
        return result

    def get_ids(self, readings, ids, include, exclude):
        result = [ids[index]
                  for index, lst in enumerate(readings)
                  if self.check_list_included(include, lst)
                  and not self.check_list_similarity(exclude, lst)]
        return result

    def get_target_readings(self, word):
        """
        単語の読みをカタカナで返す関数
        """
        return mecab.parse(word).replace('\n', '')

    def check_list_similarity(self, lst1, lst2):
        """
        2つのリストに共通のオブジェクトが含まれるか確認する関数
        含まれる場合：True
        含まれない場合: False
        """
        return set(lst1).intersection(set(lst2))

    def check_list_included(self, lst1, lst2):
        """
        lst1の全要素がlst2に含まれるか確認する関数（順不同）
        含まれる：True
        含まれない：False
        """
        return set(lst1).issubset(set(lst2))
