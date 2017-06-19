from bs4 import BeautifulSoup
import urllib.request as urllib2

import unicodedata
import collections, re	

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  

import numpy as np
import string 

from nltk.corpus import stopwords
import nltk


class top_news():
	def toi(self):
		
		# TOI url
		url = 'http://timesofindia.indiatimes.com/'

		# url to html
		response = urllib2.urlopen(url)
		html = response.read()
		toi_news = []
		
		# scrap News
		soup = BeautifulSoup(html,"lxml")
		for li in soup.find_all("ul", class_='list8'):
			child = li.findChildren('li')
			for schild in child:
				toi_news.append(schild.text)
		
		final_toi_news = []
		# Print news
		for i in toi_news[:7]:
			txt = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
			final_toi_news.append(txt.decode('utf-8').strip('\n'))		

		#for i in final_toi_news:
			#print(i)
		return final_toi_news

	def india_today(self):
		
		# TOI url
		url = 'http://indiatoday.intoday.in/'

		# url to html
		response = urllib2.urlopen(url)
		html = response.read()
		in_today_news = []
		
		# scrap News
		soup = BeautifulSoup(html,"lxml")
		for li in soup.find_all("div", class_='newstextlink'):
			child = li.findChildren('a')
			for schild in child:
				in_today_news.append(schild.text)
		
		final_in_today_news=[]
		# Print news
		for i in in_today_news:
			txt = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
			final_in_today_news.append(txt.decode('utf-8'))	
		
		#for i in final_in_today_news:
			#print(i)
		return final_in_today_news

	def google_news(self):
		
		# TOI url
		url = 'https://news.google.co.in/'

		# url to html
		response = urllib2.urlopen(url)
		html = response.read()
		google_news = []
		
		# scrap News
		soup = BeautifulSoup(html,"lxml")
		for li in soup.find_all("span", class_='titletext',limit=5): # limit = number of classes to scrap for titletext
			google_news.append(li.text)
		
		final_google_news=[]
		# Print news
		for i in google_news:
			txt = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
			final_google_news.append(txt.decode('utf-8'))	
		
		#for i in final_google_news:
			#print(i)
		return final_google_news

# Uncomment this and use it to download stopwords 
#nltk.download()

# Scrapping starts
top = top_news()
print('Top news: ')
text1 = top.toi()
text2 = top.india_today()
text3 = top.google_news()

# All the scrapped news in text
text = text1+text2+text3
print(len(text))

# Print the scraped news data
for i, j in zip(text, range(0, len(text))):
	print(str(j)+' '+i)

# For tokenizing the text
tokenize = lambda doc: doc.lower().split(" ")

# Removing stopwords, tokenizing and creating tdidf vectorizer object
sklearn_tfidf = TfidfVectorizer(stop_words='english', tokenizer=tokenize) # use tokenizer=tokenize for tokenizing

# Fitting text to the object and obtaining tfidf matrix
tfidf_matrix = sklearn_tfidf.fit_transform(text) 
#print(tfidf_matrix)

# For storing news
final_news=[]
indexes = []

# This loop calculates the similarity between the individual news headline with the other headlines 
# and appends accordingly to the final_news list
for i in range(0, len(text)):

	# Calculates cosine similarity
	cosine = cosine_similarity(tfidf_matrix[i], tfidf_matrix)

	# Delete itself from the tfidf matrix
	cosine = np.delete(cosine, i)

	# Append news headlines having maximum cosine_similarity with the ith headline 
	# and also which are unique(having tfidf 0 for the ith headline)
	if np.all(cosine==0):
		final_news.append(text[i])
	else:
		max_i = np.argmax(cosine)
		final_news.append(text[max_i])

	# k = index, l = individual element in cosine matrisx
	try:
		for k,l in np.ndenumerate(cosine):
			#print(k)
			if cosine.item(i) == l:
				indexes.append(k[0])
	except :
		pass

try:
	for i in indexes:
		final_news.remove(text[i])
except:
	pass

# Remove news having less than 5 words
for news in final_news:
	i = news
	if len(i.split(" ")) < 6:
		final_news.remove(news)

# Remove space break at the starting of the news headlines if present
for news, i in zip(final_news, range(0,len(final_news))):
	if news[0]==' ':
		final_news[i] = final_news[i][1:]

# Remove duplicate items from the final_news list
final_news = set(final_news)

# Display the final NEWS
print("Final NEWS: ")
for i in final_news:
	print(i)

# The number of final NEWS headlines
print(len(final_news))
