#!/usr/bin/env python
#coding: utf-8
import csv
import re
import picsgetter
import classifier
from template_stuff import style, template, render_skills, render_classifications

# Instantiating our skills classifier, born
# at Pilsner and Programming in Bergen #3 2016.
c = classifier.SkillzClassifier()

with open("jammers.csv") as csvfile:
	jammers = csv.DictReader(csvfile)
	
	with open("jammers.html", "w+") as htmlfile:
		htmlfile.write("<meta charset=\"utf-8\">\n\r %s" % style)
		
		for jammer in jammers:			
			# Classifying the jammer role
			jammer["class"] = "cls_" + c.simply_classify(jammer["Skills"])
			classifications = c.classify(jammer["Skills"])
			jammer["classifications"] = render_classifications(classifications)
			skills_and_labels = c.label_skillset(jammer["Skills"])
			jammer["Allskills"] = render_skills(skills_and_labels)
			#Picture time
			jammer["Picture"] = picsgetter.find_or_create_picture(jammer)
			htmlfile.write( template % jammer )
		
#pedagogics. Yes, python has a webbrowser module built-in. Use it !:)
import webbrowser
webbrowser.open(htmlfile.name)
