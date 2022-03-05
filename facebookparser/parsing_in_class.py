from . import parsing
import re

class People:
	def get_profile_picture(html):
		return parsing.to_bs4(html).find("img", {"alt": lambda x: x and "profile picture" in x})["src"]

	def get_cover_picture(html):
		data = parsing.to_bs4(html)
		cover = data.find("div", {"id":lambda x: x and "profile_cover_photo_container" in x})
		if cover:
			return

		return data.find("img", {"src":lambda x: x and "scontent" in x})["src"]

	def getName(html):
		return parsing.to_bs4(html).find("title").text

	def getId(html):
		return re.search(r"owner_id=(\d+)", html).group(1)

class Group:
	def getName(html):
		return parsing.to_bs4(html).find("title").text

	def getId(html):
		return re.search(r"/groups/(\d+)\Wview", html).group(1)

	def total_member(html):
		return parsing.to_bs4(html).find("span", {"id":"u_0_0"}).text

class Fanspage:
	def getName(html):
		return parsing.to_bs4(html).find("title").text

	def getUsername(html):
		return parsing.to_bs4(html).find("span", string = lambda x: x and "@" in x).text.replace("@", "")