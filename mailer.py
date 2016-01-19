import smtplib
#coding: utf-8 

ticket_offer_from_waiting_list = """

	Hei %(Full Name)s ! Gratulerer med plass på Bergen Game Jam!

	Du har stått på venteliste, og nå har vi akkurat funnet en ledig plass til deg. 

	For at vi skal kunne melde deg inn må du ha en Global Game Jam Konto.
	Har du ikke det kan du lage det her.
	http://globalgamejam.org/user/signup/to/participate/using
	
	Vi ser at du har oppgitt %(Username)s som kontonavn. 


	Send oss ditt kontonavn så skal vi få meldt deg på!
	

	Vi gleder oss til å møte deg på Bergen Game Jam 2016!


"""

subject_ticket_offer_from_waiting_list = "Gratulerer med plass fra ventelisten til BGJ16!"

def mail(message, jammer):
	""" Mails a jammer with the given message """
	
	return message % dict(jammer)


def send_mail(to, subj, msg):

	from config import gmail_pwd, gmail_account
	fromaddr = gmail_account
	toaddrs  = to
	print( to )


	# Credentials (if needed)
	username = gmail_account
	password = gmail_pwd
	
	msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % ( fromaddr, toaddrs, subj, msg )


	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()




def grant_tickets():
	from utils import venteliste
	from analyze import load

	usernames, jammers = load(venteliste, "jammerskillz.csv")
	#print( [jammer["Email"] for jammer in jammers])
	
	for jammer in jammers:
		msg = mail(ticket_offer_from_waiting_list, jammer)
		send_mail(jammer["Email"], subject_ticket_offer_from_waiting_list, msg)


if __name__ == '__main__':
	#grant_tickets()
	#print (mail(ticket_offer_from_waiting_list, )
	import webbrowser
	webbrowser.open("https://www.google.com/settings/security/lesssecureapps")
	

