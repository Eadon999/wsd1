#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import coquadb

def make_page(num_split, n):
	tmp = [F'<a class = "cont{x}" href = "#cont{x}">{x}</a> ' if x != n else F'<b>{x} </b>' for x in range(1, num_split+1)]
	return '<div class = "page">' + ''.join(tmp) + '</div>'


def make_link(lst):
	tmp = [F'<p><img src = "{url}" height = 141px width = 100px><a href = https://cookpad.com/recipe/{num}>{name}</a></p>' for [num, name, url] in lst]
	return '<div class = "link">' + ''.join(tmp) + '</div>'


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
	if 'text' in form:
		txt = form['text'].value
		lst = txt.split()
		Alst = [x     for x in lst if x[0] != '-']
		Nlst = [x[1:] for x in lst if x[0] == '-']
		cdb = coquadb.CoquaDB('coqua.db')
		data = cdb.ingredients_search(Alst, Nlst)
		box = '「' + txt + '」 ' + str(len(data)) + '件の検索結果\n'
		box += get_cont(data)
	else:
		box = '材料名を入れて検索してみましょう'

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
print(box)
