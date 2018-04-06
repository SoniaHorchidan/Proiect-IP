import urllib.request
from bs4 import BeautifulSoup


def findKeywords(urls, keywords):
	# function receives a list of urls and a list of keywords and returns a dictionary
	# with urls and the found keywords
	dictionary = {}
	for url in urls:
		dictionary[url] = []
		html = urllib.request.urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")
		for script in soup(["script", "style"]):
		    script.extract()    
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		for word in keywords:
			if word.lower() in text.lower().split():
				dictionary[url].append(word)		
	return dictionary
			