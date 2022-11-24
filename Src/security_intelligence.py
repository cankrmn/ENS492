from datetime import datetime
from modulefinder import packagePathMap
from bs4 import BeautifulSoup
import requests
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import  StaleElementReferenceException
from selenium.common.exceptions import NoSuchWindowException
import time
import json
import pandas as pd


header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
  

def getSearchResults():
  
  queries = ['fraud', 'hacker groups', 'government', 'corporation',
       'darknet', 'cyber defense', 'hacking', 'security concepts',
       'security products', 'network security', 'cyberwar', 'geopolitical',
       'data breach', 'vulnerability', 'platform', 'cyber attack']
  queries1=['fraud']

  dic= {}

  for query in queries:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    url= 'https://securityintelligence.com/?s='+query+'&orderby=date&post_type%5B%5D=post&post_type%5B%5D=ibm_internals&post_type%5B%5D=ibm_externals&post_type%5B%5D=ibm_news&post_type%5B%5D=ibm_event'
    driver.get(url)
    time.sleep(5)

   
    click_counter=0
    while True:
      soup = BeautifulSoup(driver.page_source, 'lxml')
      try:
        if(click_counter > 20):
          raise NoSuchElementException
        #button = driver.find_element("xpath", '/html/body/div[2]/div/section/amp-list/amp-list-load-more[1]/button')
        button = driver.find_element("xpath", '/html/body/amp-list/amp-list-load-more[1]/button')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        click_counter+=1

      except NoSuchElementException:
        break
      except StaleElementReferenceException:
        break
      except NoSuchWindowException:
        break
    
    for post in soup.find_all('article', {"class": "post post--list search__post"}):
      #bunu printlemek yerine alttakini comment out et.
      #scrapeSecurityIntelligence(post.find('a', {"class": "search__excerpt"}).get('href'))
      #if(post.find('span', {"class": "post__date"}).text.split(',')[1] > "2017"):
      urlKey= post.find('a', {"class": "search__excerpt"}).get('href')
     
      if urlKey in dic and query not in dic[urlKey] and urlKey!="{{{permalink}}}":
        dic[urlKey].append(query)
      else:
        dic[urlKey] = [query]
  
    for listPost in soup.find_all('article', {"class": "article article_grid"}):
      #if(listPost.find('span', {"class": "article__date"}).text.split(',')[1] > "2017"):
      listPostUrl = listPost.find('a', {"class": "article__content_link"}).get('href')
      if listPostUrl in dic and query not in dic[urlKey] and listPostUrl!="{{{permalink}}}":
        dic[listPostUrl].append(query)
      else:
        dic[listPostUrl] = [query]
    driver.close()

    json_object = json.dumps(dic, indent=4)
    # Writing to sample.json
    with open("security_intelligence.json", "w") as outfile:
        outfile.write(json_object)



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
  dic["title"] = soup.find("p", class_= "breadcrumbs__page_title").text
  dic["url"] = url

  date_string = soup.find("span", class_="article__info__date").text.replace(',', '').replace(' ', '-')
  dic["date"] = str(datetime.strptime(date_string, '%B-%d-%Y').strftime('%d/%m/%Y')) if len(date_string)!= "" else "No Date"   

 
  return dic

getSearchResults()
#scrapeSecurityIntelligence("https://securityintelligence.com/articles/sec-business-data-breach/")
