#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import coquadb

def make_page(num_split, n):
	tmp = [F'<a class = "cont{x}" href = "#cont{x}">{x}</a> ' if x != n else F'<b>{x} </b>' for x in range(1, num_split+1)]
	return '<div class = "page">' + ''.join(tmp) + '</div>'


def make_link(lst):
	tmp = '';
	for [num, name, url] in lst:
		tmp += '<div class = "recipe">'
		tmp += '<div class = "recipe_img">'
		tmp += F'<img src = "{url}" height = 141px width = 100px>'
		tmp += '</div>'
		tmp += '<div class = "recipe_cont">'
		tmp += F'<a href = https://cookpad.com/recipe/{num}>{name}</a>'
		tmp += '</div>'
		tmp += '</div>'
	return tmp


def get_cont(lst):
	len_split = 10
	num_split = int((len(lst)-1)/len_split)+1
	lsts = [lst[i : i+len_split] for i in range(0, len(lst), len_split)]
	tmp = '<div class = "cont">'
	for i, lst in zip(range(1, num_split+1), lsts):
		tmp += F'<div id = "cont{i}">' if i == 1 else F'<div id = "cont{i}" style = "display:none;">'
		tmp += make_page(num_split, i) + make_link(lst) + make_page(num_split, i)
		tmp += '</div>'
	tmp += '</div>'
	return tmp


if __name__ == '__main__':
	cgitb.enable()
	form = cgi.FieldStorage()
	# 並び替え順の決定
	sortrule = form['sort'].value if 'sort' in form else 'repo'
	# checkboxの値を得る
	checklst = [i for i in range(1, 9) if F"filter{i}" in form and form[F"filter{i}"].value == 'true']
	# レシピを出力
	print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
	txt = form['text'].value if 'text' in form else ""
	if txt != '' or checklst != []:
		lst = txt.split()
		Alst = [x     for x in lst if x[0] != '-']
		Nlst = [x[1:] for x in lst if x[0] == '-']
		cdb = coquadb.CoquaDB('coqua.db')
		data = cdb.ingredients_search(Alst, Nlst, sortrule, checklst)
		print(F"<!-- \n{cdb.last}\n -->\n")
		print('「' + txt + '」 ' + str(len(data)) + '件の検索結果\n')
		print(get_cont(data))
		cdb.close()

