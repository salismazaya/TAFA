# coded by: salism3
# 22 - 07 - 2020 12:19

import os, random, time, sys, shutil
from glob import glob
from getpass import getpass

try:
	import facebookparser as fb
	from facebookparser import action
	from colorama import init, Fore, Back
	init(autoreset=True)
except ImportError:
	print("Installing modules ...")
	os.system(("python" if os.name == "nt" else "python3") + " -m pip install requests bs4 colorama")
	exit("\nSuccess")

B = Fore.BLUE
W = Fore.WHITE
C = Fore.CYAN
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
ERR = f"   {R}[!]{W} " 
QUE = f"   {C}[?]{W} "
INF = f"   {C}[+]{W} " 
DAN = f"{R} [!]"

TOTAL_ENTER = 0

ses = None

list_menu = {
	"like": [
		"Spam Like in Home",
		"Spam Like in People Timeline",
		"Spam Like in Group", 
		"Spam Like in Fanspage"
	],
	"react": [
		"Spam React in Home",
		"Spam React in People Timeline",
		"Spam React in Group",
		"Spam React in Fanspage"
	],
	"comment": [
		"Spam Comment in Home",
		"Spam Comment in People Timeline",
		"Spam Comment in Group",
		"Spam Comment in Fanspage"
	],
	"people": [
		"Mass Accept Friend Request" + DAN,
		"Mass Reject Friend Request" + DAN,
		"Mass Unadd (not Unfriend)",
		"Mass Unfriend" + DAN,
		"Mass Follow Friend",
		"Mass Unfollow Friend",
	],
	"group": [
		"Mass Leave Group" + DAN,
	],
	"chat": [
		"Mass Chat Friend",
		"Mass Chat Online Friend",
	],
	"downloader": [
		"Album Downloader",
		"Mass Download Photo in Inbox"
	],
	"deleter": [
		"Mass Delete Chat" + DAN,
		"Mass Delete Post" + DAN,
		"Mass Untag" + DAN,
		"Mass Unlike/Unreact Post"
	],
	"other": [
		"Find Id People",
		"Find Id Group",
		"Delete Empty Output Folder",
		"Delete All Output",
	],
	"unreact": [
		"Mass Unlike/Unreact in People Timeline",
		"Mass Unlike/Unreact in Fanspage"
	]
}


LOGO = f""" 
   {B}╔╦╗{W}┌─┐┌─┐┌─┐  {B}╔╦╗{W}┌─┐┌─┐┬  ┬┌─┬┌┬┐
    {B}║{W} ├─┤├┤ ├─┤   {B}║{W} │ ││ ││  ├┴┐│ │ 
    {B}╩{W} ┴ ┴└  ┴ ┴   {B}╩{W} └─┘└─┘┴─┘┴ ┴┴ ┴ v{B}1.5{W}"""

def updateFunc(func):
	def inner():
		global CURRENT_FUNC
		CURRENT_FUNC = func
		func()
	return inner

def randomstring(num):
	char = list("qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM")
	rv = "".join([random.choice(char) for _ in range(num)])
	return rv

def banner():
	os.system("cls" if os.name == "nt" else "clear")
	print(LOGO)
	print("    " + Back.BLUE + Fore.BLACK + random.choice([" donate: https://cutt.ly/salismazaya ", " by: salismazaya from xiuzcode "]))
	print()

def input_(text, que = True, looping = True):
	if looping:
		for _ in range(8):
			rv = input((QUE if que else "") + text + C)
			if rv.strip():
				return rv
			else:
				print(f"   {R}[!]{W} blank input\n")
		else:
			print(f"   {R}[!]{W} Dah lah maless !!!")
			enter()

	else:
		return input((QUE if que else "") + text + C)


def select(min, max, text = "   >>> ", error_msg = "input not valid", que = False):
	for _ in range(8):
		try:
			data = int(input_(W + text, que = que, looping = False))
			if data in range(min, max + 1):
				return data
		except ValueError:
			pass
		print(f"   {R}[!]{W} {error_msg}\n")
	else:
		print(f"   {R}[!]{W} Dah lah maless !!!")
		enter()

def confirm_execute():
	text = "yes" + str(random.randint(0,999)).zfill(3)
	if input_(f"type '{text}' to confirm: ", looping = False) != text:
		print(ERR + "operation cancelled!")
		enter()

