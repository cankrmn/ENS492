from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import requests

from Utils.header import header
from Utils.get_text import getText


def scrapeWordfence(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    textContainer = soup.find("section", class_="blog-post-content")
    pArray = textContainer.find_all("p")
    rawText = " ".join(list(map(getText, pArray)))
    dic["raw text"] = rawText
    print(dic)
    return dic


# will be deleted later
jsonFile = open("../packet_storm.json", "r+")
packet_storm = json.load(jsonFile)
wordfence_news = packet_storm["Wordfence"]
scrapeWordfence(
    'https://www.wordfence.com/blog/2022/08/ukrainian-website-threat-landscape-throughout-2022/')

jsonFile.seek(0)
# convert back to json.
json.dump(packet_storm, jsonFile, indent=2)

jsonFile.close()
