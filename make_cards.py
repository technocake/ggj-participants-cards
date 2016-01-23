#!/usr/bin/env python
#coding: utf-8
import csv
import re
import picsgetter
from picsgetter import username
import classifier
from template_stuff import style, template, render_skills, render_classifications, render_role, render_jammer

from ggj import JamSite, Jammer

# Instantiating our skills classifier, born
# at Pilsner and Programming in Bergen #3 2016.
c = classifier.SkillzClassifier()


def import_jammers(filename="jammers.csv", fieldnames=None):
	"""
		Imports jammer info from jammers.csv 
		it will perform classification and picture (url) fetching
		returns a list of Jammer objects with propagated fields.
	"""
	parsed_jammers = []
	with open(filename) as csvfile:
		if fieldnames is None:
			# Read fieldnames from first line of csvfile.
			jammers = csv.DictReader(csvfile) 
		else:
			# Fieldnames provided
			jammers = csv.DictReader(csvfile, fieldnames)
			# Skip header line/fieldnames line
			next(jammers)
		for jammer in jammers:
			# Put it in object yo.
			if filename == "jammers.csv":
				# These jammers has registered to the jam site. 
				jammer["has_ticket"] = True
			jammer = Jammer(**jammer)
			#print(jammer.username, filename)			
			# Crunch a little on this jammer.
			jammer.accumulate()
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


if __name__ == '__main__':
	jamsite = JamSite()
	jamsite.mergeinsert( import_jammers("jammers.csv") )
	jamsite.mergeinsert( import_registered_jammers() )

	htmlfile = write_jammer_cards(jamsite.jammers.values())
	#pedagogics. Yes, python has a webbrowser module built-in. Use it !:)
	import webbrowser
	webbrowser.open(htmlfile.name)
