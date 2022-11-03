from bs4 import BeautifulSoup
import requests
import string
import re
import json
from Utils.format_text import formatText

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

url2 = "https://www.theguardian.com/environment/2022/nov/02/europes-climate-warming-at-twice-rate-of-global-average-says-report"#web url
url3 = "https://content.guardianapis.com/environment/2022/nov/02/europes-climate-warming-at-twice-rate-of-global-average-says-report?show-fields=all&api-key=6b75646b-af1d-4b1e-a7f1-0806a7015400"#api url

def scrapeGuardian(url):
  api_url_content = getText(url, ['https:\/\/www\.theguardian\.com'])
  api_url = 'https://content.guardianapis.com' + api_url_content + '?show-fields=all&api-key=6b75646b-af1d-4b1e-a7f1-0806a7015400'
  api_text = requests.get(api_url, headers=header).text
  news_json = json.loads(api_text)
  news_body = news_json['response']['content']['fields']['body']
  
  dic = {}
  raw_text = getText(news_body, ['<p>', '<\/p>', '<a.*?a>'])
  dic["raw text"] = raw_text
  dic["stemmed text"] = formatText(raw_text)
  #print(dic["raw text"])
  return dic

def getText(text, regexList):
  newText = text
  for regex in regexList:
    newText = re.sub(regex, '', str(newText))
  return newText
