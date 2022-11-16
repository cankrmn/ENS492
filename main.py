import json
import pandas as pd

from Utils.format_text import formatText

from Src.ars_technica import scrapeArsTechnica
from Src.bbc_news import scrapeBBCNews
from Src.scmagazine import scrapeSCMag
from Src.security_intelligence import scrapeSecurityIntelligence
from Src.the_hacker_news import scrapeTheHackerNews
from Src.threat_post import scrapeThreatPost
from Src.zdNet import scrapeZDNet


CRAWLERS = {
   #"BBC News UK": {"crawler": scrapeBBCNews, "key": "BBC News UK" },
   #"SC Magazine": {"crawler": scrapeSCMag, "key": "SC Magazine" },
   #"Security Intelligence": {"crawler": scrapeSecurityIntelligence, "key": "Security Intelligence" },
   "The Hacker News": {"crawler": scrapeTheHackerNews, "key": "The Hacker News" },
   #"Threatpost": {"crawler": scrapeThreatPost, "key": "Threatpost" },
   #"ZDNet": {"crawler": scrapeZDNet, "key": "ZDNet" },
}

def main():
   df = pd.read_csv('parsed_news.csv')


   jsonFile = open("packet_storm.json", "r+")
   fileData = json.load(jsonFile)

   for dict in CRAWLERS.values():
      crawler = dict["crawler"]
      key = dict["key"]
      
      for newsInstance in fileData[key].values():
         if(newsInstance["isParsed"] == True): 
            continue # go to the next news if already parsed
         
         url = newsInstance["url"]
         dic = crawler(url)
         dic["stemmed text"] = formatText(dic["raw text"])

         tempNewsInstance = newsInstance.copy()
         del tempNewsInstance["isParsed"]



         df = df.append({**dic, **tempNewsInstance}, ignore_index=True)
         newsInstance["isParsed"] = True

   df.to_csv("parsed_news.csv")

   # Sets file's current position at offset.
   jsonFile.seek(0)
   # convert back to json.
   json.dump(fileData, jsonFile, indent = 2)

   jsonFile.close()
      
main()