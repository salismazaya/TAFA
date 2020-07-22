# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output
from . import sorting
from . import parsing

@check_login
def like_core(ses, func, arg, url, next, string_next):
	html = ses.session.get(url if not next else next).text
	data = parsing.parsing_href(html, "like.php")
	next = sorting.to_mbasic(parsing.parsing_href(html, string_next, one = True))
	return Output(ses, func, arg = arg, items = data, next = next, html = html)

def like_post_home(ses, next = None):
	return like_core(ses, like_post_home, [], "https://mbasic.facebook.com/home.php", next, "?aftercursorr=")

def like_post_people(ses, id, next = None):		
	return like_core(ses, like_post_people, [id], "https://mbasic.facebook.com/{}?v=timeline".format(id), next, "?cursor")

def like_post_fanspage(ses, username, next = None):	
	return like_core(ses, like_post_fanspage, [username], "https://mbasic.facebook.com/{}".format(username), next, "?sectionLoadingID=")

def like_post_group(ses, id, next = None):
	return like_core(ses, like_post_group, [id], "https://mbasic.facebook.com/groups/{}".format(id), next, "?bacr=")