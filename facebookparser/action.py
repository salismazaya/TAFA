# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .checker import check_login
from . import output
from . import sorting
from . import parsing
import time

def open_url(ses, url):
	return ses.session.get(url).text

def dump(func, args = [], kwargs = {}, limit = 100):
	time.sleep(0.8)
	rv = []

	if type(func) == output.Output and func.isNext:
		data = func.next()
	else:
		data = func(*args, **kwargs)

	rv += data.items[:limit]
	if len(rv) >= limit:
		return rv[:limit]
	while data.isNext:
		data = data.next()
		rv += data.items
		if len(rv) >= limit:
			return rv[:limit]
	return rv

class Output:
	def __init__(self, ses, status, html):
		self.status = status
		self._html = html
		self.session_number = ses.session_number

	@property
	def html(self):
		return self._html

	def bs4(self):
		return parsing.to_bs4(self.html)

	def __repr__(self):
		return "<status: {}>".format(self.status)

class status:
	@check_login
	def like(ses, url, _html = None):
		html = ses.get(url).text if not _html else _html
		status = True
		try:
			url = parsing.parsing_href(html, "/like.php", one = True)
			html = ses.session.get(url).text
		except:
			status = False
		return Output(ses, status, html)


	@check_login
	def comment(ses, url, text, _html = None):
		r_ses = ses
		ses = ses.session
		html = ses.get(url).text if not _html else _html
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
		return Output(ses, status, html)

	@check_login
	def react(ses, url, type = "like", in_reactions_picker = True, _html = None):
		r_ses = ses
		ses = ses.session
		status = True

		if not in_reactions_picker:
			html = ses.get(url).text if not _html else _html
			url = parsing.parsing_href(html, "reactions/picker", one = True)

		html = ses.get(url).text if not _html else _html
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
				url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=16&" in x)["href"])
			elif type == "love":
				url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=2&" in x)["href"])
			elif type == "unreact":
				url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=0&" in x)["href"])
			else:
				url = sorting.to_mbasic(data.find("a", href = lambda x: "&reaction_type=1&" in x)["href"])
			# print(url)
			html = ses.get(url).text
		except:
			status = False

		return Output(ses, status, html)

	@check_login
	def delete_post(ses, option_url):
		status = True
		html = ses.session.get(option_url).text
		try:
			url_post = parsing.to_bs4(html).find("form", {"method":"post", "action":lambda x: x and "/nfx/basic/handle_action" in x})["action"]
			url_post = "https://mbasic.facebook.com" + url_post
			param = ses.session.current_hidden_input(index = 0)
			param["action_key"] = "DELETE"
			# print(url_post)
			# print(param)
			html_ = ses.session.post(url_post, data = param).text
			# print(html_)
			if "mbasic_logout_button" in html_:
				html = html_
			else:
				status = False
		except:
			status = False
		return Output(ses, status, html)

	@check_login
	def untag_post(ses, option_url):
		status = True
		html = ses.session.get(option_url).text
		try:
			url_post = parsing.to_bs4(html).find("form", {"method":"post", "action":lambda x: x and "/nfx/basic/handle_action" in x})["action"]
			url_post = "https://mbasic.facebook.com" + url_post
			param = ses.session.current_hidden_input(index = 0)
			param["action_key"] = "UNTAG"
			# print(url_post)
			# print(param)
			html_ = ses.session.post(url_post, data = param).text
			# print(html_)
			if "mbasic_logout_button" in html_:
				html = html_
			else:
				status = False
		except:
			status = False
		return Output(ses, status, html)

class people:
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
		return Output(ses, status, html)

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
		return Output(ses, status, html)

	@check_login
	def addfriend(ses, id):
		status = True
		html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
		try:
			url = parsing.parsing_href(html, "profile_add_friend.php", one = True)
			req = ses.session.get(url)
			html = req.text
			if not "/friends" in req.url:
				status = False
		except:
			status = False
		return Output(ses, status, html)

	@check_login
	def unadd(ses, id):
		status = True
		html = ses.session.get("https://mbasic.facebook.com/{}".format(id)).text
		try:
			url = parsing.parsing_href(html, "/friendrequest/cancel/?", one = True)
			req = ses.session.get(url)
			html = req.text
			if not "/privacy/touch/block/confirm/" in html:
				status = False
		except:
			status = False
		return Output(ses, status, html)

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
		return Output(ses, status, html)

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
		return Output(ses, status, html)

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
		return Output(ses, status, html)

class group:
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
		return Output(ses, status, html)

	@check_login
	def join_group(ses, id):
		status = True
		html = ses.session.get("https://mbasic.facebook.com/groups/{}".format(id)).text
		try:
			url = ses.session.bs4().find("form", {"action":lambda x: x and "/join/" in x})
			url = sorting.to_mbasic(url["action"])
			data = ses.session.current_hidden_input(index = 1)
			html_ = ses.session.post(url, data = data).text
			if "?source=ErrorPage" in html_:
				raise Exception
			html = html_
		except:
			status = False
		return Output(ses, status, html)

class fanspage:
	@check_login
	def like(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "?fan&id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(ses, status, html)

	@check_login
	def unlike(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "?unfan&id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(ses, status, html)

	@check_login
	def follow(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "subscriptions/add?subject_id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(ses, status, html)

	@check_login
	def unfollow(ses, username):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "/follow_mutator/?page_id=", one = True)
			ses.session.get(url).text
		except:
			status = False
		return Output(ses, status, html)

	@check_login
	def send_msg(ses, username, msg):
		status = True
		html = ses.session.mbasic(username).text
		try:
			url = parsing.parsing_href(html, "messages/thread", one = True)
			html_ = ses.session.get(url).text
			param = ses.session.current_hidden_input(index = 1)
			param["body"] = msg
			ses.session.post("https://mbasic.facebook.com/messages/send/?icm=1&ref=dbl", data = param)
		except:
			status = False
		return Output(ses, status, html)