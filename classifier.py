#coding: utf-8

class SkillzClassifier():
	skillset = "3d art,  animation,  audio,  game design,  game development,music,  programming,  project management,  story and narrative, 2d art, quality assurance, hardware, writing, marketing, web design, management"

	groups = {
		"3D": ["3d art"],
		"2D": ["2d art"],
		"Programming": ["game development", "programming", "hardware", 
						"web design"],
		"Sound": ["music", "audio"],
		"Other": ["game design", "writing", "story and narrative", "project management", "marketing", "quality assurance", "management", "animation"]
	}
	
	
	def simply_classify(self, text):
		""" Herlig naiivt". """
		skillz = text.split(",")
		if len(skillz) == 1:
			return self.cssname(skillz[0])
		else:
			return "unclassified"


	def classify(self, text):
		"""Group membership classification"""
		labels = {}
		if text == "":
			labels["unclassified"] = 1
		skillz = self.parse_skills(text)
		for skill in skillz:
			for group in self.groups:
				if skill in self.groups[group]:

					if group not in labels:
						labels[group] = 1
					else:
						labels[group] += 1

		return labels


	def parse_skills(self, text):
		""" string with comma separated skills --> list of skills. """
		return [s.strip() for s in text.split(",")]


	def label(self, skill):
		""" labels a single skill from the classifier 
			see self.groups for mappings.
		"""
		return list(self.classify(skill))[0]


	def label_skillset(self, text):
		""" Process and classify skills individually. """
		skills = self.parse_skills(text)
		skills_and_labels = [(self.label(skill), skill) for skill in skills]
		return skills_and_labels

	def cssname(self, classstr):
		""" 2d art -> 2d_art """
		return classstr.replace(" ", "_")


if __name__ == '__main__':
	c = SkillzClassifier()
	print(c.classify("programming, h"))
	
	print(c.classify("2d art"))
	print(c.classify(""))
	


	print(c.classify("audio, hardware, marketing, music, programming, project management, web design"))