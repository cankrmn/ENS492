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


options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

url= "https://threatpost.com/search/fraud/?post_type=post&search-older=true"
driver.get(url)
time.sleep(5)

click_counter=0 
while True:
  soup = BeautifulSoup(driver.page_source, 'lxml')
  for post in soup.find_all('div', {"class": "o-col-8@md o-col-4@lg c-card__col-title"}):
    if(post.find('time').attrs["datetime"].split('-')[0]> "2017"):
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




def getSearchResults():
  queries = ['fraud']#, 'hacker groups', 'government', 'corporation',
      # 'unrelated', 'darknet', 'cyber defense', 'hacking', 'security concepts',
      # 'security products', 'network security', 'cyberwar', 'geopolitical',
      # 'data breach', 'vulnerability', 'platform', 'cyber attack']
  
  for query in queries:
    # Constracting http query
    url = 'https://threatpost.com/search/'+query+'/?post_type=post&search-older=true'
    
    response = requests.get(url, headers = header).text
    soup = BeautifulSoup(response, "lxml")

    for posts in soup.find_all('article', class_="c-card c-card--horizontal--half@md c-card--horizontal@lg c-card--horizontal--flat@md js-post-item"):
      for post in posts.find_all('h2', {"class": "c-card__title"}):
        for link in post.find_all('a'):
          print(link.get('href'))


def scrapeThreatPost(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")
  dic = {} 
  body=""
  for div in soup.find_all('div', class_='c-article__content js-reading-content'):
    for p in div.find_all('p'):
      if p.parent["class"][0] != "c-article__sharing":
        body = body + (p.text)
  dic["raw text"] = body
  print("DEVAM")
  return dic

#getSearchResults()
#scrapeThreatPost("https://packetstormsecurity.com/news/view/31293/Microsoft-Outlook-Users-Targeted-By-Gamaredon-s-New-VBA-Macro.html")
#scrapeThreatPost("https://threatpost.com/microsoft-outlook-users-targeted-by-gamaredons-new-vba-macro/156484/")