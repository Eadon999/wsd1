# 実装の説明

## ingredient_search.pyについて

以下のように実装をする：
```
$ python ingredient_search.py ../preprocessed/filtered_ingredient.csv (探索キーワード)
```

とする。例えば、
```
$ python ingredient_search.py ../preprocessed/filtered_ingredient.csv キャベツ
```
と実行すると、その出力は以下のようになる：
```
...
1128216	: キャベツ
3079370 : キャベツ(フトメセンギリハバ2cmイ)
3240131 : レタスヤキャベツナド
1405013 : キャベツ
1426773 : キャベツ
240933 : キャベツモヤシシイタケナド
3399393 : キャベツ
939554 : キャベツ
286028 : レイトウロールキャベツ
4425172 : キャベツ
2433495 : キャベツ
3884060 : キャベツ
1751733 : キャベツ(ザクギリ)
...
```
