import nltk
import string

nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('wordnet')
nltk.download('omw-1.4')


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

def formatText(sentence):
   newSentence = removeStopWords(sentence)
   return stemSentence(newSentence)