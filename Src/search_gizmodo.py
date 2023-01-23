from bs4 import BeautifulSoup
import requests
import string
import re
import json
import time
'''''
!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
'''''
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',options=chrome_options)

def end_of_page_check(soup, min_year, news_content):
  if(soup.find("a", {"class": "peggds-2 ixaYpK next-button"})):
    return False
  else:
    date_year = re.search('datetime="(\d*?)-', str(news_content))
    if(date_year != None and int(date_year.group(1)) > min_year):
     return False
    return True

def search_gizmodo(keyword, min_year = 2020, max_page = 5):#usage: search_gizmodo("hacking", 2019, 4)
  end_of_page = False
  page_count = 1
  dic_list = []
  while(not end_of_page):
    #goto url
    url = "https://gizmodo.com/tag/" + keyword + "?startIndex=" + str(page_count * 20)
    driver.get(url)

    driver.maximize_window()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    news_content = soup.find_all("div", {"class": "cw4lnv-5 aoiLP"}) #get all news in page
    print(news_content)

    if(end_of_page_check(soup, min_year, news_content) or max_page <= page_count):#is this the last page to iterate
      end_of_page = True

    for news in news_content:#get urls from news
      dic = {}
      news_url = re.search('"https.*?"', str(news))
      if(news_url):
        dic["keyword"] = keyword
        dic["webUrl"] = news_url.group(0)
        dic_list.append(dic)

    page_count += 1
    #print("page:" + str(page_count))

  #print("End, page count: " + str(page_count))
  return dic_list

#Uncomment the following line for testing crawler:
#print(search_gizmodo("fraud",2017,3))
