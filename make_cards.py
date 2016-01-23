#!/usr/bin/env python
#coding: utf-8
import csv
import re
import picsgetter
from picsgetter import username
import classifier
from template_stuff import style, template, render_skills, render_classifications, render_role, render_jammer, render_jammers

from ggj import JamSite, Jammer
from utils import fetch_gforms_csv, gf_fieldnames

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
		# Put it in object yo.
		#try:
		if hasattr(csvfile, "name") and csvfile.name == "jammers.csv":
			# These jammers has registered to the jam site. 
			jammer["ticket"] = True
		jammer = Jammer(**jammer)
		#except:
		#	print("Skipping %s" % jammer)
		#	continue #skip invalid jammers.
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
		for chunk in render_jammers(jammers):
			htmlfile.write(chunk)
	return htmlfile


def import_from_gforms(jamsite):
	""" Fetches the gforms reusults page as csv from a published csv link.
		imports it to the jamsite.jammers 
	"""
	# import gforms, from the webz.
	csvfile = fetch_gforms_csv()
	jamsite.mergeinsert( import_jammers(csvfile, fieldnames=gf_fieldnames()) )


def import_from_ggj(jamsite):
	""" Imports from jammers.csv and mergeinserts into jamsite.jammers. """
	# import jammers.csv
	with open("jammers.csv") as csvfile:
		jamsite.mergeinsert( import_jammers(csvfile) )


def import_all_jammers():
	""" Handles the details """
	jamsite = JamSite().load().reset()
	
	import_from_ggj(jamsite)
	import_from_gforms(jamsite)
	
	# Write it to file.
	jamsite.apply_human()
	return jamsite


def make_cards():
	""" Main function. It will import jammers from jammers.csv, then from google forms and build a card for each. 

		Output - jammers.html 
	"""
	jamsite = import_all_jammers()
	htmlfile = write_jammer_cards(jamsite.jammers.values())

	#pedagogics. Yes, python has a webbrowser module built-in. Use it !:)
	import webbrowser
	webbrowser.open(htmlfile.name)	

if __name__ == '__main__':
	make_cards()
	
