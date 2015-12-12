# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 01:26:00 2015

@author: Jigar Mehta
"""
import pandas as pd
from pandas.io.json import json_normalize
from bson import json_util, ObjectId
import json
import glob
from pymongo import MongoClient

def mongo_to_dataframe(mongo_data):
    
            sanitized = json.loads(json_util.dumps(mongo_data))
            normalized = json_normalize(sanitized)
            df = pd.DataFrame(normalized)
    
            return df
    
cl = MongoClient()
db = cl.test
    
cursora = db.ebay.find()
eb1=mongo_to_dataframe(cursora)
eb1.shape

cursorb = db.amaz.find()
db1=mongo_to_dataframe(cursorb)
db1.shape

db1=db1[db1['lang']=='en']
db1.shape

eb1=eb1[eb1['lang']=='en']
eb1.shape

terms_all=[]
# Amazon - Top parameters
from nltk import bigrams
#Top Keywords
from nltk.corpus import stopwords
from nltk import bigrams 
import string
import re
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
    
punctuation = list(string.punctuation)
stop=stopwords.words('english') + punctuation
stop=stop+ ['Read','ebay','Ebay','eBay','10','Please','8','16','7','Now','Only', 'New', 'GB','4',\
            'NEW','5','6','\u2026','HOLY','25','Gift','pm','2','1','Entire','follows','d83d','6.00','A',\
            'give','dogs','dog','amp','The','I','away','person','giving','one','random','tweet','rt','50',\
            'EST','3','RTs','RT','\u2026','Amazon','Clinton', 'via']


'''terms_all=[]            
for text in db1['text']:
    for term in preprocess(text):
        if term not in stop and not term.startswith(('@','#','http','https')):
            terms_all.append(term)
print type(terms_all)
terms_all=terms_all[:2000]
s=set(terms_all)
print (terms_all)
print s'''



open("data_e.txt", "w").write("\n".join(("\t".join(item)) for item in out))

import os
lst=os.listdir("C:\\txt_sentoken\\neg")
print lst
neg_tweets=[]
for i in range(0,len(lst)):
    path="C:\\txt_sentoken\\neg\\"+lst[i]
    print path
    input=open(path, "r")      
    for line in input:
        neg_tweets.append((line,"negative"))
    input.close()    
#print neg_tweets  

import os
lst=os.listdir("C:\\txt_sentoken\\pos")

pos_tweets=[]
for i in range(0,len(lst)):
    path="C:\\txt_sentoken\\pos\\"+lst[i]
    print path
    input=open(path, "r")      
    for line in input:
        pos_tweets.append((line,"positive"))
    input.close()    
#print pos_tweets


   
tweets = []

import nltk

for (words, sentiment) in pos_tweets + neg_tweets:
    #if words not in stop:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        if words not in stop:
            all_words.extend(words)
    return all_words
    
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    print wordlist
    word_features = wordlist.keys()
    return word_features
    
word_features = get_word_features(get_words_in_tweets(tweets))
#print word_features

def extract_features(document):

    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
training_set = nltk.classify.apply_features(extract_features, tweets)
#print training_set

classifier = nltk.NaiveBayesClassifier.train(training_set)

from  collections import Counter

out_a=[]
c2=db1[:500]
for tweet in c2['text']:
    o=classifier.classify(extract_features(preprocess(tweet)))
    if o=="positive":
        #creating learning model by feeding output
        input=open("C:\\txt_sentoken\\pos\\Learningset1.txt", "a")
        
        input.write(tweet.encode('utf-8'))
        
        input.write("\n")
    else:
        #creating learning model by feeding output
        input=open("C:\\txt_sentoken\\neg\\Learningset1.txt", "a")
        input.write(tweet.encode('utf-8'))
        input.write("\n")
        
    out_a.append(o)
    #tempList.append([tweet,out])
    #print classifier.show_most_informative_features(32) 

o_a=Counter(out_a)
print (o_a)
input.close()

out=[]
c1=eb1[:500]
for text in c1['text']:
    o=classifier.classify(extract_features(preprocess(tweet)))
    if o=="positive":
        #creating learning model by feeding output
        input=open("C:\\txt_sentoken\\pos\\Learningset.txt", "a")
        
        input.write(tweet.encode('utf-8'))
        
        input.write("\n")
    else:
        #creating learning model by feeding output
        input=open("C:\\txt_sentoken\\neg\\Learningset.txt", "a")
        input.write(tweet.encode('utf-8'))
        input.write("\n")
    out.append(o)
    
cou=Counter(out)
print cou
input.close()
  

























import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
    
dfh.shape
print(preprocess("RT @realDonaldTrump: Hillary Clinton is weak"))
(dfh['text'])

dfh['text'].astype(basestring)
dfh.dtypes
for tw in dfh['text']:
    dfh['text'].=preprocess(tw)
    
