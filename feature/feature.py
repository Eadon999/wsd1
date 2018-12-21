
# 引数でfeature.txtのpathを指定してください
# seriesを返します. 下のコメントの概形を参考に

import pandas as pd

def feature(path):
    with open(path) as f:
        l = f.readlines()
    df = pd.Series(l)
    df_feature = df.str.extractall("([^ \s\d,()'']+)",)
    se_feature = pd.Series(df_feature[0])
    return se_feature

if __name__ == "__main__":
    import sys
    args = sys.argv
    se = feature(args[1])
    print(se)

# 概形
# print(type(se_feature[0]))
# pandasのseries
# print(se_feature[0])
# match
# 0      簡単
# 1      手軽
# 2    シンプル
# 3      時間
# 4      時短
# 5      手間
# 6      面倒
# 7     忙しい
# print(type(se_feature[0][1]))
# str
# print(se_feature[0][1])
# 手軽
