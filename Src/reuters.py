from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import requests

from Utils.header import header
from Utils.get_text import getText


def scrapeReuters(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    textContainer = soup.find("div",
                              class_="article-body__content__17Yit paywall-article")
    pArray = textContainer.find_all("p")
    pArray.pop()  # also need to remove first paragraph until "-"
    rawText = " ".join(list(map(getText, pArray)))
    dic["raw text"] = rawText
    print(dic)
    return dic


# will be deleted later
jsonFile = open("../packet_storm.json", "r+")
packet_storm = json.load(jsonFile)
reuters_news = packet_storm["Reuters"]
scrapeReuters(
    'https://www.reuters.com/business/retail-consumer/bed-bath-beyond-reviewing-possible-data-breach-2022-10-28/')
# for url in reuters_news:
#    scrapeReuters(url)

jsonFile.seek(0)
# convert back to json.
json.dump(packet_storm, jsonFile, indent=2)

jsonFile.close()
