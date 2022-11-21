from modulefinder import packagePathMap
from bs4 import BeautifulSoup
import requests
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
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

    url= 'https://securityintelligence.com/?s='+query+'&orderby=date&post_type%5B%5D=post&post_type%5B%5D=ibm_internals&post_type%5B%5D=ibm_externals&post_type%5B%5D=ibm_news&post_type%5B%5D=ibm_event'
    driver.get(url)
    time.sleep(5)

    while True:
      soup = BeautifulSoup(driver.page_source, 'lxml')
      for post in soup.find_all('article', {"class": "post post--list search__post"}):
        
          #bunu printlemek yerine alttakini comment out et.
          #scrapeSecurityIntelligence(post.find('a', {"class": "search__excerpt"}).get('href'))
          print(post.find('a', {"class": "search__excerpt"}).get('href'))
      try:
        if(post.find('span', {"class": "post__date"}).text.split(',')[1] < "2017"):
          raise NoSuchElementException
        button = driver.find_element("xpath", '/html/body/div[2]/div/section/amp-list/amp-list-load-more[1]/button')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
      except NoSuchElementException:
        break
    driver.close()



def scrapeSecurityIntelligence(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")

  dic = {}  

  body=""
  for div in soup.find_all('main', class_='post__content'):
    for p in div.find_all(['h2', 'p']):
      if p.parent["class"][0] != "author__description":
        body = body + " " + (p.text) 

  dic["raw text"] = body
  
  return dic

#getSearchResults()
#scrapeSecurityIntelligence("https://securityintelligence.com/articles/sec-business-data-breach/")
