# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output
from . import sorting
from . import parsing
import re

@check_login
def friend_request(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/friends/center/requests/" if not next else next).text
	confirm = parsing.parsing_href(html, "?confirm=")

	reject = parsing.parsing_href(html, "?delete=")
	data = list(zip(confirm, reject))
	next = parsing.parsing_href(html, "?ppk=", one = True)

	return Output(ses, friend_request, items = data, next = next, html = html)

@check_login
def friend_requested(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/friends/center/requests/outgoing/" if not next else next).text
	data = parsing.parsing_href(html, "/cancel/?")
	next = parsing.parsing_href(html, "?ppk=", one = True)
	return Output(ses, friend_requested, items = data, next = next, html = html)

@check_login
def list_friend(ses, id, next = None):
	if str(id).isdigit():
		url = "https://mbasic.facebook.com/profile.php?id={}&v=friends".format(id)
	else:
		url = "https://mbasic.facebook.com/{}/friends".format(id)
	html = ses.session.get(url if not next else next).text

	data = parsing.parsing_href(html, "fref=fr_tab", bs4_class = True)
	data = [x.parent.parent for x in data]

	def sorted(x):
		name = x.find("a").text
		id_ = re.search(r"\w[\w.]+", x.find("a")["href"].replace("/", "").replace("profile.php?id=", "")).group()
		img = x.find("img")["src"]
		return name, id_, img

	data = list(map(sorted, data))
	next = parsing.parsing_href(html, "unit_cursor=", one = True)

	return Output(ses, list_friend, arg = [None], items = data, next = next, html = html)
	
def myFriend(ses, next = None):
	return list_friend(ses, ses.id, next = next)

@check_login
def onlineFriend(ses, next = None):
	out = []
	html = ses.session.get("https://mbasic.facebook.com/buddylist.php").text
	data = parsing.to_bs4(html).find_all("img", {"src":lambda x: "https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/bzGumJjigJ0.png" in x})
	data = [x.parent.parent for x in data]
	del data[0]
	
	def sorted(arg):
		a_class = arg.find("a")
		name = a_class.text
		id = a_class["href"].split("fbid=")[1].split("&")[0]
		return name, id

	data = list(map(sorted, data))
	return Output(ses, onlineFriend, items = data, html = html)
