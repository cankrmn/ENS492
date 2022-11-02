from bs4 import BeautifulSoup
import requests
import string
import pandas as pd
import json
from Utils.getText import getText

# allTags = ['0 Day', 'Adobe', 'Afghanistan', 'Africa', 'Algeria', 'Amazon', 'Anonymous', 'Apache', 'Apple', 'Argentina', 'Australia', 'Backdoor', 'Bank', 'BlackBerry', 'Botnet', 'Brazil', 'Britain', 'BSD', 'Canada', 'Car', 'Caribbean', 'Censorship', 'China', 'CIA', 'Cisco', 'Commodore', 'Conference', 'Cookiejacking', 'Cryptography', 'CSRF', 'Cuba', 'Cybercrime', 'Cyberwar', 'Data Loss', 'Database', 'DMCA', 'DNS', 'DoS', 'eBay', 'Egypt', 'Email', 'Ethiopia', 'Facebook', 'FBI', 'Finland', 'Firefox', 'Flaw', 'France', 'Fraud', 'Gamble', 'Germany', 'Google', 'Google Chrome', 'Government', 'Greece', 'Hacker', 'Headline', 'IBM', 'Identity Theft', 'India', 'Indonesia', 'Intel', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Japan', 'Java', 'Juniper', 'Kernel', 'Korea', 'Libya', 'Linux', 'Malaysia', 'Malware', 'McAfee', 'Mexico', 'Microsoft', 'Military', 'Motorola', 'Mozilla', 'MPAA', 'MySQL', 'Nasa', 'Netherlands', 'New Zealand', 'Nintendo', 'Nokia', 'Nortel', 'Norway', 'NSA', 'OpenBSD', 'Opera', 'Oracle', 'Pakistan', 'Passport', 'Password', 'Patch', 'PayPal', 'Philippines', 'Phish', 'Phone', 'Pirate', 'Portugal', 'Privacy', 'Religion', 'RFID', 'RIAA', 'Romania', 'RSA', 'Russia', 'Safari', 'Samsung', 'Saudi Arabia', 'Scada', 'Scam', 'Science', 'Scotland', 'Sega', 'Singapore', 'Site', 'Skype', 'Social', 'Sony', 'Space', 'Spain', 'Spam', 'Spyware', 'SSH', 'SSL', 'Survey', 'Sweden', 'Switzerland', 'Symantec', 'Syria', 'Taiwan', 'Terror', 'Thailand', 'Trojan', 'Turkey', 'Twitter', 'Uber', 'USA', 'Venezuela', 'VeriSign', 'Vietnam', 'Virus', 'VoIP', 'WebKit', 'Wireless', 'WordPress', 'Worm', 'XSS', 'Yahoo!', 'Yemen']

months = {
   "Jan": "01",
   "Feb": "02",
   "Mar": "03",
   "Apr": "04",
   "May": "05",
   "Jun": "06",
   "Jul": "07",
   "Aug": "08",
   "Sep": "09",
   "Oct": "10",
   "Nov": "11",
   "Dec": "12",
}

def dateFormatter(dateStr):
   dateArr = dateStr.split(" ")
   return dateArr[1][:-1] + "/" +  months[dateArr[0]] + "/" + dateArr[2]

header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

packetStorm = {
   "title": "",
   "url": "",
   "date": "",
   "source": "",
   "tags": "",
   "first paragraph": "",
   "stemmed text": "",
}


jsonFile = open("packet_storm.json", "r+")
fileData = json.load(jsonFile)

def scrapePacketStorm(page = ""):
   html_text = requests.get('https://packetstormsecurity.com/news/' + page, headers = header).text
   soup = BeautifulSoup(html_text, "lxml")
   newsList = soup.find_all("dl", class_ = "news")

   for newsInstance in newsList:
      dic = {}

      try:
         dic["title"] = newsInstance.dt.text
         dic["url"] = "https://packetstormsecurity.com" + newsInstance.dt.a.get("href")
         dic["date"] = dateFormatter(newsInstance.find("dd", class_ = "datetime").a.text)
         dic["source"] = {"url": newsInstance.find("dd", class_ = "posted-by").a.get("href"), "label": newsInstance.find("dd", class_ = "posted-by").a.text }
         
         tagsArr = newsInstance.find("dd", class_ = "tags").find_all("a")
         tagsArr = list(map(getText, tagsArr))
         dic["tags"] = tagsArr
         dic["isParsed"] = False

         sourceName = dic["source"]["label"]
         if sourceName in fileData:
            if(dic["url"] not in fileData[sourceName]):
               fileData[sourceName][dic["url"]] = dic
         else:
            fileData[sourceName] = {dic["url"]: dic}
      except:
         print(f'error on page: {page}')

for i in range(110, 120):
   scrapePacketStorm("page" + str(i + 1))

# scrapePacketStorm()
# Sets file's current position at offset.
jsonFile.seek(0)
# convert back to json.
json.dump(fileData, jsonFile, indent = 2)


jsonFile.close()