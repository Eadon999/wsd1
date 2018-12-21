import MeCab

mecab = MeCab.Tagger('-Oyomi')


def get_readings_array(data):
    result = [[mecab.parse(item).replace('\n', '')
               for item in lst] for lst in data]
    return result


def get_reading_list(data):
    return [mecab.parse(item).replace('\n', '') for item in data]


def get_reading(word):
    return mecab.parse(word).replace('\n', '')
