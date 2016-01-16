#!/usr/bin/env python
#coding: utf-8
import csv
#coding: utf-8
import picsgetter
import re
import datetime
import classifier

skillz_sensor = classifier.SkillzClassifier()

style = """
	<style>
		.jammer{
			border: 1px dashed gray;
			margin: 10px;
			page-break-after: always;
			border-width: 20px;
			position: relative;
			padding: 40px;
		}

		.jammer:before {
			position: absolute;
			left: 0;
			right: 0;
			top: 0;
			bottom: 0;
			border-width: 10px;
			border-style: solid;
			content: ''; 
		}

		.cls_unclassified { border-color: Cornsilk; }		
		.cls_music { border-color: purple; }		
		.cls_programming { border-color: yellow; }		
		.cls_marketing { border-color: black; }		
		.cls_2d_art { border-color: pink;}		
		.cls_game_design { border-color: green;}		
		.cls_game_development{border-color: orange;}		
		.cls_project_management{border-color: red;}		
		.cls_story_and_narrative{ border-color: orange; }		
		.cls_management{border-color: LightSalmon;}		
		.cls_hardware{ border-color: light-green; }		
		.cls_audio{ border-color: dark-purple;}		
		.cls_web_design{ opacity: 0.3; border-color: blue; }
		


		.cls_unclassified:before { border-color: Cornsilk; }
		.cls_music:before { border-color: purple; }
		.cls_programming:before { border-color: yellow; }
		.cls_marketing:before { border-color: black; }
		.cls_2d_art:before { border-color: pink;}
		.cls_game_design:before { border-color: green;}
		.cls_game_development:before { border-color: orange;}
		.cls_project_management:before { border-color: gray;}
		.cls_story_and_narrative:before { border-color: green;}
		.cls_management:before { border-color: LightSalmon;}
		.cls_hardware:before { border-color: light-green;}
		.cls_audio:before { border-color: dark-gray;}
		.cls_web_design:before { opacity: 0.5; border-color: blue;}
		
		li { list-style: none; display: inline-block; border-radius: 5px; background-color: LightSalmon; padding: 4px; margin: 2px;}

		.licls_Sound{ background-color: Lime;}
		.licls_2D{background-color: yellow;}
		.licls_3D{}
		.licls_Programming{ background-color: blue;}
		.licls_Other{}


		body {
			text-align: center;
		}
		ul {
			margin: 0;
			padding: 0;
		}
		img {
			border-radius: 80px;
			margin: 40px;
		}
		</style>
"""

template = """
	<div class="jammer %(class)s">
		<h2>%(Username)s</h2>
		<h3>%(Full name)s</h3>
		
		<ul>
			%(classifications)s
		</ul>
		
		<img src="%(Picture)s" />
		
		<h3>Skills:</h3>
		<ul>
			%(Allskills)s
		</ul>
	</div>
	"""



with open("jammers.csv") as csvfile:
	jammers = csv.DictReader(csvfile)
	jammers_without_skills = []
	with open("jammers.html", "w+") as htmlfile:
		htmlfile.write("<meta charset=\"utf-8\">\n\r %s" % style)
		
		for jammer in jammers:
			if jammer["Skills"] is not "":

				#CLASSIFYing
				jammer["class"] = "cls_" + skillz_sensor.simply_classify(jammer["Skills"])

				classifications = skillz_sensor.classify(jammer["Skills"])
				classifications = "\n".join(["<li class='licls_%s'>%s</li>" % (lbl, lbl) for lbl in classifications])
				jammer["classifications"] = classifications
				
				Allskills = ""
				for skill in [s.strip() for s in jammer["Skills"].split(",")]:
					try:
						lbl = skillz_sensor.classify(skill).keys()[0]
					except:
						print jammer["Username"], jammer["Skills"]
					
					Allskills += "<li class='licls_%s'>%s</li>" % (lbl, skill)
				
				jammer["Allskills"] = Allskills
				jammer["Picture"] = picsgetter.find_or_create_picture(jammer)
				htmlfile.write( template % jammer )
			else:
				jammers_without_skills.append(jammer)
	print len(jammers_without_skills)



import webbrowser
webbrowser.open(htmlfile.name)


