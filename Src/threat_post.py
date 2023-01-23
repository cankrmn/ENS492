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
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

with open('threatpost_search.json', 'w') as f:
  json.dump({}, f)

with open('threatpost_search.json', 'r') as f:
  current_data = json.load(f)

def urlExists(url,query):
  if url in current_data:
    print("Url already exists in the database." + url)
    #print(current_data[url]["tags"])
    if current_data[url]["tags"].count(query)==0:
      # Update the 'tags' field of the dictionary
      current_data[url]['tags'].append(query)
      # Open the JSON file in write mode
      with open('threatpost_search.json', 'w') as f:
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
  with open('threatpost_search.json', 'w') as f:
    json.dump(updated_data, f)

  

def getSearchResults():
  
  queries1 = ['fraud', 'hacker groups', 'government', 'corporation',
       'dark net', 'cyber defense', 'hacking', 'security concepts',
       'security products', 'network security', 'cyberwar', 'geopolitical',
       'data breach', 'vulnerability', 'platform', 'cyber attack']
  queries=["fraud", "hacker groups", "government", "corporation", "dark net", "incident response", "cyber intelligence", "antivirus", 
            "forensics", "pen testing", "firewall", "cyber defense", "hacking", "white hat", "black hat", "stenography", "cryptography",
            "cloud security", "firewall", "antivirus", "botnet", "IoT", "DDOS", "network security", "cyberwar","cyberwar", "usa", "russia", 
            "ukraine", "cyberterrorism", "data breach", "security breach", "vulnerability", "cve", "XSS", "patch", "mobile", "IoT", "OS", "platform",
            "cyber attack", "malware", "virus", "DDOS", "botnet", "phishing", "adware", "rootkit", "backdoor", "keylog", "trojan", 
            "ransomware", "spyware"]


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
      try:
        if(click_counter > 1):
          raise NoSuchElementException
        button = driver.find_element("xpath", '/html/body/div[2]/div[1]/div/div/div/div[1]/div[3]/button')
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)
        click_counter += 1 
      except NoSuchElementException:
        break
      except StaleElementReferenceException:
        break
      except NoSuchWindowException:
        break  
    for post in soup.find_all('article', {"class": "c-card c-card--horizontal--half@md c-card--horizontal@lg c-card--horizontal--flat@md js-post-item"}):
      if(post.find('time').attrs["datetime"].split('-')[0]> "2017"):
        urlKey= post.find('a').get('href')
        if(urlExists(urlKey,query)):
          continue
        else:
          print("starting scraping")
          if query == "dark net":
            query = "darknet"
          scrapeThreatPost(urlKey, query) 
    driver.close()
    print(query + " finished!")

   
def scrapeThreatPost(url, query=""):
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
  dic["source"]= {"url": "https://threatpost.com/", "label":"Threatpost"}

  
  if query != "":
    dic["tags"]=[]
    dic["tags"].append(query)
  print(dic)
  add_data(url, dic)


''''
with open('threatpost_search.json', 'r') as f:
  data1 = json.load(f)
  for key,value in data1.items():
    if len(value["tags"])>1:
      print(key, value["tags"])
'''''

#Uncomment following lines to test the scraper:
#scrapeThreatPost('https://threatpost.com/squirrelwaffle-fraud-exchange-server-malspamming/178434/')


#Uncomment following line for Search:
#getSearchResults()
