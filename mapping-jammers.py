from analyze import load
from picsgetter import username


def mapthe(jammers):
	nicks = ["technocake", "torthu"]
	ins = {}
	for i, jammer in enumerate(jammers):
		for nick in nicks:
			if username(nick) == username(jammer["Username"]):
				ins[nick] = 1
		
	return list(ins)
		
	



if __name__ == '__main__':
	load(mapthe)
