from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import requests

from Utils.header import header
from Utils.get_text import getText
from Utils.format_text import formatText


def scrapeSCMag(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    textContainer = soup.find("div", class_="GuttenbergBlockFactory_wrapper__RwaDA")
    pArray = textContainer.find_all("p")
    rawText = " ".join(list(map(getText, pArray)))
    dic["raw text"] = rawText
    print(dic)
    return dic


# will be deleted later
jsonFile = open("../packet_storm.json", "r+")
packet_storm = json.load(jsonFile)
scmag_news = packet_storm["SC Magazine"]
scrapeSCMag(
    'https://www.scmagazine.com/analysis/threat-intelligence/burgeoning-cranefly-hacking-group-has-a-new-intel-gathering-tool')
# for url in scmag_news:
#    scrapeReuters(url)

jsonFile.seek(0)
# convert back to json.
json.dump(packet_storm, jsonFile, indent=2)

jsonFile.close()
