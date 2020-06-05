import murtanto as m
from murtanto import function as f

kuki = eval(open("data.json").read())["cookies"]

ses = m.Account(kuki)
print(f.leave_group(ses,  33583936376122))
#print(ses.session.html)