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

def tokenizeTheHackerNews(url):
  data = requests.get(url, headers = header).text
  new_soup = BeautifulSoup(data, "lxml")
  #body = new_soup.find_all("div", itemprop = "articleBody")

  body=""
  for div in new_soup.find_all('div', id='articlebody'):
    for p in div.find_all('p'):
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


def scrapeTheHackerNews(url):
  html_text = requests.get(url, headers = header).text
  soup = BeautifulSoup(html_text, "lxml")

  dic = {} 
  dic["title"] = soup.find("h1", class_= "story-title").text
  dic["first paragraph"] = soup.find('div', id='articlebody').find('p').text
  dic["url"] = url

  date_string = soup.find("span", class_="author").text.replace(',', '').replace(' ', '-')
  dic["date"] = str(datetime.strptime(date_string, '%B-%d-%Y').date()) if len(date_string)!= "" else "No Date"   

  dic["stemmed text"] = tokenizeTheHackerNews(url)
  #print(dic["date"])


scrapeTheHackerNews("https://thehackernews.com/2022/10/russian-hacker-arrested-in-india-for.html")
