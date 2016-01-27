#!/usr/bin/env python
#coding: utf-8
import csv
from ggj import JamSite, Jammer
from simplify import errormsg
try:
	import requests
	#Let's cache this shit
	import requests_cache
except:
	print(errormsg['missing_dependencies'])
	sys.exit(1)


requests_cache.install_cache('bgj_cache')


def import_jammers(csvfile, fieldnames=None):
	"""
		Imports jammer info from [jammers.csv] 
		it will perform classification and picture (url) fetching
		returns a list of Jammer objects with propagated fields.

		Hardcoded reasoner that thinks the jammer has a ticket, 
		if it comes from the jammers.csv file.
	"""
	parsed_jammers = []
	if fieldnames is None:
		# Read fieldnames from first line of csvfile.
		jammers = csv.DictReader(csvfile) 
	else:
		# Fieldnames provided
		# Skip header line/fieldnames line
		jammers = csv.DictReader(csvfile, fieldnames)
		next(jammers)

	for jammer in jammers:
		if hasattr(csvfile, "name") and csvfile.name == "jammers.csv":
			# These jammers has registered to the jam site. 
			jammer["ticket"] = True
		# Put it in object yo.
		jammer = Jammer(**jammer)
		parsed_jammers.append(jammer)
	return parsed_jammers


def import_from_url(jamsite, url, fieldnames=None):
	""" Fetches the gforms results page as csv from a published csv link.
		imports it to the jamsite.jammers 
	"""
	# import csv, from the webz.
	csvfile = fetch_csv_from_url(url)
	jamsite.mergeinsert( import_jammers(csvfile, fieldnames=fieldnames) )


def import_from_file(jamsite, source='jammers.csv', fieldnames=None):
	""" Imports from jammers.csv and mergeinserts into jamsite.jammers. """
	# import jammers.csv
	with open(source) as csvfile:
		jamsite.mergeinsert( import_jammers(csvfile, fieldnames=fieldnames) )




def import_all_jammers(sources=[dict(file='jammers.csv')], fieldnames=None):
	""" Handles the details """
	jamsite = JamSite().load().reset()
	
	for source in sources:
		if "url" in source.keys():
			url = source['url']
			fieldnames = gf_fieldnames(source.get('fields', None))
			import_from_url(jamsite, url, fieldnames)
		else:
			file = source.get("file", "Catastrophe")
			fieldnames = gf_fieldnames(source.get('fields', None))
			import_from_file(jamsite, file, fieldnames)
	
	# Add a touch of human decisions.
	jamsite.apply_human()
	return jamsite


def fetch_csv_from_url(url):
	""" Gets a fresh copy of the Google Forms Response file and treats it like a file object. 

		In order for this to work, the response sheet must be published to the web as csv and the link must be put in config.py under the variable gforms_url.
	"""
	
	#cache avoidance.
	with requests_cache.disabled():
		r = requests.get(url)
		if r.status_code == 200:
			return r.iter_lines()



def gf_fieldnames(fn="forms-fields.txt"):
	""" Input a google form mapped fieldnames file, 
		output: better fieldnames for scripting 

		format:
			* one line per fieldname
			* optional better name given with the syntax: 
				<better_fieldname>:<original field name>

	"""
	if fn is None: 
		return None
	with open(fn) as f:
		fieldnames = [fieldname.split(":")[0] for fieldname in f]
		return fieldnames





def import_registered_jammers(filename="jammerskillz.csv"):
	""" Registered jammers are those who have filled out the 

		second form (in BGJ ). They may or may not have a ticket.
	"""
	from utils import gf_fieldnames
	return import_jammers(filename, fieldnames=gf_fieldnames())
