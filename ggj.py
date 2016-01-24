#!/usr/bin/env python
#coding: utf-8
import picsgetter
import classifier
from collections import OrderedDict
try:
	import cPickle as cpickle
except:
	import cpickle

# Instantiating our skills classifier, born
# at Pilsner and Programming in Bergen #3 2016.
c = classifier.SkillzClassifier()


class JamSite():
	def __init__(self):
		self.jammers = OrderedDict()
		# computer says no, human says yes.
		# This is a list of human made overriding changes
		# per jammer. It will be applied last in the 
		# import cascade, and thus have the highest priority.
		self.administrated_jammers = OrderedDict()


	def mergeinsert(self, other_list_of_jammers, accumulate=True):
		""" Merging a the jamsites jammers with additional / overlapping jammer info """
		for jammer in other_list_of_jammers:
			if jammer in self.jammers:
				# overwriting new data
				self.jammers[jammer.username].update(jammer)
			else:
				self.jammers[jammer.username] = jammer
			if accumulate:	
				# Learn some more about this jammer now with this 
				# new knowledge
				self.jammers[jammer.username].accumulate()


	def apply_human(self):
		""" Last step is to overwrite with human changes """
		self.apply_human_decissions(self.administrated_jammers.values())


	def apply_human_decissions(self, list_of_jammers):
		self.mergeinsert(list_of_jammers, accumulate=False)



	def waiting_list(self):
		""" Goes over all jammers, and returns those without a ticket """
		wait_list = []
		for jammer in self.jammers.values():
			if not jammer.has_ticket:
				wait_list.append(jammer)
		return wait_list

	@property
	def jammers_with_ticket(self):
		return [j for j in self.jammers.values() if j.has_ticket]


	def save(self, filename="jamsite.pickle"):
		""" sideeffects """
		with open(filename, "wb") as statefile:
			cpickle.dump(self, statefile)


	def serialize(self):
		"""used to store state """
		return cpickle.dumps(self)


	@staticmethod
	def load(filename="jamsite.pickle"):
		""" sideeffects """
		with open(filename, "rb") as statefile:
			jamsite = cpickle.load(statefile)
			#self.jammers = jamsite.jammers
			#self.administrated_jammers = jamsite.administrated_jammers
		return jamsite


	def reset(self, all=False):
		""" Empties the jammer list, but keeps the human made changes """
		self.jammers = OrderedDict()
		if all:
			self.administrated_jammers = OrderedDict()
		return self


class Jammer():
	__docstring__ = """ Jammer class, must have Username as a minimum. """
	def __init__(self, **kwargs):
		""" populates itself from kwargs """
		#self.Experience = ""
		#self.Size = "?"
		if 'Username' not in kwargs:
			print("Missing Username field")
			raise Exception
		for key in kwargs:
			value = kwargs[key]
			setattr(self, key, value)




	@property
	def username(self):	
		""" Property and static hack to just keep it procedural. why not."""
		return Jammer.format_username(self.Username)
	

	@property
	def has_ticket(self):
	    return hasattr(self, "ticket") and self.ticket == True
	
	
	def update(self, updated_jammer):
		"""
			When agregating data from multiple sources, this
			algorithm goes through the new data, adds fields not found
			and overwrites old fields with the new version 
		"""
		# Step 1, add or overwrite with updated data
		for key in updated_jammer.__dict__:
			self.__dict__[key] = updated_jammer.__dict__[key]
		return self


	@staticmethod
	def format_username(Username):
		""" 
			1. FB-registered users has a little twitchy nicky thingy
			basically Name Surname => name-surname 

			2. all usernames are lowercased in the url
			3. _ is allowed but stripped from the username in the url.
			4. sometimes there are leading / trailing spaces in input. feush
		"""
		return Username.strip().lower().replace("_", "").replace(" ", "-")


	def accumulate(self):
		"""
			Get more data from the data about this jammer.
		"""
		# Classify skills.
		self.classifications = c.classify(self.Skills)
		self.main_role = c.main_role(self.Skills)
		self.skills_and_labels = c.label_skillset(self.Skills)
		# Profile picture
		self.picture = picsgetter.find_or_create_picture(self.__dict__)
		return self


	def __repr__(self):
		return self.username
	

	def __hash__(self):
		""" Used for comparison with other jammers. normalized username is the hash. """
		return hash(self.username)


	def __getitem__(self, key):
		""" Use the jammer as a dict :) """
		return getattr(self, key)


	def __eq__(self, other):
		""" hmmm. using hash or not. that is the question """
		try:
			return self.username == other.username
		except:
			# explanation. it compares itself with a string username.
			# return self.username == other
			# hack to make it possible to compare keys in a dict of jammers
			# with a jammer object.
			return self.username == other


if __name__ == '__main__':
	j = Jammer(Username="Technocake")
	print(j.Username, j.username)
	j.update(Jammer(Username='Technocake', Skills="music, programming, music"))