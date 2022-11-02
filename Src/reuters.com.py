from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import nltk
import string

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer

nltk.download('wordnet')
nltk.download('omw-1.4')
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
}

englishStemmer = SnowballStemmer("english")

wordnet_lemmatizer = WordNetLemmatizer()


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
    token_words = word_tokenize(sentence)
    stem_sentence = []
    for word in token_words:
        w = (wordnet_lemmatizer.lemmatize(word, pos="n"))
        stem_sentence.append(englishStemmer.stem(w))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def tokenizeReuters(url):
    data = requests.get(url, headers=header).text
    new_soup = BeautifulSoup(data, "lxml")
    body = ""
    for div in new_soup.find_all("div", class_="article-body__content__17Yit paywall-article"):
        for p in div.find_all('p'):
            print(p.find_all("data-testid"))
            # if "paragraph" is in :
            # body = body + p.text
    return body


def scrapeReuters(url):
    html_text = requests.get(url, headers=header).text
    soup = BeautifulSoup(html_text, "lxml")
    dic = {}
    dic["title"] = soup.find("h1",
                             class_="text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_2__1K_hh heading__base__2T28j heading__heading_2__3Fcw5").text
    # dic["first paragraph"] = soup.find("div", class_="article-body__content__17Yit paywall-article").find("p").text
    dic["raw text"] = tokenizeReuters(url)
    dic["stemmed text"] = {}
    print(dic)
    return dic


# edit json file
jsonFile = open("../packet_storm.json", "r+")
packet_storm = json.load(jsonFile)
reuters_news = packet_storm["Reuters"]
for url in reuters_news:
    scrapeReuters(url)

jsonFile.seek(0)
# convert back to json.
json.dump(packet_storm, jsonFile, indent=2)

jsonFile.close()
