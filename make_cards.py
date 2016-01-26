#!/usr/bin/env python
#coding: utf-8
import csv
import re
import picsgetter
from picsgetter import username
import classifier
from template_stuff import style, template, render_skills, render_classifications, render_role, render_jammer, render_jammers

from ggj import JamSite, Jammer
from utils import fetch_csv_from_url, gf_fieldnames

# Instantiating our skills classifier, born
# at Pilsner and Programming in Bergen #3 2016.
c = classifier.SkillzClassifier()

def make_invitation_mail(jammer):
	from mailer import invitation_message
	return u"To: %(Email)s" % jammer, invitation_message(jammer.__dict__)


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


def import_registered_jammers(filename="jammerskillz.csv"):
	""" Registered jammers are those who have filled out the 

		second form (in BGJ ). They may or may not have a ticket.
	"""
	from utils import gf_fieldnames
	return import_jammers(filename, fieldnames=gf_fieldnames())


def write_jammer_cards(jammers, filename="jammers.html"):
	""" Serializes """
	with open(filename, "w+") as htmlfile:
		for chunk in render_jammers(jammers):
			htmlfile.write(chunk)
	return htmlfile


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

def load_sources():
		""" Will attempt to load sources from config,
			if config doesn't existt; 
				returns default
		"""
		try:
			import config
			sources = getattr(config, "sources", [dict(file='jammers.csv')])
		except:
			sources = [dict(file='jammers.csv')]
		return sources


def make_cards(sources=[dict(file='jammers.csv')], fieldnames=None):
	""" Main function. It will import jammers from jammers.csv, then from google forms and build a card for each jammer. 

		Output - jammers.html 
	"""
	jamsite = import_all_jammers(sources)
	htmlfile = write_jammer_cards(jamsite.jammers.values())
	return htmlfile


if __name__ == '__main__':
	import argparse
	import webbrowser

	parser = argparse.ArgumentParser(description="""
		Bergen Game Jam Card Maker.

		A program that will create a printable html file with a card for
		all the jammers in a global gamejam site. 
		
		by default it will look for the file: jammers.csv in this directory.
		""")
	parser.add_argument('sources', metavar='S', type=str, nargs='*',
							default='',	
							help='Sources of jammer info in csv format. Either files or urls. If none provided, default is jammers.csv')
	parser.add_argument('--fields', metavar='FIELDNAMES_FILE', type=str, 
							help='NOT IMPLEMENTED YET.Optionally you can give a file with fieldnames mappings for the source. ')
	args = parser.parse_args()
	# Load source from args
	if type(args.sources) is list:
		sources = []
		for source in args.sources:
			if "http" in source:
				#foo hack to guess if fields is given, it belongs to an external source.
				sources.append(dict(url=source, fields=args.fields))

			else:
				sources.append(dict(file=source))
	else:
		# Load sources from config, if that fails, default.
		sources = load_sources()
	

	fieldnames=gf_fieldnames()
	htmlfile = make_cards(sources)
	#pedagogics. Yes, python has a webbrowser module built-in. Use it !:)
	webbrowser.open(htmlfile.name)	
	
