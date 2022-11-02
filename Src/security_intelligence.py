from modulefinder import packagePathMap
from bs4 import BeautifulSoup
import requests
import string


header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

def scrapeSecurityIntelligence(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")

  dic = {}  

  body=""
  for div in soup.find_all('main', class_='post__content'):
    for p in div.find_all(['h2', 'p']):
      if p.parent["class"][0] != "author__description":
        body = body + " " + (p.text) 

  dic["raw text"] = body
  
  return dic


#scrapeSecurityIntelligence("https://securityintelligence.com/articles/sec-business-data-breach/")
