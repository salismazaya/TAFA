# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output, People, Group
from . import parsing
import re

@check_login
def msgUrl(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/messages" if not next else next).text
	data = parsing.parsing_href(html, "/read/")
	next = parsing.parsing_href_regex(html, r"[?]pageNum.*selectable", one = True)
	return Output(ses, msgUrl, items = data, next = next, html = html)

@check_login
def myGroup(ses):
  html = ses.session.get("https://mbasic.facebook.com/groups/?seemore&refid=27").text
  data = parsing.parsing_href_regex(html, r"/groups/\d+\W", bs4_class = True)
  data = [(x.text, re.search(r"/(\d+)\W", x["href"]).group(1)) for x in data]
  return Output(ses, myGroup, items = data, html = html)

def find_people(ses, name):
  html = ses.session.get("https://mbasic.facebook.com/search/people/?q={}&source=filter&isTrending=0".format(name)).text
  url = parsing.parsing_href(html, "__xts__", one = True)
  try:
    html = ses.session.get(url).text
    return People(ses, html)
  except:
    return
 
def find_group(ses, name):
  html = ses.session.get("https://mbasic.facebook.com/search/groups/?q={}&source=filter&isTrending=0".format(name)).text
  url = parsing.parsing_href(html, "__xts__", one = True)
  try:
    # print("in try")
    id_ = re.search(r"/(\d+)\Wrefid", url).group(1)
    html = ses.session.get("https://mbasic.facebook.com/groups/{}?view=info".format(id_)).text
    return Group(ses, html)
  except:
    return

@check_login
def list_album(ses, id):
  if id.isdigit():
    url = f"https://mbasic.facebook.com/profile.php?v=photos&id={id}"
  else:
    url = f"https://mbasic.facebook.com/{id}/photos"

  html = ses.session.get(url).text
  data = parsing.parsing_href(html, "/albums/", bs4_class = True)
  
  data = [(x.text, "https://mbasic.facebook.com" + x["href"]) for x in data]
  return Output(ses, list_album, items = data, html = html)

@check_login
def list_photo_inAlbum(ses, url, next = None, html = None):
    if not html:
        html = ses.session.get(url if not next else next).text

    data = parsing.parsing_href_regex(html, r"photo.php|/photos/")

    def get_photo(url):
        html_ = ses.session.get(url).text
        data = parsing.to_bs4(html_).find("div",  {"style":"text-align:center;"}).find("img").get("src")
        return data

    data = list(map(lambda url: get_photo(url), data))
    next = parsing.parsing_href(html, "?start_index=", one = True)
    return Output(ses, list_photo_inAlbum, arg = [url], items = data, html = html, next = next)

@check_login
def get_photo_from_inbox(ses, url, next = None, html = None):
    if not html:
        html = ses.session.get(url if not next else next).text

    data = parsing.to_bs4(html).find_all("img", {"src":lambda x: "oh=" in x and "oe=" in x, "alt":False})
    data = [x.get("src") for x in data]
    next = parsing.parsing_href_regex(html, r"(last_message_timestamp)(pagination_direction=)", one = True)
    return Output(ses, get_photo_from_inbox, arg = [url], items = data, html = html, next = next)

@check_login
def option_post_people(ses, id, next = None, html = None):
    html = ses.session.get(("https://mbasic.facebook.com/" + id) if not next else next).text
    data = parsing.parsing_href(html, "direct_actions/?context_str=")
    next = parsing.parsing_href(html, "?cursor", one = True)
    return Output(ses, option_post_people, arg = [id], items = data, html = html, next = next)

