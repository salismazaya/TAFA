# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .requests_session import HttpRequest
from bs4.element import Tag
from . import sorting
from . import parsing
from .like import *
from .comment import *
from .friend import *
from .react import *
from .other import *

like_post_group = like_post_grup
react_post_group = react_post_grup
comment_post_group = comment_post_grup

class Account:
    __number = 0
    __logged = False
	
    def __init__(self, cookies):
        self._name = None
        self._id = None
        self._cookies = None
        self._session = None
        self._session_active = False
        self.info = None
        self.session_number = self.__tambah()
        self.login(cookies)
    
    def __repr__(self):
        return "<logged: {}, name: {}, id: {}, session_number: {}, info: {}>".format(self.__logged, self._name, self._id, self.session_number, self.info)

    @classmethod
    def __tambah(cls):
        cls.__number += 1
        return cls.__number
        
    @property
    def logged(self):
        return self.__logged
    
    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id
    
    @property
    def cookies(self):
        return self._cookies
    
    @property
    def session(self):
        return self._session
    
    def login(self, cookies):
        self._cookies = cookies
        self._session = HttpRequest()
        self.session.set_cookies(cookies)
        data = self.session.get("https://mbasic.facebook.com/me")
        html = data.text
        if not "?refsrc" in data.url and "mbasic_logout_button" in html:
            self.__success_login(html)
        else:
            self.info = "failed login! when taking cookies make sure not in free mode"
    
    def __success_login(self, html):
        self.info = "You successfully login"
        self.__logged = True
        self._session_active = True
        self._name = parsing.getMyName(html)
        self._id = parsing.getMyId(html)

        profile_picture = parsing.to_bs4(html).find("img", alt = lambda x: x and "profile picture" in x)
        self.profile_picture = profile_picture.get("src") if type(profile_picture) == Tag else None

