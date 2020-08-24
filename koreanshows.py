from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pickle
import sys
import datetime
import time
import operator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def actor_input():	#stores user input into variable called actor name
	actor_name = input("Please input an actor's name: ")
	actor_name = actor_name.upper()
	return actor_name

def date_input():	#stores user input into variable called date
	date = input("Please input a year: ")
	return date

def preference_input(): #stores user input into list variable called actor_preference_list
	actor_pref_list = []
	actor_preference = input("Please input an actor's name: ")
	actor_preference = actor_preference.upper()
	actor_preference_database = open("actor_preference_database.txt", "a")
	actor_preference_database.write("%s,"%actor_preference)
	with open("actor_preference_database.txt", "r") as actor_preference_database: 
		actor_pref_list = actor_preference_database.read().strip().split(",")
	return actor_pref_list

def new_shows(): #function to find new shows
	current_date = datetime.date.today().strftime("%Y,%m,%d")
	return current_date

def find_shows_given_actor(actor_dict, search_actor, date_dict):
	shows_actor_is_in = {}
	for key, value in actor_dict.items():
		if search_actor in value:
			shows_actor_is_in[(str(key).replace("\n      ","").replace("\n", ""))] = date_dict[key]
	return shows_actor_is_in

def find_shows_given_date(date_dict, search_date):
	shows_by_date = []
	for key, value in date_dict.items():
		if search_date in value: 
			shows_by_date.append(str(key).replace("\n      ","").replace("\n", ""))
	return shows_by_date

def find_new_shows_with_preffered_actors(list_of_new_shows, actor_dict, actor_pref, date_dict):
	relevant_shows = {}
	for key, value in actor_dict.items(): 
		if str(key).replace("\n      ","").replace("\n", "") in list_of_new_shows:
			for actor in actor_pref:
				if actor in value:
					if str(key).replace("\n      ","").replace("\n", "") not in relevant_shows:
						relevant_shows[(str(key).replace("\n      ","").replace("\n", ""))] = date_dict[key], actor
	return relevant_shows
					
def find_new_shows(date_dict, current_search_date):
	new_shows_out = []
	year, month, day = current_search_date.split(",")
	for key, value in date_dict.items(): 
		if year in value: 
			if int(value[len(value)-10 : len(value)-8]) >= int(month):
					new_shows_out.append(str(key).replace("\n      ","").replace("\n", ""))
	return new_shows_out

def notification_via_email(new_show_update):
	fromaddr = "SENDING_FROM_THIS_EMAIL_ADDRESS"
	toaddr = "SENDING_TO_THIS_EMAIL_ADDRESS"
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Korean Drama Updates"
	body = "\n%s"%new_show_update
	msg.attach(MIMEText(body, 'plain'))

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "EMAIL_PASSWORD_HERE")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	print("Email sent")

