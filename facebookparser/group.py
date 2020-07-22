# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .output import Output
from . import sorting
from . import parsing

@check_login
def member_group(ses, id, next = None):
	url = "https://mbasic.facebook.com/browse/group/members/?id={}".format(id)
	html = ses.session.get(url if not next else next).text
	data = parsing.to_bs4(html).find_all("table", {"id":lambda x: x and "member_" in x})

	def sorted(arg):
		name = arg.find("a", href = True).text
		id_ = arg["id"].replace("member_", "")
		img = arg.find("img").get("src")
		return name, id_, img

	next_ = parsing.parsing_href(html, "&cursor=", one = True)
	data = list(map(sorted, data))
	return Output(ses, member_group, arg = [id], items = data, next = next_, html = html)