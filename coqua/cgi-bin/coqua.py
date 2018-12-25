#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys
import coquadb

import os.path

cgitb.enable()
print('Content-type: text/html; charset=UTF-8\r\n')

html = """
<!doctype html>
<html lang="ja">
	<head>
		<meta charset="UTF-8">
		<meta name="keywords" content="COQUA">
		<meta name="description" content="レシピ推薦サービス">
		<meta name="author" content="COQUA">
		<link rel="stylesheet" type="text/css" href="../style/css.css">
		<title>COQUA</title>
	</head>
	<body>
		<header>
			<h1><a href = '../../'>COQUA</a></h1>
		</header>
		<main>
			<article>
				%s
			</article>
		</main>
		<footer>
			<p> - COQUA - </p>
		</footer>
		</div>
	</body>
</html>
"""

form = cgi.FieldStorage(encoding = 'utf-8')
dct={}
for key in form.keys():
	dct[key] = form.getvalue(key)

box = ''
if 'text' in dct:
	lst = dct['text'].split()
	Alst = []
	Nlst = []
	for x in lst:
		if x[0] != '-':
			Alst.append(x)
		else:
			Nlst.append(x[1:])
	cdb = coquadb.CoquaDB('cgi-bin/coqua.db')
	lst = cdb.ingredients_list(Alst, Nlst)
	for num in lst:
		box += "<p><a href = https://cookpad.com/recipe/" + str(num) + ">";
		box += cdb.name(num)[0] + "</a></p>"
print(html % box)


