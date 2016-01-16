import requests
from bs4 import BeautifulSoup
#Let's cache this shit
import requests_cache
requests_cache.install_cache('bgj_cache')
import re
import hashlib

def username(Username):
	""" 
		FB-registered users has a little twitchy nicky thingy
		basically Name Surname => name-surname 
	"""
	return Username.lower().replace(" ", "-")


def yes_I_said_fetch_profile_picture(email):
	""" We wantz pics. """
	return "http://www.gravatar.com/avatar/%(email)s?d=retro" % dict(email=hashlib.md5(email.lower()).hexdigest())
	

def fetch_profile_picture(Username):
	""" Gets the user profile picture from GGJ.org """
	r = requests.get("http://globalgamejam.org/users/%(Username)s"%dict(Username=username(Username)))
	if r:
		soup=BeautifulSoup(r.text.encode("utf-8"), "lxml")
		for img in soup.find_all("img"):
			src = img.get("src")
			if "http://globalgamejam.org/sites/default/files/styles/user_profile_picture" in src:
				return src


def find_or_create_picture(jammer):
	url = fetch_profile_picture(jammer["Username"])
	if "default" in url:
		return yes_I_said_fetch_profile_picture(jammer["Email"])
	return url


if __name__ == '__main__':
	url = fetch_profile_picture("torthu")
	url_really = yes_I_said_fetch_profile_picture("torthu")
	import webbrowser
	webbrowser.open(url)
	webbrowser.open(url_really)