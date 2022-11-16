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
    if soup is not None:
        textContainer = soup.find("div", class_="GuttenbergBlockFactory_wrapper__RwaDA")
        if textContainer is not None:
            pArray = textContainer.find_all("p")
            rawText = " ".join(list(map(getText, pArray)))
            dic["raw text"] = rawText
    return dic
