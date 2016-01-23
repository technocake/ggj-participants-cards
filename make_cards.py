#!/usr/bin/env python
#coding: utf-8
import csv
import re
import picsgetter
from picsgetter import username
import classifier
from template_stuff import style, template, render_skills, render_classifications, render_role, render_jammer

from ggj import JamSite, Jammer
from utils import fetch_gforms_csv, gf_fieldnames

# Instantiating our skills classifier, born
# at Pilsner and Programming in Bergen #3 2016.
c = classifier.SkillzClassifier()


def import_jammers(csvfile, fieldnames=None):
	"""
		Imports jammer info from jammers.csv 
		it will perform classification and picture (url) fetching
		returns a list of Jammer objects with propagated fields.
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
		# Put it in object yo.
		try:
			if hasattr(csvfile, "name") and csvfile.name == "jammers.csv":
				# These jammers has registered to the jam site. 
				jammer["ticket"] = True
			jammer = Jammer(**jammer)
		except:
			continue #skip invalid jammers.
		#print(jammer.username, filename)			
		# Crunch a little on this jammer.
		#jammer.accumulate()
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
			htmlfile.write("<meta charset=\"utf-8\">\n\r %s" % style)
			for jammer in jammers:
				htmlfile.write( render_jammer(jammer) )
	return htmlfile


def import_from_gforms():
	""" Fetches the gforms reusults page as csv from a published csv link.
		imports it to the jamsite.jammers 
	"""
	# import gforms, from the webz.
	fetch_gforms_csv()
	csvfile = fetch_gforms_csv()
	jamsite.mergeinsert( import_jammers(csvfile, fieldnames=gf_fieldnames()) )


if __name__ == '__main__':
	
	jamsite = JamSite()
	# import jammers.csv
	with open("jammers.csv") as csvfile:
		jamsite.mergeinsert( import_jammers(csvfile) )

	import_from_gforms()
	# Write it to file.
	htmlfile = write_jammer_cards(jamsite.jammers.values())
	print (jamsite.waiting_list())

	#pedagogics. Yes, python has a webbrowser module built-in. Use it !:)
	import webbrowser
	webbrowser.open(htmlfile.name)
