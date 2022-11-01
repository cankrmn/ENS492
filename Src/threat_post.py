from datetime import datetime
from modulefinder import packagePathMap
from bs4 import BeautifulSoup
import requests
import string
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.stem.snowball import SnowballStemmer
englishStemmer=SnowballStemmer("english")

nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()


header = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}
def removeStopWords(sentence):
  stop_words = set(stopwords.words('english'))
  word_tokens = word_tokenize(sentence)
  filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words]

  # filtered_sentence to single string
  newSentence = ""

  for word in filtered_sentence:
    newSentence += word + " "

  newSentence = newSentence.translate(newSentence.maketrans("", "", string.punctuation + "“”’0123456789"))

  return newSentence


def stemSentence(sentence):
  token_words=word_tokenize(sentence)
  stem_sentence=[]
  for word in token_words:
    w = (wordnet_lemmatizer.lemmatize(word, pos="n"))
    stem_sentence.append(englishStemmer.stem(w))
    stem_sentence.append(" ")
  return "".join(stem_sentence)

def tokenizeThreatPost(url):
  data = requests.get(url, headers = header).text
  new_soup = BeautifulSoup(data, "lxml")
  #body = new_soup.find_all("div", itemprop = "articleBody")

  body=""
  for div in new_soup.find_all('div', class_='c-article__content js-reading-content'):
    for p in div.find_all(['p','h2'])[:-1]:
        body = body + (p.text)
  return body
'''''
  newsText = ""

  for txt in body:
    newsText += txt.strip()
  
  newsText = newsText.translate(newsText.maketrans("", "", string.punctuation + "“”0123456789"))

  sentence = removeStopWords(newsText)
  sentence = stemSentence(sentence)
  return sentence
'''
  # return sentence.split(" ")
  # return tokenize([sentence])


def scrapeThreatPost(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")

  dic = {} 
  dic["title"] = soup.find("h1", class_= "c-article__title").text
  dic["first paragraph"] = soup.find("div", class_="c-article__intro").text
  dic["url"] = url

  date_string = soup.find("div", class_="c-article__time").find("time").get("datetime").split('T')[0]
  dic["date"] = date_string if len(date_string)!= "" else "No Date"   

  dic["stemmed text"] = tokenizeThreatPost(url)
  #print(dic)


scrapeThreatPost("https://threatpost.com/cisco-network-breach-google/180385/")
