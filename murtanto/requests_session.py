# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

from bs4 import BeautifulSoup as bs
from . import sorting
import requests

class HttpRequest(requests.Session):
    def __init__(self):
        super(HttpRequest, self).__init__()
        self._html = None
        self.headers.update({"User-Agent":"Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5A Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36"})

    def set_cookies(self, cookies):
        self.cookies = requests.utils.cookiejar_from_dict(sorting.to_dict_cookies(cookies))

    def get(self, url, **kwargs):
        rv = super(HttpRequest, self).get(url, **kwargs)
        self._html = rv.text
        return rv

    def post(self, url, **kwargs):
        rv = super(HttpRequest, self).post(url, **kwargs)
        self._html = rv.text
        return rv
       
    def bs4(self):
    	return bs(self.html, "html.parser")
    
    def current_title(self):
        data = bs(self._html, "html.parser")
        return data.find("title").text

    def current_hidden_input(self, index = None):
        data = []
        for x in bs(self._html, "html.parser").find_all("form"):
            z = dict((y["name"], y["value"]) for y in x.find_all("input", {"type":"hidden", "name":True, "value":True}))
            data.append(z)
        
        if type(index) == int:
        	return data[index]
        return data
    
    @property
    def html(self):
        return self._html
