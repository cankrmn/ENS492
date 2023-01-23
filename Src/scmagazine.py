import time

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

#from Utils.header import header
#from Utils.get_text import getText

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}


def search_scmag():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    queries1 = ['fraud', 'hacker groups', 'government', 'corporation',
                'darknet', 'cyber defense', 'hacking', 'security concepts',
                'security products', 'network security', 'cyberwar', 'geopolitical',
                'data breach', 'vulnerability', 'platform', 'cyber attack']

    queries = ['fraud']
    driver.maximize_window()
    for query in queries:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        url = 'https://www.scmagazine.com/search?q=' + query
        driver.get(url)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        print(soup)

    driver.close()


def scrapeSCMag(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    if soup is not None:
        textContainer = soup.find("div", class_="GuttenbergBlockFactory_wrapper__RwaDA")
        if textContainer is not None:
            pArray = textContainer.find_all("p")
            rawText = " ".join(list(map(lambda val : val.text, pArray)))
            dic["raw text"] = rawText
    return dic


#search_scmag()

#Uncomment the following line for testing crawler:
#print(scrapeSCMag("https://www.scmagazine.com/news/emerging-technology/microsoft-expands-availability-of-azure-openai-service"))