def fetch_data():
	show_actor_database = {}
	show_date_database = {}

	for z in range(1,35):
		show_page = "https://www.viki.com/explore?country=korea&page={}".format(z)
		#bypass security -- creates fake user
		user_agent = {"Mozilla/5.0"}
		#change url shows_page into html
		req = Request(show_page, headers={'User-Agent': user_agent})
		page = urlopen(show_page )

		#parse page it with beautiful soup
		soup = BeautifulSoup(page, 'html.parser')
		#find all show titles
		show_list = soup.find_all('a', attrs={"class": "thumb-title strong"})

		#create a list to store all show titles and urls
		show_titles = []
		show_links = []
		for x in range(len(show_list)):
			actors = []
			#make list of show titles
			show_titles.append(show_list[x].get_text().upper().replace(u"\u2019", "'"))
			print(show_titles[x])
			#get show links
			show_links.append(show_list[x].attrs['href'])
			
			#broadcast period
			individual_show = "https://www.viki.com{}".format(show_links[x])
			#change url shows_page into html
			req = Request(show_page, headers={'User-Agent': user_agent})

			page1 = urlopen(individual_show)

			#parse page it with beautiful soup
			soup = BeautifulSoup(page1, 'html.parser')
			#find show broadcast period and return it 
			text_block = soup.find_all('dl', attrs={"class": "dl-horizontal"})
			new = str(text_block).split("\\n")
			dates = 00-00-0000
			for i in range(len(new)-1):
				if new[i].find("<dt>Broadcast Period</dt>") != -1:
					dates = new[i+1].replace("<dd>", "").replace("</dd>", "")
			#establish dictionary with the title as a key and date as the value 
			show_date_database[show_titles[x]] = dates
			
			#actors
			individual_show_actors = "https://www.viki.com{}#modal-casts".format(show_links[x])
			#change url shows_page into html
			req = Request(show_page, headers={'User-Agent': user_agent})
			page2 = urlopen(individual_show_actors)

			#parse page it with beautiful soup
			soup = BeautifulSoup(page2, 'html.parser')
			#find all the actor names
			show_actor_list = soup.find_all('span', attrs={"itemprop": "name"})
			#get all the actors from one show
			for y in range(len(show_actor_list)): 
				actors.append(show_actor_list[y].get_text().upper())
			#establish dictionary with the title as a key and actor list as the value 
			show_actor_database[show_titles[x]] = actors


		print("Page number: {}".format(z))
	#create pickle file for show_date_database
	show_date_database_pkl = open("show_date_database.pkl", "wb")
	pickle.dump(show_date_database, show_date_database_pkl)
	show_date_database_pkl.close()

	#create pickle file for show_actor_database
	show_actor_database_pkl = open("show_actor_database.pkl", "wb")
	pickle.dump(show_actor_database, show_actor_database_pkl)
	show_actor_database_pkl.close()

def user_input():
	actor_preference_list = []
	repeat = True
	while repeat == True: 
		print("1. Search for an actor \n2. Search for shows by date \n3. Enter actors you like \n4. Search for new shows \n5. Send an update email \n6. Exit from this menu\n")
		menu_choice = input("Please input a number from the menu: ")
		print ("\n")
		if menu_choice == "1": 
			actor_name = actor_input()
			show_actor_database_pkl = pickle.load(open("show_actor_database.pkl", "rb"))
			show_date_database_pkl = pickle.load(open("show_date_database.pkl", "rb"))
			actor_check = find_shows_given_actor(show_actor_database_pkl, actor_name, show_date_database_pkl)
			print("\n")
			for show, date in actor_check.items():
				print(show, date)
			break
		if menu_choice == "2": 
			date = date_input()
			show_date_database_pkl = pickle.load(open("show_date_database.pkl", "rb"))
			date_check = find_shows_given_date(show_date_database_pkl, date)
			print("\n")
			for show in date_check:
				print(show)
			break
		if menu_choice == "3": 
			actor_preference_database = preference_input()
			current_date = new_shows()
			show_date_database_pkl = pickle.load(open("show_date_database.pkl", "rb"))
			current_shows = find_new_shows(show_date_database_pkl, current_date)
			show_actor_database_pkl = pickle.load(open("show_actor_database.pkl", "rb"))
			actor_pref_check = find_new_shows_with_preffered_actors(current_shows, show_actor_database_pkl, actor_preference_database, show_date_database_pkl)
			print ("\n")
			for show, date in actor_pref_check.items():
				print(show, date)
			break
		if menu_choice == "4": 
			current_date = new_shows()
			show_date_database_pkl = pickle.load(open("show_date_database.pkl", "rb"))
			new_show_check = find_new_shows(show_date_database_pkl, current_date)
			print("\n")
			for show in new_show_check:
				print(show)
			break
		if menu_choice == "5":
			actor_preference_database = preference_input()
			current_date = new_shows()
			show_date_database_pkl = pickle.load(open("show_date_database.pkl", "rb"))
			current_shows = find_new_shows(show_date_database_pkl, current_date)
			show_actor_database_pkl = pickle.load(open("show_actor_database.pkl", "rb"))
			new_show_updates = find_new_shows_with_preffered_actors(current_shows, show_actor_database_pkl, actor_preference_database, show_date_database_pkl)
			notification_via_email(new_show_updates)
			break
		if menu_choice == "6":
			break
		else: 
			print("Please enter a valid number: ")

def main():
	fetch_data()
	user_input()

if __name__ == "__main__":
	main()

