from modules.regex import RegexModules
from modules.formatter import FormatModules
from modules.utility import UtilityModules


symbol_pattern = '[^ぁ-んァ-ンーa-zA-Z0-9一-龠０-９.~～〜()（）/\w]+|u3000'

regex = RegexModules()
formatter = FormatModules()
utility = UtilityModules()


def cal_functions(lst):
    # 帯分数を小数へ
    result = regex.replace_pat_in_list(
        '(\d+)[と.](\d+)\/(\d+)', utility.mixedfraction_to_float, lst)

    # 分数を小数へ
    result = regex.replace_pat_in_list(
        '(\d+)\/(\d+)', utility.fraction_to_float, result)

    # 分数 (日本語) を小数へ
    result = regex.replace_pat_in_list(
        '(\d+)分の(\d+)', utility.bunsu_to_float, result)

    # 「量としての半分」を「0.5」へ (割合としての半分はそのままにしたい)
    # 具体的には, 直前に「の」がない「半分」にマッチして置換
    result = regex.replace_pat_in_list(
        '(?<!の)半分', '0.5', result)

    return result


def get_ingredient_amount_list(data):
    ingredients = formatter.convert_str_list(
        (data).map(formatter.normalize))

    # 材料の記号を除去
    ingredients = regex.replace_pat_in_array(symbol_pattern, '', ingredients)

    # 材料名と量を分割
    ingredients, amount = formatter.convert_2darray_to_lists(ingredients)

    # 量の数字を漢数字から英数字に変換
    amount = [[formatter.kanji_numbers(item)
               for item in lst] for lst in amount]

    # 量を全て小数点に変換する
    amount = [cal_functions(lst) for lst in amount]

    return ingredients, amount
