from datetime import datetime
from modulefinder import packagePathMap
from bs4 import BeautifulSoup
import requests
import string
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}


def getSearchResults():
  
  queries1 = ['fraud', 'hacker groups', 'government', 'corporation',
       'darknet', 'cyber defense', 'hacking', 'security concepts',
       'security products', 'network security', 'cyberwar', 'geopolitical',
       'data breach', 'vulnerability', 'platform', 'cyber attack']
  queries=['fraud']
  for query in queries:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    url= 'https://threatpost.com/search/'+query+'/?post_type=post&search-older=true'
    driver.get(url)
    time.sleep(5)

    click_counter=0 
    while True:
      soup = BeautifulSoup(driver.page_source, 'lxml')
      for post in soup.find_all('div', {"class": "o-col-8@md o-col-4@lg c-card__col-title"}):
        if(post.find('time').attrs["datetime"].split('-')[0]> "2017"):
          #bunu printlemek yerine alttakini comment out et.
          #scrapeThreatPost(post.find('a').get('href'))
          print(post.find('a').get('href')+ " "+ post.find('time').attrs["datetime"].split('-')[0])
      try:
        if(click_counter > 4):
          raise NoSuchElementException
        button = driver.find_element("xpath", '/html/body/div[2]/div[1]/div/div/div/div[1]/div[3]/button')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        click_counter += 1
      except NoSuchElementException:
        break
    driver.close()


def scrapeThreatPost(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")
  dic = {} 
  body=""
  for div in soup.find_all('div', class_='c-article__content js-reading-content'):
    for p in div.find_all(['p','li','h2']):
      if p.parent.has_attr('class'):
        if p.parent.attrs["class"][0] != "c-article__sharing":
          body = body + (p.text)
      else: 
        body = body + (p.text)
  dic["raw text"] = body

  dic["title"] = soup.find("h1", class_= "c-article__title").text
  dic["url"] = url
  date_string = soup.find("div", class_="c-article__time").find("time").attrs["datetime"].split('T')[0]
  dic["date"] = str(datetime.strptime(date_string, '%Y-%m-%d').strftime('%d/%m/%Y')) if len(date_string)!= "" else "No Date"   

  return dic

#getSearchResults()
#scrapeThreatPost('https://threatpost.com/squirrelwaffle-fraud-exchange-server-malspamming/178434/')