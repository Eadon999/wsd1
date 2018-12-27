#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys
import coquadb

import os.path

cgitb.enable()

form = cgi.FieldStorage(encoding = 'utf-8')
dct={}
for key in form.keys():
	dct[key] = form.getvalue(key)

box = ''
if 'text' in dct:
	txt = dct['text']
	lst = txt.split()
	Alst = []
	Nlst = []
	for x in lst:
		if x[0] != '-':
			Alst.append(x)
		else:
			Nlst.append(x[1:])
	cdb = coquadb.CoquaDB('coqua.db')
	lst = cdb.ingredients_list(Alst, Nlst)
	box = '「' + txt + '」 ' + str(len(lst)) + '件の検索結果'
	for num in lst:
		box += "<p><a href = https://cookpad.com/recipe/" + str(num) + ">";
		box += cdb.name(num)[0] + "</a></p>"
else:
	box += '材料名を入れて検索してみましょう'

print('Content-type: text/html\nAccess-Control-Allow-Origin: *\n')
print(box)
