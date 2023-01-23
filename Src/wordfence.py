from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import requests

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}


url = "https://www.wordfence.com/blog/2022/11/missing-authorization-vulnerability-in-blog2social-plugin/"

def scrapeWordfence(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    if soup is not None:
        textContainer = soup.find("section", class_="blog-post-content")
        if textContainer is not None:
            pArray = textContainer.find_all("p")
            rawText = " ".join(list(map(lambda val : val.text, pArray)))
            dic["raw text"] = rawText
    return dic
# Uncomment the following line to test the scraper
# print(scrapeWordfence(url))