def check_login(cookies = None):
	global ses
	if not cookies:
		try:
			cookies = open("cookies.txt").read()
		except:
			return False
	ses = fb.Account(cookies)
	return ses.logged

def show_select_menu(menu, back = True):
	for i, x in enumerate(menu):
		print(f"   {C}{i + 1}).{W} {x}")

	if back:
		print(f"   {C}0).{W} Back")

	return select(0 if back else 1, len(menu))

# use lambda function for argument dump_func
def dump(dump_func, limit, show_target = True):
	data = dump_func()
	rv = data.items

	time.sleep(1)
	print()
	if show_target:
		title = data.bs4().find("title").text
		print(f"{INF}Target: {G}{title[:22]}")
	print(f"{INF}Getting data ...")

	if not data.isNext or len(rv) > limit:
		print(f"{INF}Total: {G}{len(rv[:limit])}")
		return rv[:limit]

	rv += action.dump(data, limit = limit - len(rv))
	print(f"{INF}Total: {G}{len(rv[:limit])}")
	return rv[:limit]

def procces(func, list_, before_done = None):
	count = 0
	total = len(list_)
	for x in list_:
		count += 1
		data = func(x)
		count_proccess(count, total)
		time.sleep(random.random() * random.randint(1,3))
	print()
	if callable(before_done):
		before_done()
	print(INF + "Done!")
	enter()

def count_proccess(count, total):
	angka = str(count * 100 / total)
	a, b = angka.split(".")

	angka = f"{a}.{b[:2].ljust(2, ' ')} %"

	sys.stdout.write(f"\r{INF}Proccess: {G}{angka}{W}")
	sys.stdout.flush()

@updateFunc
def home():
	banner()
	print(f"""   {C}1).{W} Go To Menu
   {C}2).{W} Login
   {C}3).{W} Logout
   {C}4).{W} Update
   {C}0).{W} Exit""")
	pilih = select(0,4)
	if pilih == 0:
		banner()
		print("    Thank you for using this tool ^_^")
	elif pilih == 1:
		if not check_login():
			print(ERR + "You must login!")
			enter()
		else:
			menu()
	elif pilih == 2:
		if not check_login():
			login()
		else:
			print(ERR + "You has been login!")
			enter()
	elif pilih == 3:
		confirm_execute()
		os.remove("cookies.txt")
		enter()
	elif pilih == 4:
		print(W + "\n   if you install this tool from git")
		print("   you can type 'git pull'")

def login():
	global ses
	os.system("cls" if os.name == "nt" else "clear")
	print(f"""               
			 {R}[WARNING]{W}

   1. Your account can be banned if you use this
   2. After successfully logging in your account will
      automatically comment on the author
      profile photo and react
   3. Don't use this for crime
   4. Everything the user does is not the responsibility
      of the author
   5. By using this the user is considered to
      understand and comply with the above provisions
      """)

	cookies = input_("Your Facebook Cookies: ")
	ses = fb.Account(cookies)
	try:
		url = "https://mbasic.facebook.com/photo.php?fbid=166694224710808&id=100041106940465"
		msg = ["Hello I'M TAFA User", "Halo bro gw user Tafa btw toolnya keren banget", "be yourself and never surrender"]
		action.status.comment(ses, url, random.choice(msg))
		time.sleep(1)
		action.status.react(ses, url, type = random.choice(["wow", "love"]), in_reactions_picker = False)
	except:
		pass
	if ses.logged:
		open("cookies.txt", "w").write(cookies)
		print(f"{INF}Successully Login!")
		enter()
	else:
		print(ERR + "Cookies Not Valid!")
		enter()

@updateFunc
def menu():
	banner()
	print(f"   Login as: {G}{ses.name[:22]}")
	print(f"   UID     : {G}{ses.id}\n")
	print(f"{C}   No.{W} Menu\n{Y}   --- ----")
	func = [like_menu, react_menu, comment_menu, people_menu, group_menu, chat_menu, downloader_menu, deleter_menu, other_menu]
	pilih = show_select_menu([
		"Like",
		"React", 
		"Comment", 
		"People", 
		"Group", 
		"Chat", 
		"Downloader", 
		"Deleter", 
		"Other",
	])
	if pilih == 0:
		home()
	else:
		func[pilih - 1]()

