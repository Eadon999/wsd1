単位換算器 unit_converter の概略 と 
簡易確認器 simple_checker の使い方 

------------------------ 
単位換算器 unit_converter の概略 

  4つのファイルに分かれている.
 (1) 単位換算関数 uc_functions.py 
 (2) データ入出力 uc_io.py 
 (3) 単位換算テーブル uc_tables.py 
 (4) 主単位換算器 unit_converter.py 

------------------------ 
簡易確認器 simple_checker の使い方 

例. 
  材料に「玉ねぎ」を含むレシピについて, 
    行番号, レシピID, 材料, カタカナ読み, 分量, 換算値, 新単位 
 を出力したいとき. 

        $ python simple_checker.py 玉ねぎ

 とすると, 

    行番号: レシピID: 材料 / カタカナ読み / 分量 / 換算値 新単位
       3: 2167745: 玉ねぎ / タマネギ / 0.25個 / 0.25 タマネギ
       4: 3972003: 玉ねぎ / タマネギ / 大1個 / 1.0 タマネギ
       9: 2181095: 玉ねぎ / タマネギ / 0.5個~ / 0.5 タマネギ

    ((中略))
   
    4976: 1794003: 玉ねぎ / タマネギ / 0.5個 / 0.5 タマネギ
    4988:  337890: 玉ねぎ / タマネギ / 1個 / 1.0 タマネギ
    4999: 1132302: たまねぎ / タマネギ / 3個 / 3.0 タマネギ
    検索結果 920 件 

  のように出力する. 
