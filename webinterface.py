from flask import Flask, request, Response, redirect, url_for, render_template, flash
from werkzeug import secure_filename

from make_cards import import_all_jammers
from ggj import JamSite, Jammer
from template_stuff import render_jammers, render_editable_jammers, render_waiting_list
import classifier


app = Flask(__name__)
app.config.from_object('config')
if "WEBROOT" in app.config:
	import os
	os.chdir(app.config["WEBROOT"])


edit_jammer_ui = "\n\r".join(["<a class='update' href='{url}?Username=%(Username)s&main_role={role}'>Change to {role}</a>".format(role=role, url='{url}') for role in classifier.groups])


@app.route("/")
def index():
	jamsite = JamSite.load()
	jamsite.apply_human()
	return render_template("index.html", jamsite=jamsite)


@app.route("/import")
def import_jammers():
	try:
		jamsite = import_all_jammers()
		jamsite.save()
		flash("Imported. Remember to have a fresh version of jammers.csv from ggj.org in this folder. put it in this folder.")
		return redirect(url_for('index'))
	except:
		import traceback
		import os
		return "<h1>not worky\n\r</h1><p>"+traceback.format_exc()+"</p>"\
			+ os.getcwd()

@app.route("/print/cards")
def cards():
	""" Renders cards for all jammers with a ticket """
	jamsite = JamSite.load()
	jamsite.apply_human()
	return Response(render_jammers(jamsite.jammers_sorted_by_main_role(with_ticket=True)))


@app.route("/cards")
def editable_cards():
	""" Renders cards for all jammers with a ticket , and lets them be edited."""
	jamsite = JamSite.load()
	jamsite.apply_human()
	return Response(render_editable_jammers(jamsite.jammers_with_ticket, ui=edit_jammer_ui.format(url=url_for('update_jammer'))))


@app.route("/waiting-list")
def waiting_list():
	jamsite = JamSite.load()
	jamsite.apply_human()
	return render_waiting_list(jamsite.waiting_list())


@app.route("/cards/all")
def all_cards():
	""" Renders cards for all known about jammers associated with this site.
		ticekt holders and waiting list jammers """
	jamsite = JamSite.load()
	jamsite.apply_human()
	return Response(render_jammers(jamsite.jammers.values()))


@app.route("/reset")
def reset():
	try:
		jamsite = JamSite.load()
		jamsite.reset(all=True)
		jamsite.save()
		flash("Hard reset performed.")
		return redirect(url_for('index'))
	except:
		import traceback
		return "<pre>"+traceback.format_exc()+"</pre>"


def allowed_file(filename):
	return filename.split(".")[-1] in ["csv"]


@app.route("/upload/jammers.csv", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
	try:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = 'jammers.csv'
                file.save(filename)
                flash('Uploaded %s' % filename)
                return redirect(url_for('index'))
        except:
            import traceback
            return filename + "<pre>" + traceback.format_exc() + "</pre>"
    import config
    ggj_url = config.ggj_url if hasattr(config, 'ggj_url') else ""
    return render_template('upload-file.html', ggj_url=ggj_url)



	
@app.route("/jammer/update")
def update_jammer():
	""" updates a jammer """
	d = request.args
	#hehehehehe. but it works. 
	jammer = Jammer(**dict((k, str(d[k])) for k in list(d.keys())))
	#jammer.accumulate()
	jamsite = JamSite.load()
	jamsite.administrated_jammers[jammer.username] = jammer
	#jamsite.jammers[jammer.username] = jamsite.jammers[jammer.username].update(jammer)
	jamsite.save()
	## Flash (OK). not necessary actually.
	return redirect(url_for('editable_cards') + '#' + jammer.username)


if __name__ == '__main__':
	import webbrowser
	webbrowser.open("http://localhost:5000")
	app.run(debug=True)
