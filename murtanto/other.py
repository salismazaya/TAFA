# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output
from . import parsing
import re

@check_login
def msgUrl(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/messages" if not next else next).text
	data = parsing.parsing_href(html, "/read/")
	next = parsing.parsing_href_regex(html, r"[?]pageNum.*selectable", one = True)
	return Output(items = data, next = next, html = html, session_number = ses.session_number)

@check_login
def myGroup(ses):
	html = ses.session.get("https://mbasic.facebook.com/groups/?seemore&refid=27").text
	data = parsing.parsing_href_regex(html, r"/groups/\d+\W", bs4_class = True)
	data = [(x.text, re.search(r"/(\d+)\W", x["href"]).group(1)) for x in data]
	return Output(items = data, html = html, session_number = ses.session_number)

def find_id_friend(ses, name):
  html = ses.session.get("https://mbasic.facebook.com/search/people/?q={}&source=filter&isTrending=0".format(name)).text
  url = parsing.parsing_href(html, "__xts__", one = True)
  try:
    html = ses.session.get(url).text
    if not "removefriend.php?friend_id=" in html:
      return
    name = parsing.getTitle(html)
    id_ = re.search(r"owner_id=(\d+)", html).group(1)
    profile_picture = parsing.to_bs4(html).find("img", {"alt": lambda x: x and "profile picture" in x})["src"]
    return (name, id_, profile_picture)
  except IOError:
    return
 
def find_id_group(ses, name):
  html = ses.session.get("https://mbasic.facebook.com/search/groups/?q={}&source=filter&isTrending=0".format(name)).text
  url = parsing.parsing_href(html, "__xts__", one = True)
  try:
    html = ses.session.get(url).text
    return (parsing.getMyName(html), re.search(r"/groups/(\d+)", html).group(1))
  except:
    return
