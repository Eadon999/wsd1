import pandas as pd
import sqlite3
from .rel_name        import make_rel_name
from .rel_pref        import make_rel_pref
from .rel_author      import make_rel_author
from .rel_publication import make_rel_publication
from .rel_ingredients import make_rel_ingredients
from .rel_yield       import make_rel_yield

def makedb(dbcur, csvpath):
	# データベースを再構築します
	# csvを読み込む
	df = pd.read_csv(
			csvpath,
			usecols = [
				'recipe_id',
				'author',
				'name',
				'history',
				'description',
				'advice',
				'categories',
				'related_keywords',
				'datePublished',
				'recipeYield',
				'recipeIngredient'])
	# テーブルの作成
	make_rel_name('names', dbcur, df)
	make_rel_pref('preferable_bits', dbcur, df)
	make_rel_author('authors', dbcur, df)
	make_rel_publication('publications', dbcur, df)
	make_rel_ingredients('ingredients', dbcur, df)
	make_rel_yield('yields', dbcur, df)

