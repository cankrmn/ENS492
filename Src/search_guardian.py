from bs4 import BeautifulSoup
import requests
import string
import re
import json

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

def search_guardian(keyword, maxPage):
  #testurl = https://content.guardianapis.com/search?q=hacking&section=technology|media|us-news|world|uk-news|politics|business|australia-news&type=article&show-tags=keyword&show-fields=all&from-date=2017-01-01&page=1&page-size=50&api-key=6b75646b-af1d-4b1e-a7f1-0806a7015400 # keyword = 'hacking'
  api_url = 'https://content.guardianapis.com/search?q=' + keyword + '&section=technology|media|us-news|world|uk-news|politics|business|australia-news&type=article&show-tags=keyword&show-fields=all&from-date=2017-01-01&page=1&page-size=50&api-key=6b75646b-af1d-4b1e-a7f1-0806a7015400'
  
  api_text = requests.get(api_url, headers=header).text
  response_json = json.loads(api_text)
  page_count = response_json['response']['pages']
  if (page_count >= maxPage):
    page_count = maxPage
  dic_list = []
  for current_page in range(1, 3 + 1):#iterate all pages
    #print("Parsing page no: " + str(current_page))
    page_api_url = 'https://content.guardianapis.com/search?q=' + keyword + '&section=technology|media|us-news|world|uk-news|politics|business|australia-news&type=article&show-tags=keyword&show-fields=all&from-date=2017-01-01&page='+ str(current_page) +'&page-size=50&api-key=6b75646b-af1d-4b1e-a7f1-0806a7015400'
    api_text = requests.get(api_url, headers=header).text
    response_json = json.loads(api_text)
    results = response_json['response']['results']

    for result in results:#iterate each page
      dic = {}
      raw_text = result['fields']['bodyText']
      dic["webUrl"] = result['webUrl']
      dic["keyword"] = keyword
      dic["raw text"] = raw_text
      dic_list.append(dic)

  return dic_list


#Uncomment following line for testing search:
#print(search_guardian("fraud",2))
