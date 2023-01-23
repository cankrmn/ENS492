from bs4 import BeautifulSoup
import requests
import string
import re
#from Utils.format_text import formatText

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

url1 = "https://www.cnet.com/tech/home-entertainment/apple-tv-4k-2022-review-in-progress-cheaper-price-new-chip-only-go-so-far/"

def scrapeCnet(url):
  html_text = requests.get(url, headers=header).text
  soup = BeautifulSoup(html_text, "lxml")
  dic = {}
  textContainer = soup.find("div", class_="col-6 article-main-body row")
  pArray = textContainer.find_all("p")
  raw_text = getText(pArray, ['<.*?>'])
  dic["raw text"] = raw_text
  #dic["stemmed text"] = formatText(raw_text)
  #print(dic["raw text"])
  return dic

def getText(text, regexList):
  newText = text
  for regex in regexList:
    newText = re.sub(regex, '', str(newText))
  return newText

#Uncomment the following line for testing crawler:
#print(scrapeCnet(url1))