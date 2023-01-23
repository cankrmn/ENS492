from bs4 import BeautifulSoup
import requests
import string
import re
import json
import time

import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome('chromedriver',options=chrome_options)

def check_eop(html_text, max_year):#end of page
  date_regex = 'class="fa fa-clock-o"><\/i>(.*, (\d*))<\/a><\/div>'
  date = re.search(date_regex, html_text)
  if date is not None:
    date_year = date.group(2)
    if int(date_year) >= max_year:
      return False, date_year
    else:
      return True, 0
  return False, 0

def getSearchResults(tagName):

   print("Searching: " + tagName)
   myDict = {}

   driver = webdriver.Chrome('chromedriver',options=chrome_options)
   driver.maximize_window()
   current_page = 1
   end_of_page = False
   url= 'https://www.itsecurityguru.org/page/' + str(current_page) + '/?s=' + tagName #get first page
   driver.get(url)
   time.sleep(5)

   regex_last_page = '(<a class="page_number").*"(\d*)".*(\s<a class="page_nav next")'
   last_page = re.search(regex_last_page, str(driver.page_source))#get last page

   if last_page is not None:
      last_page = last_page.group(2)
      print("last_page: " + str(last_page))
      for page_no in range(1, int(last_page) + 1):#loop all pages
         if not end_of_page:
            print("current page: " + str(page_no))
            url= 'https://www.itsecurityguru.org/page/' + str(page_no) + '/?s=' + tagName
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            news_list = soup.find_all("article", {"class": "jeg_post jeg_pl_md_2 format-standard"})

            for new in news_list:
            #print(len(news_list))
               date_result = check_eop(str(new), 2017)
               if not date_result[0]:#check date
                  href_regex = '<a href=.*("https.*\/")><div class'
                  web_url = re.search(href_regex, str(new))#get url
                  if web_url is not None:
                     web_url = web_url.group(1)
                  myDict[web_url] = tagName
                  print(myDict)
   return myDict
   driver.close()

def getText(text, regexList):
  newText = text
  for regex in regexList:
    newText = re.sub(regex, '', str(newText))
  return newText


# Uncomment following line for Search:
# print(getSearchResults("fraud"))