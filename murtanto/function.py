# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from .checker import check_argument
from .output import Output2
from . import sorting
from . import parsing

def open_url(ses, url):
	return ses.session.get(url).text

@check_login
def comment(ses, url, text):
	r_ses = ses
	ses = ses.session
	html = ses.get(url).text
	status = True
	try:
		data = parsing.to_bs4(html).find("form", action = lambda x: "comment.php" in x)
		url = sorting.to_mbasic(data["action"])
		data = data.find_all("input", type = "hidden")
		fb_dtsg = data[0]["value"]
		jazoest = data[1]["value"]
		html = ses.post(url, data = dict(fb_dtsg = fb_dtsg, jazoest = jazoest, comment_text = text)).text
	except:
		status = False
	return Output2(status, html, r_ses.session_number)

@check_login
def react(ses, url, type = "like", in_reactions_picker = True):
	r_ses = ses
	ses = ses.session
	status = True

	if not in_reactions_picker:
		html = ses.get(url).text
		url = parsing.parsing_href(html, "reactions/picker", one = True)

	html = ses.get(url).text
	data = parsing.to_bs4(html)
	try:
		if type == "haha":
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=4&" in x)["href"])
		elif type == "wow":
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=3&" in x)["href"])
		elif type == "sad":
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=7&" in x)["href"])
		elif type == "angry":
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=8&" in x)["href"])
		elif type == "care":
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=1&6" in x)["href"])
		elif type == "love":
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=2&" in x)["href"])
		else:
			url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=1&" in x)["href"])
		html = ses.get(url).text
	except:
		status = False

	return Output2(status, html, r_ses.session_number)

# @check_argument(["args", "kwargs"])
def dump(func, args = [], kwargs = {}, limit = 100):
  rv = []
  kwargs = kwargs.copy()
  data = func(*args, **kwargs)
  rv += data.items[:limit]
  if len(rv) >= limit:
    return rv[:limit]
  while data.next:
    kwargs["next"] = data.next
    data = func(*args, **kwargs)
    rv += data.items
    if len(rv) >= limit:
      return rv[:limit]
  return rv

@check_login
def follow(ses, id):
	r_ses = ses
	ses = ses.session
	status = True
	html = ses.get("https://mbasic.facebook.com/{}".format(id)).text
	url = parsing.parsing_href(html, "subscribe.php", one = True)
	if not url:
		status = False
	else:
		html = ses.get(url).text
	return Output2(status, html, r_ses.session_number)

@check_login
def unfollow(ses, id):
	r_ses = ses
	ses = ses.session
	status = True
	html = ses.get("https://mbasic.facebook.com/{}".format(id)).text
	url = parsing.parsing_href(html, "subscriptions/remove", one = True)
	if not url:
		status = False
	else:
		html = ses.get(url).text
	return Output2(status, html, r_ses.session_number)

@check_login
def unfriend(ses, id):
	r_ses = ses
	ses = ses.session
	status = True
	html = ses.get("https://mbasic.facebook.com/{}".format(id)).text
	url = parsing.parsing_href(html, "removefriend", one = True)
	if not url:
		status = False
	else:
		post_data = parsing.getHiddenInput(ses.get(url).text, "removefriend")
		post_data["confirm"] = "Confirm"
		html = ses.post("https://mbasic.facebook.com/a/removefriend.php", data = post_data).text
	return Output2(status, html, r_ses.session_number)

@check_login
def send_msg(ses, id, msg):
	r_ses = ses
	ses = ses.session
	status = True
	html = ses.get("https://mbasic.facebook.com/{}".format(id)).text
	url = parsing.parsing_href(html, "messages/thread", one = True)
	if not url:
		status = False
	else:
		post_data = parsing.getHiddenInput(ses.get(url).text, "messages/send")
		post_data["body"] = msg
		post_data["Send"] = "Send"
		html = ses.post("https://mbasic.facebook.com/messages/send/?icm=1", data = post_data).text
	return Output2(status, html, r_ses.session_number)

@check_login
def deleteMsg(ses, url):
	status = True
	html = ses.session.get(url).text
	try:
		url = parsing.to_bs4(html).find("form", action = lambda x: "/messages/action_redirect" in x)["action"]
		url = sorting.to_mbasic(url)
		param = parsing.getHiddenInput(html, "/messages/action_redirect")
		param["delete"] = "Delete"
		html = ses.session.post(url, data = param).text
		url = parsing.parsing_href(html, "mm_action=delete", one = True)
		html = ses.session.get(url).text
	except:
		status = False
	return Output2(status, html, ses.session_number)

@check_login
def leave_group(ses, id):
	status = True
	html = ses.session.get("https://mbasic.facebook.com/group/leave/?group_id={}".format(id)).text
	try:
		data = ses.session.current_hidden_input(index = 1)
		html_ = ses.session.post("https://mbasic.facebook.com/a/group/leave/?qp=0", data = data).text
		if "?source=ErrorPage" in html_:
			raise Exception
		html = html_
	except:
		status = False
	return Output2(status, html, ses.session_number)		