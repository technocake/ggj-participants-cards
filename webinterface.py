from flask import Flask, request, Response, redirect, url_for, render_template

from make_cards import import_all_jammers
from ggj import JamSite, Jammer
from template_stuff import render_jammers

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/import")
def import_jammers():
	jamsite = import_all_jammers()
	jamsite.save()
	return "Imported. Remember to have a fresh version of jammers.csv from ggj.org in this folder. put it in this folder."


@app.route("/cards")
def cards():
	jamsite = JamSite.load()
	jamsite.apply_human()
	return Response(render_jammers(jamsite.jammers.values()))


@app.route("/jammer/update")
def update_jammer():
	""" updates a jammer """
	d = request.args
	#hehehehehe. but it works. 
	jammer = Jammer(**dict((k, str(d[k])) for k in list(d.keys())))
	
	jamsite = JamSite.load()
	jamsite.administrated_jammers[jammer.username] = jammer
	#jamsite.jammers[jammer.username] = jamsite.jammers[jammer.username].update(jammer)
	jamsite.save()
	return "<p>".join(list(jammer.__dict__.values()))

if __name__ == '__main__':
	import webbrowser
	#webbrowser.open("http://localhost:5000")
	app.run(debug=True)