#!/usr/bin/env python
#coding: utf-8
import os

try:#io from right folder.
	from config import WEBROOT
	os.chdir(WEBROOT)
except:
	pass
	


errormsg = dict(
missing_jammers_file=""" 
	Ah hoy!, forgotten something Mrs/Mr? 
		-Missing 'jammers.csv'. 

	Make sure 'jammers.csv' is in the same folder 
	as this script and run again. This file contains 
	the information about your site's jammers. 

	Download it from your jamsite's global gamejam page. 
	Click the button [Download Jammer info] 
	at the bottom, beneath the list of jammers.
	""",

missing_dependecies="""
	Failed to import dependencies, (python modules this script uses).
	You can install all dependencies by running these 
	commands in the terminal: (copy, paste, enter)

	%s
	"""%open('dependencies.txt').read()
)



def make_minimum_configuration():
	"""
		Generates the minimum required configuration to run
		the web-interface out of the box
	"""
	SECRET_KEY = ''.join('%02x' % ord(x) for x in os.urandom(16))
	with open("config.py", "w") as configfile:
		configfile.write("SECRET_KEY='%s'\n"%SECRET_KEY)



def load_sources():
		""" Will attempt to load sources from config,
			returns default sources if config doesn't exist.
		"""
		try:
			import config
			sources = getattr(config, "sources", [dict(file='jammers.csv')])
		except:
			sources = [dict(file='jammers.csv')]
		return sources
