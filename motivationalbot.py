import sys
import random 
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import textwrap

def main():
	print("Would you like to \n1. Select a topic for a quote\n2. Get a random quote ")
	print("-------------------------------------------------------------------------")
	choice = input()
	if (int(choice) == 1):
		#get topic
		print("Enter in a feeling/topic: ")
		topic = input()
		url = "https://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q={}&commit=Search".format(topic)
	else:
		url = "https://www.goodreads.com/quotes/"
	search_by_topic(url)

def search_by_topic(url):
	req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
	page = urlopen(url)
	#parse page with beautiful soup
	soup = BeautifulSoup(page, 'html.parser')
	#find all quote text
	quotes = soup.find_all('div', attrs={"class": "quoteText"})
	#handle errors 
	if (len(quotes) <= 0):
		print("Please enter a valid feeling/topic: ")
		sys.stdout.flush()
		input_feeling = input()
		search_by_topic(input_feeling)
	#generate random number to select a quote
	randomnumber = random.randint(0, len(quotes)-1)
	#print quote
	print("-------------------------------------------------------------------------")
	print(quotes[randomnumber].get_text())
	print("-------------------------------------------------------------------------")
	exit()

if __name__ == "__main__":
    main()