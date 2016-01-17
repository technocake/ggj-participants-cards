#coding: utf-8
from analyze import load
from picsgetter import username


def venteliste(jammers, signupfile):
	""" Matches jammers in the ggj provided list of jammers and
		the google forms provided list of jammers """
	
	def find_waiting_people(formjammers, filename, jammers):
		""" Finds jammers waiting for a seat """
		formjammers = [username(jammer['Hva er kontoen din / ditt username på Globalgamejam.org?']) for jammer in formjammers]
		jammers = [username(jammer['Username']) for jammer in jammers]
		
		for signed_up_jammer in jammers:
			if signed_up_jammer in formjammers:
				formjammers.remove(signed_up_jammer)
		return formjammers
	
	venteliste = load(find_waiting_people, filename=signupfile, jammers=jammers)
	return venteliste


def gf_fieldnames(fn="forms-fields.txt"):
	""" Input a google form mapped fieldnames file, 
		output: better fieldnames for scripting 

		format:
			* one line per fieldname
			* optional better name given with the syntax: 
				<better_fieldname>:<original field name>

	"""
	with open(fn) as f:
		fieldnames = []
		for fieldname in f:
			fieldnames.append(fieldname.split(":")[0])
		return fieldnames

def emails(jammers):
	for jammer in jammers:
		print( jammer["Email"])


def whoose_account(jammers, email):
	for jammer in jammers:
		if jammer["Email"] == email:
			print(jammer.values())
			print(username(jammer["Username"]))

def how_many(jammers):
	return len(["" for j in jammers])

if __name__ == '__main__':
	load(whoose_account, "email@participant.com")
	#load(emails)
	print( load(how_many) )
	print( load(venteliste, "jammerskillz.csv") )

	print(username("Hanne Ivarsen"))
	print( gf_fieldnames() )