from flask import Flask, render_template, request
from murtanto import function
import murtanto
import base64
import json

ses = None

app = Flask(__name__)

@app.errorhandler(murtanto.exception.CookiesInvalid)
@app.errorhandler(TypeError)
def cookies_error(error):
	return json.dumps({"status":"false", "msg":"cookies invalid"})

@app.errorhandler(Exception)
def handle_error(error):
	return json.dumps({"status":"false", "msg":str(error)})

@app.route("/")
def index():
	return render_template("index.html", ses = ses)

@app.route("/myfriends")
def myfriend():
	next_ = request.args.get("next")
	if next:
		try:
			next_ = base64.b64decode(next_.encode()).decode()
		except:
			next_ = None
	data = murtanto.myFriend(ses, next = next_)
	next_ = None if not data.next else base64.b64encode(data.next.encode()).decode()
	# print(next_)
	return render_template("myfriends.html", ses = ses, items = data.items, next = next_)

@app.route("/mygroups")
def mygroups():
	data = murtanto.myGroup(ses)
	return render_template("mygroups.html", ses = ses, items = data.items)

@app.route("/reaction/<in_>")
def reaction(in_):
	if in_ == "hm":
		return render_template("react_hm.html")
	elif in_ == "ft":
		return render_template("react_ft.html")
	elif in_ == "gr":
		return render_template("react_gr.html")
	elif in_ == "fp":
		return render_template("react_fp.html")
	else:
		raise Exception("404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.");

@app.route("/comment/<in_>")
def comment(in_):
	if in_ == "hm":
		return render_template("comment_hm.html")
	elif in_ == "ft":
		return render_template("comment_ft.html")
	elif in_ == "gr":
		return render_template("comment_gr.html")
	elif in_ == "fp":
		return render_template("comment_fp.html")
	else:
		raise Exception("404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.");

@app.route("/mass/<menu>")
def mass_menu(menu):
	if menu == "unfriend":
		title = "Mass Unfriend"
		func_dump = "myFriend"
		index_id = 1
		method = "GET"
		func_process = "unfriend"
	elif menu == "accept-friend":
		title = "Mass Accept Friend Request"
		func_dump = "friend_request"
		index_id = 0
		method = "POST"
		func_process = "open_url"
	elif menu == "reject-friend":
		title = "Mass Reject Friend Request"
		func_dump = "friend_request"
		index_id = 1
		method = "POST"
		func_process = "open_url"
	elif menu == "unadd":
		title = "Mass Unadd"
		func_dump = "friend_requested"
		index_id = ""
		method = "POST"
		func_process = "open_url"

	return render_template("mass_template.html",
		title = title,
		func_dump = func_dump,
		index_id = index_id,
		method = method,
		func_process = func_process,
	)

@app.route("/function")
def func():
	return ""

@app.route("/function/open_url", methods = ["POST"])
def open_url():
	url = request.form["id"]
	ses.session.get(url)
	return json.dumps({"status":True})

@app.route("/function/unfriend")
def unfriend_gas():
	id_ = request.args.get("id")
	if not id_:
		return json.dumps({"status":False})

	data = function.unfriend(ses, id_)
	return json.dumps({"status":data.status})

@app.route("/function/leave")
def leave_group():
	id_ = request.args.get("id")
	if not id_:
		return json.dumps({"status":False})

	data = function.leave_group(ses, id_)
	return json.dumps({"status":data.status})

@app.route("/function/dump")
def dump():
	func = request.args.get("func")
	limit = request.args.get("limit")

	if limit == None or int(limit) < 0: 
		limit = 10

	kwargs = request.args.copy()
	del kwargs["func"]
	if request.args.get("limit") != None:
		del kwargs["limit"] 

	func = eval(f"murtanto.{func}")
	data = func(ses, **kwargs)
	kwargs["next"] = data.next

	if data.next:
		data_ = function.dump(func, args = (ses,), kwargs = kwargs, limit = int(limit))
	else:
		data_ = []

	data_ = data_ + data.items

	rv = {"status":True, "title":data.bs4().find("title").text, "items":data_[:int(limit)]}
	return json.dumps(rv)

@app.route("/function/reaction", methods = ["POST"])
def give_react():
	url = request.form["url"]
	type_ = request.form["type"]

	data = function.react(ses, url, type = type_)

	return json.dumps({"status":data.status})

@app.route("/function/comment", methods = ["POST"])
def give_comment():
	url = request.form["url"]
	comment_value = request.form["comment_value"]

	data = function.comment(ses, url, comment_value)

	return json.dumps({"status":data.status})
