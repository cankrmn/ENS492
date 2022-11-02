from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
# from modulefinder import packagePathMap

from Utils.header import header
from Utils.format_text import formatText

def tokenizeSecurityIntelligence(url):
  data = requests.get(url, headers = header).text
  new_soup = BeautifulSoup(data, "lxml")
  #body = new_soup.find_all("div", itemprop = "articleBody")

  body=""
  for div in new_soup.find_all('main', class_='post__content'):
    for p in div.find_all(['h2', 'p']):
      if p.parent["class"][0] != "author__description":
        body = body + " " + (p.text) 
  return body

def scrapeSecurityIntelligence(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")

  dic = {} 
  dic["title"] = soup.find("p", class_= "breadcrumbs__page_title").text
  #dic["first paragraph"] = soup.find("main", class_="post__content").find('p').text
  dic["url"] = url

  date_string = soup.find("span", class_="article__info__date").text.replace(',', '').replace(' ', '-')
  dic["date"] = str(datetime.strptime(date_string, '%B-%d-%Y').date()) if len(date_string)!= "" else "No Date"   

  rawText = tokenizeSecurityIntelligence(url)
  dic["raw text"] = rawText
  dic["stemmed text"] = formatText(rawText)
  #print(dic)
  return dic


# scrapeSecurityIntelligence("https://securityintelligence.com/articles/sec-business-data-breach/")
