from modules.utility import UtilityModules

utility = UtilityModules()


def get_yield_list(data):
    get_yield = utility.get_yield(data)  # 人数の大きい方を抽出
    result = get_yield.values.tolist()  # リストに変換

    return result
