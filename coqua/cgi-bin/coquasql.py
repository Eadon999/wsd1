import sqlite3

def decode_query(querylst):
	if querylst in [None, []]:
		return None
	return '\n'.join(querylst)

def indent_query(querylst, first, last):
	if querylst == []:
		return []
	if len(querylst) == 1:
		lst = [first + querylst[0] + last]
	else:
		lst = [first + querylst[0]]
		ind = ' ' * len(first)
		for i in querylst[1:-1]:
			lst.append(ind + i)
		lst.append(ind + querylst[-1] + last)
	return lst

def pref_bits(checklst):
	if checklst == []:
		return None
	lst = [ 'SELECT recipe_id',
	        '  FROM preferable_bits',
	       F' WHERE pref{checklst[0]} = 1']
	for i in checklst[1:]:
		lst.append(F'   AND pref{i} = 1')
	return lst

# 単一材料名検索
def ingredient_ids(pron):
	lst = [ 'SELECT recipe_id',
	        '  FROM ingredients',
	       F' WHERE pron = "{pron}"']
	return lst

# 除外するid検索
def notlst_ids(Nlst):
	if Nlst == []:
		return None
	lst =  [    'SELECT recipe_id',
	            '  FROM ingredients',
	           F' WHERE pron = "{Nlst[0]}"']
	for i in Nlst[1:]:
		lst += [F'    OR pron = "{i}"']
	return lst

# 複数材料名検索
def ingredients_ids(Alst, Nlst):
	if Alst == []:
		return None
	Alst = list(map(ingredient_ids, Alst))
	Nlst = list(map(ingredient_ids, Nlst))
	tmp = Alst[0]
	for i in Alst[1:]:
		tmp.extend(['','INTERSECT',''] + i)
	for i in Nlst:
		tmp.extend(['','EXCEPT','']    + i)
	return tmp

# 複数材料名検索（改良版）
def ingredients_ids2(Alst, Nlst):
	if Alst == []:
		return None
	Alst = list(map(ingredient_ids, Alst))
	tmp = Alst[0]
	for i in Alst[1:]:
		tmp.extend(['','INTERSECT',''] + i)
	if Nlst != []:
		tmp.extend(['','EXCEPT','']    + notlst_ids(Nlst))
	return tmp

# 複数材料名検索（改良版２）
def recur_andlst_ids(Alst):
	lst =     [ 'SELECT recipe_id']
	lst +=    [ '  FROM ingredients']
	lst +=    [F' WHERE pron = "{Alst[0]}"']
	if Alst[1:] != []:
		lst += [ '   AND recipe_id IN']
		lst += indent_query(recur_andlst_ids(Alst[1:]), '       (',')')
	return lst
def ingredients_ids3(Alst, Nlst):
	if Alst == []:
		return None
	lst = recur_andlst_ids(Alst)
	if Nlst != []:
		lst.extend(['','EXCEPT','']    + notlst_ids(Nlst))
	return lst

# 材料名クエリに絞り込みのクエリを追加
def filter_ids(checklst, Qlst):
	if Qlst == None:
		return None
	if checklst != []:
		Plst = pref_bits(checklst)
		if Plst != []:
			Qlst = Plst + ['','INTERSECT',''] + Qlst
	return Qlst

# ソート
def sort_ids(Qlst, table, col, d):
	if Qlst in [[], None]:
		return None
	lst = [     'SELECT DISTINCT',
	            '       names.recipe_id,',
	            '       names.name,',
	            '       images.url',
	            '  FROM names',
	            '  JOIN images']
	if table != None:
	   lst += [F'  JOIN {table}']
	if table != None:
	   lst += [F'    ON {table}.recipe_id = names.recipe_id']
	   lst += [F'   AND {table}.recipe_id = images.recipe_id']
	else:
	   lst += [F'    ON names.recipe_id = images.recipe_id']
	lst +=    [ ' WHERE names.recipe_id IN']
	lst +=  indent_query(Qlst, '       (', ')')
	if table != None:
	   lst += [F' ORDER BY {table}.{col}' + (' DESC' if d == 'desc' else '')]
	return lst      

def recipe_data(Qlst):
	return sort_ids(Qlst,None,None,None)

