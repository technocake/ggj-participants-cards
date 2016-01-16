import requests
from bs4 import BeautifulSoup

url = "http://globalgamejam.org/2016/jam-sites/bergen-game-jam/members"
post_url = "http://globalgamejam.org/2016/jam-sites/bergen-game-jam/members?destination=jame-site-members/24449"
edit_url = "http://globalgamejam.org/node/24449/edit"
fields = {
	'name': "technocake",
	'pass': input("password"),
	'form_build_id': "form-Q9IMgjb_n7eAORUhgFwUvLxvkDqiqEjDirmC4gpSaSw",
	'form_id': "user_login_block"}


session = requests.Session()


# Get login form details
r = requests.get(url)
soup = BeautifulSoup(r.text.encode("utf-8"), "lxml")
fields['form_build_id'] = [inp.get("value") for inp in soup.find_all("input") if "build" in inp.get("name") ][1]

# Login
r = requests.post(post_url, data=fields)

print len(r.cookies)

r = session.get(edit_url)
print r, r.status_code #r.text.encode("utf-8")

