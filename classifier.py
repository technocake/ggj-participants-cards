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
			return self.format_ting_Til_skikkelig_format_her(skillz[0])
		else:
			return "unclassified"


	def classify(self, text):
		"""Group membership classification"""
		labels = {}
		skillz = [s.strip() for s in text.split(",")]
		for skill in skillz:
			for group in self.groups:
				if skill in self.groups[group]:

					if group not in labels:
						labels[group] = 1
					else:
						labels[group] += 1

		return labels


	def format_ting_Til_skikkelig_format_her(self, classstr):
		""" 2d art -> 2d_art """
		return classstr.replace(" ", "_")


if __name__ == '__main__':
	c = SkillzClassifier()
	print c.classify("programming, h")
	print c.classify("programming")
	print c.classify("2d art")
	print c.classify("programming")


	print c.classify("audio, hardware, marketing, music, programming, project management, web design")