@updateFunc
def like_menu():
	banner()
	menu_ = list_menu["like"]
	pilih = show_select_menu(menu_)
	show_target = True

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		func = lambda: fb.like_post_home(ses)
		show_target = False

	elif pilih == 2:
		target = input_("Id People: ")
		func = lambda: fb.like_post_people(ses, target)

	elif pilih == 3:
		target = input_("Id Group: ")
		func = lambda: fb.like_post_group(ses, target)

	elif pilih == 4:
		target = input_("Username Fanspage: ")
		func = lambda: fb.like_post_fanspage(ses, target)

	limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = show_target)
	procces(lambda url: action.open_url(ses, url), data)

@updateFunc
def react_menu():
	banner()
	menu_ = list_menu["react"]
	type_react = ["love", "care", "haha", "wow", "sad", "angry"]
	pilih = show_select_menu(menu_)
	show_target = True

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:

		func = lambda: fb.react_post_home(ses)
		show_target = False

	elif pilih == 2:
		target = input_("Id People: ")
		func = lambda: fb.react_post_people(ses, target)

	elif pilih == 3:
		target = input_("Id Group: ")
		func = lambda: fb.react_post_group(ses, target)

	elif pilih == 4:
		target = input_("Username Fanspage: ")
		func = lambda: fb.react_post_fanspage(ses, target)

	limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
	react = show_select_menu(list(map(lambda x: x.capitalize(), type_react)))
	react = type_react[react - 1]
	confirm_execute()
	data = dump(func, limit, show_target = show_target)
	procces(lambda url: action.status.react(ses, url, type = react), data)

@updateFunc
def comment_menu():
	banner()
	menu_ = list_menu["comment"]
	pilih = show_select_menu(menu_)
	show_target = True

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")
	
	if pilih == 1:
		func = lambda: fb.comment_post_home(ses)
		show_target = False

	elif pilih == 2:
		target = input_("Id People: ")
		func = lambda: fb.comment_post_people(ses, target)
	
	elif pilih == 3:
		target = input_("Id Group: ")
		func = lambda: fb.comment_post_group(ses, target)

	elif pilih == 4:
		target = input_("Username Fanspage: ")
		func = lambda: fb.comment_post_fanspage(ses, target)

	comment = input_("Comment: ")
	limit = select(1, 100, text = "Limit: ", error_msg = "min: 1, max: 100", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = show_target)
	procces(lambda url: action.status.comment(ses, url, comment), data)

@updateFunc
def people_menu():
	banner()
	menu_ = list_menu["people"]
	pilih = show_select_menu(menu_)

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		func = lambda: fb.friend_request(ses)
		execute_func = lambda url: action.open_url(ses, url[0])

	elif pilih == 2:
		func = lambda: fb.friend_request(ses)
		execute_func = lambda url: action.open_url(ses, url[1])

	elif pilih == 3:
		func = lambda: fb.friend_requested(ses)
		execute_func = lambda url: action.open_url(ses, url)

	elif pilih == 4:
		func = lambda: fb.myFriend(ses)
		execute_func = lambda data: action.people.unfriend(ses, data[1])

	elif pilih == 5:
		func = lambda: fb.myFriend(ses)
		execute_func = lambda data: action.people.follow(ses, data[1])

	elif pilih == 6:
		func = lambda: fb.myFriend(ses)
		execute_func = lambda data: action.people.unfollow(ses, data[1])

	limit = select(1, 300, text = "Limit: ", error_msg = "min: 1, max: 300", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = False)
	procces(execute_func, data)

@updateFunc
def group_menu():
	banner()
	menu_ = list_menu["group"]
	pilih = show_select_menu(menu_)

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		func = lambda: fb.myGroup(ses)
		execute_func = lambda data: action.group.leave_group(ses, data[1])

	limit = select(1, 200, text = "Limit: ", error_msg = "min: 1, max: 200", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = False)
	procces(execute_func, data)

@updateFunc
def chat_menu():
	banner()
	menu_ = list_menu["chat"]
	pilih = show_select_menu(menu_)

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		func = lambda: fb.myFriend(ses)

	elif pilih == 2:
		func = lambda: fb.onlineFriend(ses)

	msg = input_("Message: ")
	limit = select(1, 100, text = "Limit: ", error_msg = "min: 1, max: 100", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = False)
	procces(lambda data: action.people.send_msg(ses, data[1], msg), data)

