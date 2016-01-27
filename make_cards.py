#!/usr/bin/env python
#coding: utf-8
import os
import sys
from template_stuff import render_jammers
from simplify import errormsg, make_minimum_configuration, load_sources, load_extra
from importing import import_all_jammers


def write_jammer_cards(jammers, filename="jammers.html", extra=False):
	""" Serializes """
	with open(filename, "w+") as htmlfile:
		for chunk in render_jammers(jammers, extra):
			htmlfile.write(chunk)
	return htmlfile


def make_cards(sources=[dict(file='jammers.csv')], fieldnames=None, extra=False):
	""" Main function. It will import jammers from jammers.csv, then from google forms and build a card for each jammer. 

		Output - jammers.html 
	"""
	jamsite = import_all_jammers(sources)
	htmlfile = write_jammer_cards(jamsite.jammers.values(), extra=extra)
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
	parser.add_argument('--extra', action='store_true', default=None, 
							help='Add extra information from other sources. Experience and Size fields(Tshirt)')
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
		
		# Add extra fields to rendering.
		if args.extra is None:
			extra = load_extra()
		else:
			extra = True		

	print("""
	Starting to create the jammer cards. importing from %d source(s).

	Have yourself a cup of tea!
	This will take a couple of minutes the first time it is done.
	(Because it takes a while to fetch the profile pictures)
	
	Everything will be cached from now on, 
	and this should take significantly lesser time on subsequent runs ;).

	The generated file will open automatically in your browser when
	completed.
	"""%len(sources))



	try:
		htmlfile = make_cards(sources, extra=extra)
	except IOError as e:
		print("\n\r"*40)
		print(errormsg["missing_jammers_file"])
		sys.exit(1)

	#pedagogics. Yes, python has a webbrowser module built-in. Use it !:)
	print(""" Done """)
	webbrowser.open(htmlfile.name)