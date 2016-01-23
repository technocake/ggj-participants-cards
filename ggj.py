#!/usr/bin/env python
#coding: utf-8
import picsgetter
import classifier
from collections import OrderedDict

# Instantiating our skills classifier, born
# at Pilsner and Programming in Bergen #3 2016.
c = classifier.SkillzClassifier()


class JamSite():
	jammers = OrderedDict()


	def mergeinsert(self, other_list_of_jammers):
		""" Merging a list with additional / overlapping jammer info """
		for jammer in other_list_of_jammers:
			if jammer in self.jammers:
				# overwriting new data
				self.jammers[jammer.username].update(jammer)
				self.jammers[jammer.username].accumulate()
				#self.jammers[jammer.username] = jammer
			else:
				self.jammers[jammer.username] = jammer.accumulate()


	def waiting_list(self):
		""" Goes over all jammers, and returns those without a ticket """
		wait_list = []
		for jammer in self.jammers.values():
			if not jammer.has_ticket:
				wait_list.append(jammer)
		return wait_list


class Jammer():
	def __init__(self, **kwargs):
		""" populates itself from kwargs """
		self.Experience = ""
		
		if 'Username' not in kwargs:
			print("Missing Username field")
			raise Exception
		for key in kwargs:
			value = kwargs[key]
			setattr(self, key, value)


	def __repr__(self):
		return self.username
	

	def __hash__(self):
		""" Used for comparison with other jammers. normalized username is the hash. """
		return hash(self.username)


	def __eq__(self, other):
		""" hmmm. using hash or not. that is the question """
		try:
			return self.username == other.username
		except:
			return self.username == other


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
		# Step 2, accumulate info
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


if __name__ == '__main__':
	j = Jammer(Username="Technocake")
	print(j.Username, j.username)
	j.update(Jammer(Username='Technocake', Skills="music, programming, music"))