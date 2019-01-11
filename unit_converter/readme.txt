単位換算器 unit_converter の概略と 
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

 とする. 
