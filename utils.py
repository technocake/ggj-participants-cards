from analyze import load
from picsgetter import username



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
	print load(how_many)
