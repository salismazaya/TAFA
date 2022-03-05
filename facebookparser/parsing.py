# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from bs4 import BeautifulSoup as parser
from . import sorting
from .parsing_in_class import *
import re

def to_bs4(html):
	return parser(html, "html.parser")

def refsrc(html):
	return True if re.search(r'http.+\Wrefsrc', html) else False

def parsing_href(html, href, one = False, bs4_class = False):
	data = to_bs4(html)
	if one:
		data = data.find("a", href = lambda x: x and href in x)
		if not bs4_class and data != None:
			data = sorting.to_mbasic(data["href"])
	else:
		data = data.find_all("a", href = lambda x: x and href in x)
		if not bs4_class:
			data = [sorting.to_mbasic(x["href"]) for x in data]
	return data

def parsing_href_regex(html, pattern, one = False, bs4_class = False):
	data = to_bs4(html)
	if one:
		data = data.find("a", href = lambda x: re.search(pattern, x))
		if not bs4_class and data != None:
			data = sorting.to_mbasic(data["href"])
	else:
		data = data.find_all("a", href = lambda x: re.search(pattern, x))
		if not bs4_class:
			data = [sorting.to_mbasic(x["href"]) for x in data]
	return data

def getMyName(html):
	data = to_bs4(html).find("title").text
	return data

def getTitle(html):
	data = to_bs4(html).find("title").text
	return data

def getMyId(html):
    data = to_bs4(html).find("a", href = lambda x:"/allactivity" in x)["href"]
    data = re.search(r"/\d+/?", data).group().replace("/", "")
    return data

def getHiddenInput(html, post_action):
	rv = {}
	data = to_bs4(html).find("form", action = lambda x: post_action in x)
	data = data.find_all("input", {"type":"hidden", "name":True, "value":True})
	for x in data:
		rv[x["name"]] = x["value"]
	return rv