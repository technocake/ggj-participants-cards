import classifier
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
		/*
		  Well, turns out a :before element will cover the entire main element. Not doing something uselful. Just blocking it. 
		  So lets move it behind in the z-stack.
		*/

		::before { z-index: -1337; }
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

		.ui {
			position: absolute;
			right: 20px;
			display: inline-block;
			float: right;
		}
		.ui::after {clear:both;}

		.update { display: block; padding: 15px; border: 1px solid black;}

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
		

		<style type="text/css" media="print">
			@page {
			    size: auto;   /* auto is the initial value */
			    margin: 0;  /* this affects the margin in the printer settings */
			}
		</style>

""" % dict(list(role_colors.items()) + list(role_text_colors.items()))


page_head = """<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Jammers</title>
	%(style)s
</head>
<body>
""" % dict(style=style)


page_footer = """
</body>
</html>
"""






template = """
	<div class="jammer %(class)s" id="%(username)s">
		<div class='ui'>%(ui)s</div>
		<h2>%(Username)s</h2>
		<h3>%(Full name)s</h3>
		<ul>
			%(classifications)s
		</ul>
		<img src="%(picture)s" />
		
		{Extra}
		
		<h3>Skills:</h3>
		<ul>
			%(allskills)s
		</ul>
	</div>
	"""


extra_template = """
<h3>T-shirt size: %(Size)s</h3>
		<p class="experience">%(Experience)s</p>
		<h4>Education:</h4> %(Education)s
"""


def render_jammer(jammer, extra=False):
	""" Takes a fully propagated jammer and renders """
	setattr(jammer, "class", render_role(jammer.main_role))
	setattr(jammer, "classifications", render_classifications(jammer.classifications))
	setattr(jammer, "allskills", render_skills(jammer.skills_and_labels))
	if not hasattr(jammer, "Experience"):
		jammer.Experience = ""
	if not hasattr(jammer, "Size"):
		jammer.Size="?"
	if not hasattr(jammer, "Education"):
		jammer.Education=""
	if not hasattr(jammer, "ui"):
		jammer.ui=""
	setattr(jammer, "username", jammer.username)
	if extra:
		# Optionally add more info from other sources 
		return template.format(Extra=extra_template%jammer) % jammer
	return template.format(Extra="") % jammer.__dict__


def render_jammers(jammers, extra=False):
	""" assembles this whole thing together """
	yield page_head
	for jammer in jammers:
		yield render_jammer(jammer, extra)
	yield page_footer


def render_editable_jammers(jammers, ui, extra=False):
	""" assembles this whole thing together, adds UI for admin """
	yield page_head
	for jammer in jammers:
		yield render_editable_jammer(jammer, ui, extra) 	
	yield page_footer


def render_editable_jammer(jammer, ui, extra=False):
	""" 
		Adds UI for the admin to edit a jammer card 
	"""
	jammer.ui = render_ui(ui, jammer)
	return render_jammer(jammer, extra)

def render_ui(ui, jammer):
	return ui % jammer


def render_waiting_list(waiting_jammers):
	out = "<h1> Waiting list: </h1><ol>"
	for jammer in waiting_jammers:
		setattr(jammer, "username", jammer.username)
		out += "<li> <a href='http://globalgamejam.org/users/%(username)s' target='_blank'>%(Username)s</a> - %(Email)s</li>" % jammer
	out += "</ol>"
	return out


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
