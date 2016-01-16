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
		.licls_Programming{ background-color: AliceBlue;}
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


def render_classifications(classifications):
	""" Renders a list with css classes for the classificatiopns 
		of a participant
	"""
	return "\n".join(["<li class='licls_%s'>%s</li>" % (lbl, lbl) for lbl in classifications])


def render_skills(skills_and_labels):
	"""
		Renders the list of skills with stylized classes.
	"""
	rendered_list = []
	for lbl, skill in skills_and_labels:		
		rendered_list.append("<li class='licls_%s'>%s</li>" % (lbl, skill))
	return "\n".join(rendered_list)
