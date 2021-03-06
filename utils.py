#coding: utf-8
from analyze import load
from picsgetter import username
import requests
import requests_cache

def dict_jammers(list_of_jammers, key="Username", keyformat=username):
	""" Converts a list of jammers to a dict of jammers with key Username (default) """
	jammers = {}
	for jammer in list_of_jammers:
		jammers[keyformat(jammer[key])] = jammer
	return jammers




def find_waiting_people(formjammers, filename, jammers, fieldnames):
		""" Finds jammers waiting for a seat """
		formjammers_full = [jammer for jammer in formjammers]
		
		# List of usernames from both camps
		formjammers = [username(jammer['Username']) for jammer in formjammers_full if username(jammer['Username']) != ""]
		jammers = [username(jammer['Username']) for jammer in jammers]
		

		# Match usernames in both camps
		for signed_up_jammer in jammers:
			if signed_up_jammer in formjammers:
				formjammers.remove(signed_up_jammer)


		#Convert the list of jammers from the google forms to a dict of jammers
		formjammers_dict = dict_jammers(formjammers_full)
		#Fetch full jammer info from the usernames
		waiting_jammers = [formjammers_dict[waiting_jammer] for waiting_jammer in formjammers]
		

		return formjammers, waiting_jammers


def venteliste(jammers, signupfile):
	""" Matches jammers in the ggj provided list of jammers and
		the google forms provided list of jammers """
	
	venteliste = load(find_waiting_people, filename=signupfile, jammers=jammers, fieldnames=gf_fieldnames())


	return venteliste




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
	print( load(venteliste, "jammerskillz.csv")[0] )

	print()
	print( gf_fieldnames() )

	update_formjammers()