#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import coquadb
import math
import sys

# ページ切り替え部分を生成
def make_page(page, num):
	link = lambda x : " … "  if x == 0 else (F'<a href="#{x}" class = "link">{x}</a> ' if x != page else F'<b>{x} </b>')
	if num <= 12:
		lst = range(1, num+1)
	elif page <= 9:
		lst = list(range(1, 11)) + [0, num]
	elif num - page < 9:
		lst = [1, 0] + list(range(num-9, num+1))
	else:
		ratio = math.floor((8 * page - 1)/num)
		lst = [1, 0] + list(range(page-ratio-1, page+9-ratio)) + [0, num] 
	return '<div class = "page">' + ''.join(map(link, lst)) + '</div>'

# １つのレシピへのリンクを生成
def make_link(lst):
	form = '<div class = "recipe">'\
	       '<div class = "recipe_img">'\
	       '<img src = "https://img.cpcdn.com/recipes/%s/100x141c/%s" height = 141px width = 100px>'\
	       '</div>'\
	       '<div class = "recipe_cont">'\
	       '<a href = https://cookpad.com/recipe/%s>%s</a>'\
	       '</div>'\
	       '</div>'
	return ''.join(map(lambda x: form % (x[0],x[2],x[0],x[1]),lst))

# ページ部分を生成
def print_cont(page, limit, txt, checklst, sortrule, orderrule):
	lst = txt.split()
	Alst = [x     for x in lst if x[0] != '-']
	Nlst = [x[1:] for x in lst if x[0] == '-']
	cdb = coquadb.CoquaDB('coqua.db')
	# 検索件数と結果
	offset = (page - 1) * limit
	count, data = cdb.ingredients_search(Alst, Nlst, sortrule, orderrule, checklst, limit, offset)
	page_switch = make_page(page, math.floor(1+(count-1)/limit))
	page_recipe = make_link(data)
	print(F"<!-- \n{cdb.last}\n -->\n")
	if txt != "":
		print(F'「{txt}」\n')
	print('' + str(count) + '件の検索結果\n')
	print(page_switch)
	print('<div class = "cont">')
	print(page_recipe)
	print('</div>')
	print(page_switch)
	cdb.close()

def search(form):
	# 並び替え順の決定
	sortrule  = form['sort'].value  if 'sort'  in form else 'repo'
	orderrule = form['order'].value if 'order' in form else 'desc'
	# ページ番号
	page = int(form['page'].value[1:]) if 'page' in form else 1
	# checkboxの値を得る
	checklst = [i for i in range(1, 10) if F"filter{i}" in form and form[F"filter{i}"].value == 'true']
	# レシピを出力
	print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
	txt = form['text'].value if 'text' in form else ""
	if txt != '' or checklst != []:
		print_cont(page, 10, txt, checklst, sortrule, orderrule)

def recommend(form):
	# レシピを出力
	print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
	print('ここに余剰材料レシピ検索の結果が表示される予定です．')


if __name__ == '__main__':
	cgitb.enable()
	form = cgi.FieldStorage()
	# モード
	mode = form['mode'].value if 'mode' in form else sys.exit(1)
	if mode == 'search':
		search(form)
	elif mode == 'recommend':
		recommend(form)

