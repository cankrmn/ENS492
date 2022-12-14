import nltk
import contractions
import inflect
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import re, string
from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


nltk.download('punkt')
nltk.download('wordnet')

def url_remover(data): # remove any url in text
  return re.sub(r'https?\S+','',data)

def web_associated(data):
  text = url_remover(text)
  return text

# -------------------------------

def remove_round_brackets(data): # remove anything between two round brackets
   return re.sub('\(.*?\)','',data)

punctList = string.punctuation + '“”' 
def remove_punc(data): # remove any punctuation
  trans = str.maketrans('','', punctList)
  return data.translate(trans)

def remove_emojis(data): # remove any emojis
   emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
   return emoji_pattern.sub(r'', data) # no emoji

def white_space(data): # remove any double or more space
  return ' '.join(data.split())

def complete_noise(data):
  new_data = remove_round_brackets(data)
  new_data = remove_punc(new_data)
  new_data = remove_emojis(new_data)
  new_data = white_space(new_data)
  return new_data

# -------------------------------
def text_lower(data): # make every letter lowercase
  return data.lower()

def contraction_replace(data): # fix contractions (e.g. won't => will not)
  return contractions.fix(data)

def number_to_text(data): # write numbers as text and return (...12... => ...twelve...)
  temp_str = data.split()
  string = ""
  for i in temp_str:
    if i.isdigit(): # if the word is digit, converted to 
      temp = inflect.engine().number_to_words(i)
      string += temp + " "
    else:
      string += i + " "
  return string.strip()

def normalization(data):
  text = text_lower(data)
  text = number_to_text(text)
  text = contraction_replace(text)
  tokens = nltk.word_tokenize(text)
  return tokens

# -------------------------------

def stopword(data): # remove stopwords
  clean = []
  for i in data:
    if i not in stopwords.words('english'):
      clean.append(i)
  return clean

def stemming(data): # stem the text
  stemmer = LancasterStemmer()
  stemmed = []
  for i in data:
    stem = stemmer.stem(i)
    stemmed.append(stem)
  return stemmed

def lemmatization(data): # lemmatize the text
  lemma = WordNetLemmatizer()
  lemmas = []
  for i in data:
    lem = lemma.lemmatize(i, pos='v')
    lemmas.append(lem)
  return lemmas  

def final_process(data):
  stopwords_remove = stopword(data)
  stemmed = stemming(stopwords_remove)
  lemm = lemmatization(stopwords_remove)
  return stemmed, lemm

# -------------------------------

def preprocess(data = ""): # run all preprocessing functions
  txt = url_remover(data)
  txt = complete_noise(txt)
  txt = normalization(txt)
  stemmed, lemm = final_process(txt)
  return stemmed, lemm