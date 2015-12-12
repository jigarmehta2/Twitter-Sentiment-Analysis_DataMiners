# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 01:20:46 2015

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
            while a<50:
                with open('p_demo.json1', 'a') as f:
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

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['eBay'])
    stream.filter(track=['Amazon'])

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

# tokenization over
from nltk.corpus import stopwords
from nltk import bigrams 
import string
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt','RT','u\2026','Hillary','Clinton', 'via']
    
import operator 
from collections import Counter
 
fname = 'p_hil_n.json'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_only = [term for term in preprocess(tweet['text']) 
              if term not in stop and
              not term.startswith(('@'))] 
              # mind the ((double brackets))
              # startswith() takes a tuple (not a list) if 
              # we pass a list of inputs

        # Update the counter
        
 
        terms_bigram = bigrams(terms_stop)
        count_all.update(terms_bigram)
    # Print the first 5 most frequent words
    print(count_all.most_common(15)),
        
tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['created_at'] = map(lambda tweet: tweet['created_at'], tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets' , fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')