import requests
from bs4 import BeautifulSoup
#Let's cache this shit
import requests_cache
requests_cache.install_cache('bgj_cache')
import re
import hashlib
import sys

def username(Username):
	""" 
		1. FB-registered users has a little twitchy nicky thingy
		basically Name Surname => name-surname 

		2. all usernames are lowercased in the url
		3. _ is allowed but stripped from the username in the url.
	"""
	return Username.lower().replace("_", "").replace(" ", "-")


def yes_I_said_fetch_profile_picture(email):
	""" We wantz pics. """
	return "http://www.gravatar.com/avatar/%(email)s?d=retro" % dict(email=hashlib.md5(email.lower().encode("ascii")).hexdigest())
	

def fetch_profile_picture(Username):
	""" Gets the user profile picture from GGJ.org """
	try:
		r = requests.get("http://globalgamejam.org/users/%(Username)s"%dict(Username=username(Username)))
		if r.status_code == 200:
			soup=BeautifulSoup(r.text.encode("utf-8"), "lxml")
			for img in soup.find_all("img"):
				src = img.get("src")
				if "http://globalgamejam.org/sites/default/files/styles/user_profile_picture" in src:
					return src
		else:
			return "http://2.bp.blogspot.com/-_yj8c1GkwBQ/UQYmVgZAS6I/AAAAAAAABWQ/at7VveLohSA/s1600/404-terror.png"

		return None
	except ValueError as e:
		print(sys.exc_info()[0])
		print("If you have run in python3 before and are now running python2, you might need to delete the cache for it to work again.")
		print("Try deleting the bgj_cache.sqlite file in this folder.")
		sys.exit(1)



def find_or_create_picture(jammer):
	url = fetch_profile_picture(jammer["Username"])
	if "default_images" in url:
		return yes_I_said_fetch_profile_picture(jammer["Email"])
	return url


if __name__ == '__main__':
	url = fetch_profile_picture("torthu")
	url_really = yes_I_said_fetch_profile_picture("torthu")
	import webbrowser
	webbrowser.open(url)
	webbrowser.open(url_really)