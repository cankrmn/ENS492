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
    if soup is not None:
        textContainer = soup.find("div",
                                  class_="article-body__content__17Yit paywall-article")
        if textContainer is not None:
            pArray = textContainer.find_all("p")
            pArray.pop()  # also need to remove first paragraph until "-"
            rawText = " ".join(list(map(getText, pArray)))
            dic["raw text"] = rawText
    return dic
