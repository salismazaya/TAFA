# coded by: salism3
# 23 - 05 - 2020 23:18 (Malam Takbir)

def to_dict_cookies(string_cookies):
    try:
        string_cookies = string_cookies.replace(" ", "")
        dict_cookies = dict(x.split("=") for x in string_cookies.split(";"))
        return dict_cookies
    except:
        return {"datr":""}

def to_mbasic(url):
	if not url:
		return url
	if not "https://mbasic.facebook.com" in url:
		return "https://mbasic.facebook.com" + url
	return url