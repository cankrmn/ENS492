from bs4 import BeautifulSoup
import requests
import string
import re
#from Utils.format_text import formatText

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

url1 = "https://edition.cnn.com/2022/11/02/politics/biden-speech-democracy-dc/index.html"

def scrapeCnn(url):
  html_text = requests.get(url, headers=header).text
  soup = BeautifulSoup(html_text, "lxml")
  dic = {}
  textContainer = soup.find("div", class_="article__content")
  pArray = textContainer.find_all("p")
  raw_text = getText(pArray, ['<.*?>', '\\n'])
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
#print(scrapeCnn(url1))