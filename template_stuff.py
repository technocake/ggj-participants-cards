role_colors = {
		"unclassified": "Gray",
		"3D": "FireBrick",
		"2D": "Red",
		"Programming": "MidnightBlue",
		"Sound": "Yellow",
		"Other": "Purple"
	}

role_text_colors = {
		"t_unclassified": "Black",
		"t_3D": "Black",
		"t_2D": "Black",
		"t_Programming": "White",
		"t_Sound": "Black",
		"t_Other": "White"
}

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


		.cls_unclassified,
		.cls_unclassified:before { border-color: %(unclassified)s; }
		.cls_Sound, .cls_Sound:before {	border-color:%(Sound)s; }
		.cls_2D, .cls_2D:before { border-color:%(2D)s; }
		.cls_3D, .cls_3D:before { border-color:%(3D)s; }
		.cls_Programming, 
		.cls_Programming:before { border-color:%(Programming)s; }
		.cls_Other, .cls_Other:before {border-color:%(Other)s; }
		 

		li { list-style: none; display: inline-block; border-radius: 5px;  padding: 4px; margin: 2px;}

		.licls_unclassified{ 	
			background-color: %(unclassified)s !important; 
			color: %(t_unclassified)s !important; }
		.licls_Sound{ 	
			background-color: %(Sound)s !important; 
			color: %(t_Sound)s !important; }
		.licls_2D{
			background-color: %(2D)s !important; 
			color: %(t_2D)s !important; }
		.licls_3D{ 		
			background-color: %(3D)s !important; 
			color: %(t_3D)s !important; }
		.licls_Programming{ 
			background-color: %(Programming)s !important; 
			color: %(t_Programming)s !important;}
		.licls_Other{ 
			background-color: %(Other)s !important; 
			color: %(t_Other)s !important; }


		body {
			text-align: center;
			font-family: Arial;
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
""" % dict(list(role_colors.items()) + list(role_text_colors.items()))

template = """
	<div class="jammer %(class)s">
		<h2>%(Username)s</h2>
		<h3>%(Full name)s</h3>
		<p class="experience">%(Experience)s</p>
		<ul>
			%(classifications)s
		</ul>
		<h3>T-shirt size: %(Size)s</h3>
		<img src="%(picture)s" />
		
		<h3>Skills:</h3>
		<ul>
			%(allskills)s
		</ul>
	</div>
	"""

def render_jammer(jammer):
	""" Takes a fully propagated jammer and renders """
	setattr(jammer, "class", render_role(jammer.main_role))
	setattr(jammer, "classifications", render_classifications(jammer.classifications))
	setattr(jammer, "allskills", render_skills(jammer.skills_and_labels))
	if not hasattr(jammer, "Experience"):
		jammer.Experience = ""
	if not hasattr(jammer, "Size"):
		jammer.Size="?"
	return template % jammer.__dict__


def render_jammers(jammers):
	""" assembles this whole thing together """
	yield "<meta charset=\"utf-8\">\n\r %s" % style
	for jammer in jammers:
		yield render_jammer(jammer) 


def render_role(main_role):
	""" Picks the first class. and renders it.  """
	return "cls_" + main_role


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
