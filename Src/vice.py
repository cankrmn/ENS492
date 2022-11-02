from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import requests

from Utils.header import header
from Utils.get_text import getText


def scrapeVice(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    textContainer = soup.find("div",
                              class_="article__body-components")
    pArray = textContainer.find_all("p")
    pArray.pop()
    rawText = " ".join(list(map(getText, pArray)))
    dic["raw text"] = rawText
    print(dic)
    return dic


# will be deleted later
jsonFile = open("../packet_storm.json", "r+")
packet_storm = json.load(jsonFile)
vice_news = packet_storm["VICE"]
scrapeVice(
    'https://www.vice.com/en/article/4axqed/cybercriminals-leak-la-school-data-after-it-refuses-to-ransom')

jsonFile.seek(0)
# convert back to json.
json.dump(packet_storm, jsonFile, indent=2)

jsonFile.close()
