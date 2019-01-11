# 実装の説明

## ingredient_search.pyについて

以下のように実装をする：
```
$ python ingredient_search.py ../preprocessed/filtered_ingredient.csv 
```

とする。コマンドラインでは、以下のように定義する

```
検索する材料名をスペース区切りで入力してください： (材料名)
検索から省く材料名をスペース区切りで入力してください：(材料名)
余剰材料検索を行いますか？(y / n)： (y/n)

```

