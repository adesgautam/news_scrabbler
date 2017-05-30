from bs4 import BeautifulSoup
import urllib.request as urllib2

import unicodedata		

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
		for li in soup.find_all("span", class_='titletext',limit=20):
			google_news.append(li.text)
		
		final_google_news=[]
		# Print news
		for i in google_news:
			txt = unicodedata.normalize('NFKD', i).encode('ascii','ignore')
			final_google_news.append(txt.decode('utf-8'))	

		return final_google_news

top = top_news()
print('Top news: ')
text1 = top.toi()
text2 = top.india_today()
text3 = top.google_news()
text = text1+text2+text3
for i in text:
	print(i)
