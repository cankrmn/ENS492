from bs4 import BeautifulSoup
import requests
import string
import pandas as pd

# initialDic = {
#    "title": "",
#    "first paragraph": "",
#    "url": "",
#    "date": "",
#    "stemmed text": "",
# }

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

def scrapeTheRegister(earlier):
  df = pd.DataFrame()
  html_text = requests.get('https://www.theregister.com/' + earlier, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")
  allNews = soup.find_all("div", class_ = "time_comments")

  for new in allNews:
    # print(new.contents[2].get("title"))

    dic = {}

    dic["title"] = new.parent.h4.text
    dic["first paragraph"] = new.parent.div.text
    dic["url"] = "https://www.theregister.com" + new.parent.parent.get("href")
    spans = new.find_all("span")
    dic["date"] = spans[1].text if len(spans) > 1 else "No Date"
    if(spans[0].text == "Security" or spans[0].text == "Cyber-crime" or spans[0].text == "Patches" or spans[0].text == "Research" or spans[0].text == "CSO"):
      dic["category"] = spans[0].text
    else:
      dic["category"] = "non-security"
   #  dic["stemmed text"] = tokenizeTheRegister(dic["url"])
    df = df.append(dic, ignore_index = True)

  return df