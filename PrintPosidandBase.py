import sys
import pandas as pd
import MeCab

def StrToPosidAndBase(s):
    # neologdの辞書のパスを変えたりしてみてください
    # neologd内のdicrcに以下を加えてください
    # ; test
    # node-format-test = %h/%f[6]\n
    # eos-format-test = EOS\n
    m = MeCab.Tagger("-Otest -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/")
    s = m.parse(s)
    return s

if __name__ == '__main__':
    args = sys.argv
    s = args[1]
    s = StrToPosidAndBase(s)
    print(s)

