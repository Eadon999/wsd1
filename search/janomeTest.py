import os
import sys
from janome.charfilter import *
from janome.tokenizer import Tokenizer
from janome.tokenfilter import *
from janome.analyzer import Analyzer

args = sys.argv
line = args[1]

cf = []
t = Tokenizer()
tf = []
a = Analyzer(cf, t, tf)

print(' (1) 入力: ')
print(line)

for token in a.analyze(line):
    print(' (2) Token オブジェクト: ')
    print(token)

    print(' (3) 読み: ')
    print(token.reading)
