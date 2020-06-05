# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from bs4 import BeautifulSoup as bs

class Output:
	def __init__(self, items = None, next = None, html = None, url = None, session_number = None):
		self.items = items
		self.html = html
		self.url = url
		self.session_number = session_number
		self._next = next
	
	def __repr__(self):
		return "<total_items: {}, next: {}>".format(len(self.items), self.next)

	def bs4(self):
		return bs(self.html, "html.parser")

	@property
	def next(self):
		rv = self._next
		return rv

class Output2:
	def __init__(self, status, html, session_number):
		self.status = status
		self.html = html
		self.session_number = session_number

	def __repr__(self):
		return "<status: {}>".format(self.status)

	def bs4(self):
		return bs(self.html, "html.parser")		