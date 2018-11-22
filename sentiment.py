#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 09:55:49 2018

@author: Marta
"""

from textblob import TextBlob
import csv
import tweepy
import unidecode
import matplotlib.pyplot as plt
import pandas as pd

from authorization import cons_tok #import variables from module which defines them
from authorization import cons_sec
from authorization import app_tok
from authorization import app_sec

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)
    twitter_api = tweepy.API(auth)
    
    csvFile = open('results_catalonia.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["username","author id","created", "text", "retwc", "hashtag", "followers", "friends","polarity","subjectivity"])
    counter = 0
    
    
    searchresults = tweepy.Cursor(twitter_api.search, q = "Catalonia", lang = "en").items(100)
    for tweet in searchresults:
        created = tweet.created_at
        text = tweet.text
        text = unidecode.unidecode(text) 
        retwc = tweet.retweet_count
        try:
            hashtag = tweet.entities[u'hashtags'][0][u'text']
        except:
            hashtag = "None"
        username  = tweet.author.name
        authorid  = tweet.author.id              
        followers = tweet.author.followers_count 
        friends = tweet.author.friends_count     

        text_blob = TextBlob(text)
        polarity = text_blob.polarity
        subjectivity = text_blob.subjectivity
        csvWriter.writerow([username, authorid, created, text, retwc, hashtag, followers, friends, polarity, subjectivity])

    csvFile.close()
    
    twitter_data = pd.read_csv('results_catalonia.csv')
    print(twitter_data.corr())
    
    twitter_data_subjective = twitter_data[twitter_data['subjectivity']>0.5]
    print(twitter_data_subjective.corr())
    plt.scatter(twitter_data_subjective.retwc,twitter_data_subjective.polarity)
    