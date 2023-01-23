from modulefinder import packagePathMap
from bs4 import BeautifulSoup
import requests
import string


header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

def scrapeBBCNews(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")

  dic = {} 
  body=""
  for div in soup.find_all('div', class_='ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0'):
    for p in div.find_all('p'):
        body = body + (p.text)
  dic["raw text"] = body
  return dic

#Uncomment the following line for testing crawler:
#print(scrapeBBCNews("https://www.bbc.com/news/uk-63328398"))
