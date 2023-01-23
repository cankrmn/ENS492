from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import requests

#from Utils.header import header
#from Utils.get_text import getText

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

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
            rawText = " ".join(list(map(lambda val : val.text, pArray)))
            dic["raw text"] = rawText
    return dic
    
#Uncomment the following line for testing crawler:
#print(scrapeReuters("https://www.reuters.com/technology/spotify-cut-staff-soon-this-week-bloomberg-news-2023-01-23/"))