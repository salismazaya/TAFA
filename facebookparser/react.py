# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output
from . import sorting
from . import parsing

@check_login
def react_core(ses, func, arg, url, next, string_next):
	html = ses.session.get(url if not next else next).text
	data = parsing.parsing_href(html, "reactions/picker")
	next = sorting.to_mbasic(parsing.parsing_href(html, string_next, one = True))
	return Output(ses, func, arg = arg, items = data, next = next, html = html)

def react_post_home(ses, next = None):
	return react_core(ses, react_post_home, [], "https://mbasic.facebook.com/home.php", next, "?aftercursorr=")

def react_post_people(ses, id, next = None):		
	return react_core(ses, react_post_people, [id], "https://mbasic.facebook.com/{}?v=timeline".format(id), next, "?cursor")

def react_post_fanspage(ses, username, next = None):	
	return react_core(ses, react_post_fanspage, [username], "https://mbasic.facebook.com/{}".format(username), next, "?sectionLoadingID=")

def react_post_group(ses, id, next = None):
	return react_core(ses, react_post_group, [id], "https://mbasic.facebook.com/groups/{}".format(id), next, "?bacr=")