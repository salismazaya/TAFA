# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output
from . import parsing

@check_login
def msgUrl(ses, next = None):
	html = ses.session.get("https://mbasic.facebook.com/messages" if not next else next).text
	data = parsing.parsing_href(html, "/read/")
	next = parsing.parsing_href(html, "?pageNum", one = True)
	return Output(items = data, next = next, html = html, session_number = ses.session_number)