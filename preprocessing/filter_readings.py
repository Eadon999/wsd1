import MeCab

mecab = MeCab.Tagger('-Oyomi')


def get_readings_list(data):
    result = [[mecab.parse(item).replace('\n', '')
               for item in lst] for lst in data]
    return result
