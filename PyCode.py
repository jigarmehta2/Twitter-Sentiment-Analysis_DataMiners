# -*- coding: utf-8 -*-
"""
Created on Sat Dec 05 15:13:32 2015

@author: Jigar Mehta
"""

# import packages and modules
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.tokenize import word_tokenize

import json
import pandas as pd
import matplotlib.pyplot as plt

#define twitter API access connection parameters
a=0
#Variables that contains the user credentials to access Twitter API 
access_token = "4124694807-9UnjCCudHbNThtLlQjwNFRjBBTwdL5AvTroOcKi"
access_token_secret = "CYyJfefmmByIoSk7smJD0E7V2y0wjVrszWCA7Mdm46ZCQ"
consumer_key = "3Z8Tyk9X6PPwghK4qFEy9tVYH"
consumer_secret = "v8PdHTg3pxuj8RrWUXhUGib4RBvSrBebUE57dEvrPvpKfbk5km"

#Twitter data streaming class
class StdOutListener(StreamListener):
    
    def on_data(self, data):
        try:
            global a
            if a<12000:
                with open('p_hil_new.json', 'a') as f:
                    f.write(data)
                    a=a+1
                    print a
                    return True
            else:
                return False
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print status
        return True

# main class
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords:
    #stream.filter(track=['Donald Trump'])
    stream.filter(track=['Hillary Clinton'])

# read tweets data file 
tweets_data_path = "C:\Users\Jigar Mehta\Desktop\p_hil_n.json"

tweets_data = []
tweets_file = open("p_isis.json", "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
    
# print the number of tweets in the file   
print len(tweets_data)

# print twitter data
'''with open('p_hil_n.json', 'r') as f:
    line = f.readline() # read only the first tweet/line
    tweet = json.loads(line) # load it as Python dict
    print(json.dumps(tweet, indent=4)) # pretty-print '''

# tokenization
#import regex
import re

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end

from nltk.corpus import stopwords
from nltk import bigrams 
import string
 
punctuation = list(string.punctuation)
stop=stopwords.words('english') + punctuation 
stop=stop+ ['Read','ebay','Ebay','eBay','10','Please','8','16','7','Now','Only', 'New', 'GB','4',\
            'NEW','5','6','\u2026','HOLY','25','Gift','pm','2','1','Entire','follows','d83d','6.00','A',\
            'give','dogs','dog','amp','The','I','away','person','giving','one','random','tweet','rt','50',\
            'EST','3','RTs','RT','\u2026','Amazon','Clinton', 'via']
#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stop or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end

#start extract_features
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in featureList:
        features['contains(%s)' % word] = (word in tweet_words)
    return features
#end
'''    
tweets=[( pvocabulary,'positive'),
        (nvocabulary,'negative')]
''' 
tweets = [(['love', 'this', 'car'], 'positive'),
    (['this', 'view', 'amazing'], 'positive'),
    (['feel', 'great', 'this', 'morning'], 'positive'),
    (['excited', 'about', 'the', 'concert'], 'positive'),
    (['best', 'friend'], 'positive'),
    (['not', 'like', 'this', 'car'], 'negative'),
    (['this', 'view', 'horrible'], 'negative'),
    (['feel', 'tired', 'this', 'morning'], 'negative'),
    (['not', 'looking', 'forward', 'the', 'concert'], 'negative'),
    (['enemy'], 'negative')]
       
print tweets
featureList = pvocabulary+nvocabulary
print tweets
print feature_list
import nltk
training_set = nltk.classify.util.apply_features(extract_features, tweets)

print(training_set)
classifier = nltk.NaiveBayesClassifier.train(training_set)

tweet = 'sad'
print classifier.classify(extract_features(tweet.split()))


'''
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
NBClassifier
print len(nvocabulary)+len(pvocabulary)
c1=db1[:1000]

out=[]
#for text in c1['text']:
processedTestTweet = processTweet( 'sad unhappy bad jigar')
    #print processedTestTweet
o=   NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))
out.append(o)
print NBClassifier.show_most_informative_features(1)
print out

tweet = 'Your song is annoying'
print classifier.classify(extract_features(tweet.split()))



def train(labeled_featuresets, estimator=ELEProbDist):
    # Create the P(label) distribution
    label_probdist = estimator(label_freqdist)
    # Create the P(fval|label, fname) distribution
    feature_probdist = {}
    return NaiveBayesClassifier(label_probdist, feature_probdist)

'''











