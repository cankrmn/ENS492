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

with open('security_intelligence_search.json', 'w') as f:
  json.dump({}, f)

with open('security_intelligence_search.json', 'r') as f:
  current_data = json.load(f)

def urlExists(url,query):
  if url in current_data:
    print("Url already exists in the database.")
    #print(current_data[url]["tags"])
    if current_data[url]["tags"].count(query)==0:
      # Update the 'tags' field of the dictionary
      current_data[url]['tags'].append(query)

      # Open the JSON file in write mode
      with open('security_intelligence_search.json', 'w') as f:
        # Write the updated dictionary back to the file
        json.dump(current_data, f)
      
    return True

  else:
    print("Url does not exist in the database.")
    return False

def add_data(key, value,tagAppend=False):
  current_data[key] = value
  print("Data added:", key)
  # create some new data to append to the file
  new_data = {
    key: value
  }
  # update the current data with the new data
  updated_data = {**current_data, **new_data}
  # save the updated data to the JSON file
  with open('security_intelligence_search.json', 'w') as f:
    json.dump(updated_data, f)

  

def getSearchResults():
  
  queries1 = ['fraud', 'hacker groups', 'government', 'corporation',
       'darknet', 'cyber defense', 'hacking', 'security concepts',
       'security products', 'network security', 'cyberwar', 'geopolitical',
       'data breach', 'vulnerability', 'platform', 'cyber attack']
  queries =["fraud", "hacker groups", "government", "corporation", "dark net", "incident response", "cyber intelligence", "antivirus", 
            "forensics", "pen testing", "cyber defense", "hacking", "white hat", "black hat", "stenography", "cryptography",
            "cloud security", "firewall", "network security", "cyberwar", "usa", "russia", 
            "ukraine", "cyberterrorism", "data breach", "security breach", "vulnerability", "cve", "XSS", "patch", "mobile", "IoT", "OS", "platform",
            "cyber attack", "malware", "virus", "DDOS", "botnet", "phishing", "adware", "rootkit", "backdoor", "keylog", "trojan", 
            "ransomware", "spyware"]

  for query in queries:

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled') #??
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
        if(click_counter > 30):
          raise NoSuchElementException
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
      urlKey= post.find('a', {"class": "search__excerpt"}).get('href')
      if(urlExists(urlKey,query)):
        continue
      else:
        print("starting scraping")
        if query == "dark net":
            query = "darknet"
        scrapeSecurityIntelligence(urlKey, query)

    for listPost in soup.find_all('div', {"class": "article__text_container"}):
      #listPostUrl = listPost.find('a').get('href')
      listPostUrl = listPost.find('a',{"class":"article__content_link"}).get('href')
      if listPostUrl != "{{{permalink}}}":
        if(urlExists(listPostUrl,query)):
          continue
        else:
          print("starting scraping")
          if query == "dark net":
            query = "darknet"
          scrapeSecurityIntelligence(listPostUrl, query)
    driver.close()
    print(query + " finished!")
  

def scrapeSecurityIntelligence(url, query=""):
  requests.packages.urllib3.disable_warnings()
  html_text = requests.get(url, headers = header, verify=False).text
  soup = BeautifulSoup(html_text, "lxml") 

  dic = {}  
  isEvent = False
  body=""
  for div in soup.find_all('main', class_='post__content'):
    for p in div.find_all(['h2', 'p']):
      if p.parent!= None and p.parent.class_ != "author__description":
        body = body + " " + (p.text) 

  dic["raw text"] = body
  if(soup.find("p", class_= "breadcrumbs__page_title") != None):
    dic["title"] = soup.find("p", class_= "breadcrumbs__page_title").text
  else:
    isEvent = True
    dic["title"] = ""
  dic["url"] = url

  date_string = soup.find("span", class_="article__info__date")
  if(date_string != None):
    date_string = date_string.text.replace(',', '').replace(' ', '-')
    dic["date"] = str(datetime.strptime(date_string, '%B-%d-%Y').strftime('%d/%m/%Y')) if len(date_string)!= "" else "No Date" 
  else: 
    dic["date"] = ""
  dic["source"]= {"url": "https://securityintelligence.com/", "label":"Security Intelligence"}
  if query != "":
    dic["tags"]=[]
    dic["tags"].append(query)
  if(isEvent == False):
    print(dic)
    add_data(url, dic)

'''''
with open('security_intelligence_search.json', 'r') as f:
  data1 = json.load(f)
  print(len(data1.items()))

  for key,value in data1.items():
    if len(value["tags"])>1:
      print(key, value["tags"])
'''''





#Uncomment following line for testing scraper:
#scrapeSecurityIntelligence("https://securityintelligence.com/news/ibm-z16-quantum-cyber-attacks/")

#Uncomment following line for Search:
#getSearchResults()

