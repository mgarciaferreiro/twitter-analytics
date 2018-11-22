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
#import matplotlib.pyplot as plt
#import pandas as pd

from authorization import cons_tok #import variables from module which defines them
from authorization import cons_sec
from authorization import app_tok
from authorization import app_sec

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)
    twitter_api = tweepy.API(auth)
    
    csvFile = open('results_trump.csv','a')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["username","author id","created", "text", "retwc", "hashtag", "followers", "friends","polarity","subjectivity"])

    searchresults = tweepy.Cursor(twitter_api.search, q = "Trump", lang = "en").items(300)
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
    

    