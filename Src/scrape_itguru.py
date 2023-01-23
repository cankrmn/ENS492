from bs4 import BeautifulSoup
import requests
import string
import re
#from Utils.format_text import formatText

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

url1 = "https://www.itsecurityguru.org/2022/12/09/dragos-announces-partnership-with-cisco/"

def scrapeITGuru(url):
  html_text = requests.get(url, headers=header).text
  soup = BeautifulSoup(html_text, "lxml")
  dic = {}
  textContainer = soup.find("div", class_="content-inner")
  raw_text = ""
  pArray = textContainer.find_all("p")
  for paragraph in pArray:
    raw_text += paragraph.get_text()
  #print(raw_text)
  dic["raw text"] = raw_text
  #dic["stemmed text"] = formatText(raw_text)
  return dic


#Uncomment the following line for testing crawler:
#print(scrapeITGuru(url1))