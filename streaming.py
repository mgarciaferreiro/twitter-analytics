#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 18:15:00 2018

@author: Marta
"""
import tweepy
import json
#import unidecode
#import csv
#import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from authorization import cons_tok #import variables from module which defines them
from authorization import cons_sec
from authorization import app_tok
from authorization import app_sec

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh': 'Chinese', 'und': 'Undefined'}

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)
    api = tweepy.API(auth)
    L = []
    myStreamListener = MyStreamListener(num_tweets_to_grab=300)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.sample()
    L = list(map(langs.get, L))
    print(Counter(L))
    counts = Counter(L)
    plt.pie([float(v) for v in counts.values()], labels=[str(k) for k in counts.keys()], autopct='%1.1f%%',
        shadow=True, startangle=90)
    plt.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    
class MyStreamListener(tweepy.StreamListener):
    
    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        
    def on_data(self, data):
        try:
            json_data = json.loads(data)
            print(json_data["lang"])
            L.append(json_data["lang"])

            self.counter += 1
            if self.counter >= self.num_tweets_to_grab:
                return False
            return True
        except:
            # @TODO: Very dangerous, come back to this!
            pass
        
    def on_error(self, status):
        print(status)
  
    
#if __name__ == "__main__":
#    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
#    auth.set_access_token(app_tok, app_sec)
#    api = tweepy.API(auth)
#    L = []
#    myStreamListener = MyStreamListener(num_tweets_to_grab=300)
#    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#    myStream.sample()
#    L = list(map(langs.get, L))
#    print(Counter(L))
#    counts = Counter(L)
#    plt.pie([float(v) for v in counts.values()], labels=[str(k) for k in counts.keys()], autopct='%1.1f%%',
#        shadow=True, startangle=90)
#    plt.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle.
#    plt.show()