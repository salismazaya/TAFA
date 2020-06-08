# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from .exception import CookiesInvalid
from .exception import ArgumentError
from .parsing import refsrc
from functools import wraps

def check_login(func):
	@wraps(func)
	def inner(*args, **kwargs):
		data = func(*args, **kwargs)
		if refsrc(data.html):
			raise CookiesInvalid(data.session_number)
		return data
	return inner

def check_argument(kwargs):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs_):
			if None in [kwargs_.get(x) for x in kwargs]:
				raise ArgumentError("check argument in function '{}'".format(func.__name__))
			return func(*args, **kwargs_)
		return wrapper
	return decorator