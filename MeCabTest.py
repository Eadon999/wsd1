import sys
import MeCab
# neologdの辞書のパスを変えたりしてみてください
m = MeCab.Tagger("-d /usr/lib/mecab/dic/mecab-ipadic-neologd/")
print(m.parse("回鍋肉"))
print(m.parse("たまねぎ"))
print(m.parse("玉ねぎ"))
print(m.parse("玉葱"))
