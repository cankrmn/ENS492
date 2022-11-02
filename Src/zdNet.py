from bs4 import BeautifulSoup
import requests

from Utils.header import header 
from Utils.get_text import getText 
from Utils.format_text import formatText


def scrapeZDNet(url):
   html_text = requests.get(url, headers=header).text
   soup = BeautifulSoup(html_text, "lxml")
   dic = {}
   dic["first paragraph"] = soup.find("div", class_="c-contentHeader_description g-outer-spacing-top-medium g-outer-spacing-bottom-medium").text.strip()
   
   textContainer = soup.find("div", class_="c-ShortcodeContent")
   pArray = textContainer.find_all("p")
   rawText= " ".join(list(map(getText, pArray)))
   dic["raw text"] = rawText
   dic["stemmed text"] = formatText(rawText)
   return dic