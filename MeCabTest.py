import sys
import MeCab

args = sys.argv
s = args[1]

# neologdの辞書のパスを変えたりしてみてください
m = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd/")

# 引数に指定した文字列をneologdを辞書としたMeCabで形態素解析します
print(m.parse(s))
