#coding: utf-8
import csv

def load(f, *args, **kwargs):
	with open("jammers.csv") as csvfile:
		jammers = csv.DictReader(csvfile)	
		return f(jammers, *args, **kwargs)


def distribution(jammers):
	dist = {}

	for jammer in jammers:
		if jammer["Skills"] is not "":
			k = str(len(jammer["Skills"].split(","))) + " skills"
			if k not in dist:
				dist[k] = 1
			else:
				dist[k] += 1
	return dist

def combination_distribution(jammers):
	# Code written while under the influence of 
	# Imperial Stout, 3 Bean stout
	dist = {}

	for jammer in jammers:
		if jammer["Skills"] is not "":
			k = ", ".join(sorted(jammer["Skills"].split(",")))
			if k not in dist:
				dist[k] = 1
			else:
				dist[k] += 1
	return dist


def dist_of_each(jammers):
	dist = {}
	skillset = "3d art,  animation,  audio,  game design,  game development,music,  programming,  project management,  story and narrative, 2d art, quality assurance, hardware, writing, marketing, web design, management".split(",")
	for jammer in jammers:
		for kk in skillset:
			if jammer["Skills"] is not "":
				k = kk.strip()
				
				if k in [j.strip() for j in jammer["Skills"].split(",")]:
					if k not in dist:
						dist[k] = 1
					else:
						dist[k] += 1
	return dist


def animation_and(jammers):
	dist = {"2d art": 0, "3d art": 0, "None": 0, "Both": 0}
	jammers_with_animation = []
	for jammer in jammers:
		skills = [s.strip() for s in jammer["Skills"].split(",")]
		if "animation" in skills:
			jammers_with_animation.append(jammer)

	for jammer in jammers_with_animation:
		skills = [jj.strip() for jj in jammer["Skills"].split(",")]
		
		if "2d art" in skills:
			dist["2d art"] += 1
		if "3d art" in skills:
			dist["3d art"] += 1
		if not "3d art" in skills and not "2d art" in skills:
			dist["None"] +=1
		if "2d art" in skills and "3d art" in skills:
			dist["Both"] +=1

	return dist 


if __name__ == '__main__':
	print load(distribution)
	print 
	print load(dist_of_each)
	print load(animation_and)

#	combos = load(combination_distribution)
#	for combo in combos:
#		print combos[combo], "::::::::", combo