@updateFunc
def downloader_menu():
	banner()
	menu_ = list_menu["downloader"]
	pilih = show_select_menu(menu_)
	folder = randomstring(10)

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		target = input_("Id People: ")
		album = fb.list_album(ses, target).items
		print(f"{INF}Select album:")
		pilih = show_select_menu([x[0] for x in album], back = False)

		album = album[pilih - 1][1]
		func = lambda: fb.list_photo_inAlbum(ses, album)


	elif pilih == 2:
		url = input_("Url Inbox (use mbasic): ")
		func = lambda: fb.get_photo_from_inbox(ses, url)

	limit = select(1, 99999, text = "Limit: ", error_msg = "min: 1, max: 99999", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = False)
	os.mkdir("output/" + folder)
	procces(lambda url: open(f"output/{folder}/{randomstring(10)}.jpg", "wb").write(ses.session.get(url).content), data, before_done = lambda: print(f"{INF}file saved in folder: output/{folder}"))

@updateFunc
def deleter_menu():
	banner()
	menu_ = list_menu["deleter"]
	pilih = show_select_menu(menu_)

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		func = lambda: fb.msgUrl(ses)
		execute_func = lambda url: action.people.deleteMsg(ses, url)

	elif pilih == 2:
		func = lambda: fb.option_post_people(ses, "me")
		execute_func = lambda url: action.status.delete_post(ses, url)

	elif pilih == 3:
		func = lambda: fb.option_post_people(ses, "me")
		execute_func = lambda url: action.status.untag_post(ses, url)

	elif pilih == 4:
		unreact_submenu()
		exit()

	limit = select(1, 200, text = "Limit: ", error_msg = "min: 1, max: 200", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = False)
	procces(execute_func, data)

@updateFunc
def unreact_submenu():
	banner()
	menu_ = list_menu["unreact"]
	pilih = show_select_menu(menu_)
	show_target = True

	if pilih == 0:
		deleter_menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	# if pilih == 1:
	# 	func = lambda: fb.like_post_home(ses)
	# 	show_target = False

	if pilih == 1:
		target = input_("Id People: ")
		func = lambda: fb.react_post_people(ses, target)

	# elif pilih == 3:
	# 	target = input_("Id Group: ")
	# 	func = lambda: fb.react_post_group(ses, target)

	elif pilih == 2:
		target = input_("Username Fanspage: ")
		func = lambda: fb.react_post_fanspage(ses, target)

	limit = select(1, 350, text = "Limit: ", error_msg = "min: 1, max: 350", que = True)
	confirm_execute()
	data = dump(func, limit, show_target = show_target)
	procces(lambda url: action.status.react(ses, url, type = "unreact"), data)

@updateFunc
def other_menu():
	banner()
	menu_ = list_menu["other"]
	pilih = show_select_menu(menu_)

	if pilih == 0:
		menu()
		exit()

	banner()
	print(f"   {C}Selected:{W} {menu_[pilih - 1]}\n")

	if pilih == 1:
		text = input_("Full Name: ")
		data = fb.find_people(ses, text)
		if not data:
			print(ERR + "Not Found!")
		else:
			print(f"{INF}Name: {data.name}")
			print(f"{INF}ID  : {data.id}")
	elif pilih == 2:
		text = input_("Full Name: ")
		data = fb.find_group(ses, text)
		if not data:
			print(ERR + "Not Found!")
		else:
			print(f"{INF}Name: {data.name}")
			print(f"{INF}ID  : {data.id}")
	elif pilih == 3:
		confirm_execute()
		data = glob("output/*")
		for x in data:
			if len(os.listdir(x)) == 0:
				os.rmdir(x)
		print(f"{INF}Done!")
	elif pilih == 4:
		confirm_execute()
		data = glob("output/*")
		for x in data:
			shutil.rmtree(x)
		print(f"{INF}Done!")

	enter()


CURRENT_FUNC = home

def enter():
	global TOTAL_ENTER
	TOTAL_ENTER += 1
	if TOTAL_ENTER > 8:
		exit()
	getpass(f"\n   {C}[{W} Press Enter to Back {C}]{W}")
	CURRENT_FUNC()
	exit()

try:
	home()
except KeyboardInterrupt:
	exit(ERR + "Exit: Ok")
except Exception as e:
	print(ERR + str(e))
