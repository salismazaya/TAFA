# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .checker import check_argument
from .output import Output
from . import sorting
from . import parsing

@check_login
def friend_request(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/friends/center/requests/" if not next else next).text
	data = parsing.friendRequestParser(html)
	return Output(items = data["items"], next = data["next"], html = html, session_number = ses.session_number)

@check_login
def friend_requested(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/friends/center/requests/outgoing/" if not next else next).text
	data = parsing.parsing_href(html, "/cancel/?")
	next = parsing.parsing_href(html, "?ppk=", one = True)
	return Output(items = data, next = next, html = html, session_number = ses.session_number)

@check_login
@check_argument(["id"])
def friend(ses, id = None, next = None):
  if id.isdigit():
    url = "https://mbasic.facebook.com/profile.php?id={}&v=friends".format(id)
  else:
    url = "https://mbasic.facebook.com/{}/friends".format(id)
  html = ses.session.get(url if not next else next).text
  data = parsing.listFriendParser(html)
  return Output(items = data["items"], next = data["next"], html = data["html"], session_number = ses.session_number)

def myFriend(ses, next = None):
	return friend(ses, id = ses.id, next = next)

@check_login
def onlineFriend(ses, next = None):
	out = []
	html = ses.session.get("https://mbasic.facebook.com/buddylist.php").text
	data = parsing.to_bs4(html).find_all("img", {"src":lambda x: "https://static.xx.fbcdn.net/rsrc.php/v3/ym/r/bzGumJjigJ0.png" in x})
	data = [x.parent.parent for x in data]
	del data[0]
	for x in data:
		a_class = x.find("a")
		name = a_class.text
		id_ = a_class["href"].split("fbid=")[1].split("&")[0]
		out.append((name, id_))
	return Output(items = out, html = html, session_number = ses.session_number)
