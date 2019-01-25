import MeCab
import itertools
# from ortoolpy import knapsack
import cvxpy


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

    def get_indexes(self, readings, ids, include, exclude):
        """
        検索にヒットしたレシピのインデックスをリストで返す関数
        """
        result = [index
                  for index, lst in enumerate(readings)
                  if self.check_list_included(include, lst)
                  and not self.check_list_similarity(exclude, lst)]
        return result

    def get_ids(self, ids, indexes):
        """
        index番目のidをリストとして返す
        """
        result = [int(ids[index]) for index in indexes]
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

    def get_pairing_element(self, target, id_lst, lst1, lst2, recipe_index):
        """
        lst_1のリストの同じインデックスのlst_2の要素を取り出す
        return: [{'item': {'id': 'amount', ...}, ...}]
        """
        result = {
            item: {
                id_lst[i]: lst2[num][lst1[num].index(item)]
                for i, num in enumerate(recipe_index)
            } for item in target
        }

        return result

    def get_combination_sum(self, amount, ingredient, data):
        """
        data内の指定された材料がamountになるように計算し、その組み合わせを出力する
        """
        for item in ingredient:
            amounts = list(data.get(item).values())
        for index, amount in enumerate(amounts):
            if isinstance(amount, str):
                amounts[index] = 999
        print(amounts)
        # print(list(self.subset_sum(amounts, 3)))

    def subset_sum(self, numbers, target, partial=[], partial_sum=0):
        if partial_sum == target:
            yield partial
        if partial_sum >= target:
            return
        for i, n in enumerate(numbers):
            remaining = numbers[i + 1:]
            yield from self.subset_sum(remaining, target, partial + [n], partial_sum + n)

    def knapsack(self, lst, weight, target):
        x = cvxpy.Variable(shape=len(weight), boolean=True)
        objective = cvxpy.Maximize(weight * x)
        print(objective)
        constraints = [target >= lst * x]
        prob = cvxpy.Problem(objective, constraints)
        prob.solve(solver=cvxpy.ECOS_BB)
        print('最大価値:{} / 組み合わせ:{}'.format(round(prob.value, 0),
                                          [i for i in range(len(weight)) if round(x.value[i], 0) == 1]))
        # print(knapsack(lst, weight, target))
