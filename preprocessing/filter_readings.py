import MeCab

mecab = MeCab.Tagger('-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


def get_readings_array(array):
    """
    与えられた単語の行列の読みを行列で返す関数
    """
    result = [[mecab.parse(item).replace('\n', '')
               for item in lst] for lst in array]
    return result


def get_reading_list(lst):
    """
    与えられた単語のリストの読みをリストで返す関数
    """
    return [mecab.parse(item).replace('\n', '') for item in lst]


def get_reading(word):
    """
    与えられた単語の読みを返す関数
    """
    return mecab.parse(word).replace('\n', '')
