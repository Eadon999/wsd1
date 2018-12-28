import mojimoji
import MeCab

mecab = MeCab.Tagger('-Oyomi -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')


class Formatter(object):
    def convert_str_to_list(self, string, splitter):
        """
        文字列をsplitter区切りとしてリストとして返す関数
        """
        # 全角を半角に変換（ただしカタカナは全角のまま）
        string = mojimoji.zen_to_han(string, kana=False)

        # 文字列をカタカナに変更
        string = mecab.parse(string).replace('\n', '')

        return string.split(splitter)
