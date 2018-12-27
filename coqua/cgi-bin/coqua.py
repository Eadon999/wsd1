#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import coquadb

def get_cont(lst):
	len_split = 10
	num_split = int(len(lst)/len_split)
	lsts = [lst[i : i+len_split] for i in range(0, len(lst), len_split)]
	tmp = '<div class = "cont">\n'
	for i, lst in zip(range(1, num_split+1), lsts):
		if i == 1:
			tmp += F'<div id = "cont{i}">'
		else:
			tmp += F'<div id = "cont{i}" style = "display:none;">'
		tmp += '<div class = "page">'
		for j in range(1, num_split+1):
			tmp += F'<a href = "#cont{j}">{j}</a> '
		tmp += '</div>'
		tmp += '<div class = "link">'
		for [num, name] in lst:
			tmp += F'<p><a href = https://cookpad.com/recipe/{num}>{name}</a></p>'
		tmp += '</div>'
		tmp += '</div>'
	tmp += '</div>'
	return tmp


if __name__ == '__main__':
	cgitb.enable()
	form = cgi.FieldStorage()
	if 'text' in form:
		txt = form['text'].value
		lst = txt.split()
		Alst = [x     for x in lst if x[0] != '-']
		Nlst = [x[1:] for x in lst if x[0] == '-']
		cdb = coquadb.CoquaDB('coqua.db')
		num_lst = cdb.ingredients_list(Alst, Nlst)
		recipes = list(map(lambda x : [x, cdb.name(x)[0]], num_lst))
		box = '「' + txt + '」 ' + str(len(recipes)) + '件の検索結果\n'
		box += get_cont(recipes)
	else:
		box = '材料名を入れて検索してみましょう'

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
print(box)
