# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from . import parsing

class Pewaris:
	def __init__(self, html, number):
		self._html = html
		self.number = number

	@property
	def html(self):
		return self._html

	def bs4(self):
		return parsing.to_bs4(self.html)

class Output(Pewaris):
	def __init__(self, ses, func, arg = [], items = None, next = None, html = None):
		super(Output, self).__init__(html, ses.session_number)
		self._ses = ses
		self._func = func
		self.__arg = arg
		self.items = items
		self._next = next
		self.isNext = bool(self.next_url)
	
	def __repr__(self):
		return "<total_items: {}, next: {}>".format(len(self.items), self.next_url)

	def next(self):
		if not self._next:
			return

		return self._func(self._ses, *self.__arg, next = self._next)

	@property
	def next_url(self):
		rv = self._next
		return rv

class People(Pewaris):
	def __init__(self, ses, html):
		super(People, self).__init__(html, None)
		self.ses = ses
		self.profile_picture = parsing.People.get_profile_picture(html)
		self.cover_picture = parsing.People.get_cover_picture(html)
		self.name = parsing.People.getName(html)
		self.id = parsing.People.getId(html)
		self.getFunction()

	def __repr__(self):
		return "<type: People, name: {}, id: {}>".format(self.name, self.id)

	# import di funsgi untuk menghindari error
	def getFunction(self):
		from .friend import list_friend
		from . import action
		self.list_friend_ = list_friend
		self.action = action

	def send_msg(self, msg):
		return self.action.people.send_msg(self.ses, self.id, msg)

	def list_friend(self):
		return self.list_friend_(self.ses, self.id)

	def unfriend(self):
		return self.action.people.unfriend(self.ses, self.id)

	def follow(self):
		return self.action.people.follow(self.ses, self.id)

	def unfollow(self):
		return self.action.people.unfollow(self.ses, self.id)

class Group(Pewaris):
	def __init__(self, ses, html):
		super(Group, self).__init__(html, None)
		self.ses = ses
		self.name = parsing.Group.getName(html)
		self.id = parsing.Group.getId(html)
		self.member = "/group/leave/?group_id={}".format(self.id) in self.html
		self.total_member = parsing.Group.total_member(html)
		self.getFunction()

	def __repr__(self):
		return "<type: Group, name: {}, id: {}, member: {}, total_member: {}>".format(self.name, self.id, self.member, self.total_member)

	# import di funsgi untuk menghindari error
	def getFunction(self):
		from .group import member_group
		from . import action
		self.member_group_ = member_group
		self.action = action

	def join_group(self):
		return self.action.group.join_group(self.ses, self.id)

	def leave_group(self):
		return self.action.group.leave_group(self.ses, self.id)

	def member_group(self):
		return self.member_group_(self.ses, self.id)

class Fanspage(Pewaris):
	def __init__(self, ses, html):
		super(Fanspage, self).__init__(html, None)
		self.ses = ses
		self.name = parsing.Fanspage.getName(html)
		self.username = parsing.Fanspage.getUsername(html)
		self.getFunction()

	def __repr__(self):
		return "<type: Fanspage, name: {}, username: {}>".format(self.name, self.username)

	def getFunction(self):
		from . import action
		self.action = action

	def like(self):
		return self.action.fanspage.like(self.ses, self.username)

	def unlike(self):
		return self.action.fanspage.unlike(self.ses, self.username)

	def follow(self):
		return self.action.fanspage.follow(self.ses, self.username)

	def unfollow(self):
		return self.action.fanspage.unfollow(self.ses, self.username)

	def send_msg(self, msg):
		return self.action.fanspage.send_msg(self.ses, self.username, msg)

# class Story(Pewaris):
# 	def __init__(self, ses, html):
# 		super(Story, self).__init__(html, None)
# 		self.ses = ses
	
# 	@property
# 	def whoPosted(self):
# 		return parsing.Story.getTuanStatus(self.html)

	
