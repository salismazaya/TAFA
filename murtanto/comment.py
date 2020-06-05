# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .checker import check_argument
from .output import Output
from . import sorting
from . import parsing

@check_login
def comment_core(ses, url, next, string_next):
	html = ses.session.get(url if not next else next).text
	data = parsing.parsing_href(html, "#footer_action_list")
	next = sorting.to_mbasic(parsing.parsing_href(html, string_next, one = True))
	return Output(items = data, next = next, html = html, session_number = ses.session_number)

def comment_post_home(ses, next = None):
	return comment_core(ses, "https://mbasic.facebook.com", next, "?aftercursorr=")

@check_argument(["id"])
def comment_post_friend(ses, id = None, next = None):
	return comment_core(ses, "https://mbasic.facebook.com/{}?v=timeline".format(id), next, "?cursor")

@check_argument(["username"])
def comment_post_fanspage(ses, username = None, next = None):
	return comment_core(ses, "https://mbasic.facebook.com/{}".format(username), next, "?sectionLoadingID=")

@check_argument(["id"])
def comment_post_grup(ses, id = None, next = None):
	return comment_core(ses, "https://mbasic.facebook.com/groups/{}".format(id), next, "?bacr=")