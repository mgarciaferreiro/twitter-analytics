#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:07:44 2018

@author: Marta
"""

import tweepy
from textblob import TextBlob
import csv
import unidecode
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
import os
import json
from collections import Counter

from authorization import cons_tok #import variables from module which defines them
from authorization import cons_sec
from authorization import app_tok
from authorization import app_sec

from flask import Flask, request, render_template
app = Flask(__name__)

GRAPH_FOLDER = os.path.join('static', 'graphs')
app.config['UPLOAD_FOLDER'] = GRAPH_FOLDER

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh': 'Chinese', 'und': 'Undefined'}
L=[]

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(cons_tok, cons_sec)
    auth.set_access_token(app_tok, app_sec)
    api = tweepy.API(auth)

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
            pass
        
    def on_error(self, status):
        print(status)
        
@app.route("/") 
def main():
    username = api.me().name
    myfollowers = api.me().followers_count
    mylocation = api.me().location
    welcome = "Welcome " + username + "! You have " + str(myfollowers) + " followers. " + "How's the weather in " + mylocation + "?"
    return render_template("main.html", welcome=welcome)

@app.route("/search") 
def search():
    return render_template("search.html")

@app.route("/search", methods=['POST']) 
def getquery():
    text = request.form['text']
    query = text.upper()
    
    csvFile = open('results.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["username","author id","created", "text", "retwc", "hashtag", "followers", "friends","polarity","subjectivity"])

    searchresults = tweepy.Cursor(api.search, q = query, lang = "en").items(50)
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
    twitter_data = pd.read_csv('results.csv')
    polarities = twitter_data['polarity']
    avpol = sum(polarities)/len(polarities)
    
    tweets = twitter_data['text']
    
    # join tweets to a single string
    words = ' '.join(tweets)
    # remove URLs, RTs, and twitter handles
    no_urls_no_tags = " ".join([word for word in words.split()
                                if 'http' not in word
                                    and not word.startswith('@')
                                    and word != 'RT'
                                ])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='black', width=1800, height=1400).generate(no_urls_no_tags)
    plt.imshow(wordcloud)
    plt.axis('off')
    cloudname = datetime.now().strftime('wordcloud_%H_%M_%d_%m_%Y.log')
    plt.savefig('static/graphs/' + cloudname + '.png', dpi=300, bbox_inches='tight')
    fullcloudname = os.path.join(app.config['UPLOAD_FOLDER'], cloudname + '.png')
    return render_template("search.html", query=query, fullcloudname=fullcloudname, avpol=avpol)

@app.route("/languages")
def languages():
    myStreamListener = MyStreamListener(num_tweets_to_grab=300)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.sample()
    global L 
    L = list(map(langs.get, L))
    print(Counter(L))
    counts = Counter(L)
    plt.pie([float(v) for v in counts.values()], labels=[str(k) for k in counts.keys()], autopct='%1.1f%%',
        shadow=False, startangle=90)
    plt.axis("equal") # Equal aspect ratio ensures that pie is drawn as a circle.
    langgraph = datetime.now().strftime('graph_%H_%M_%d_%m_%Y.log')
    plt.savefig('static/graphs/' + langgraph + '.png', dpi=300, bbox_inches='tight')
    fulllanggraph = os.path.join(app.config['UPLOAD_FOLDER'], langgraph + '.png')
    return render_template("languages.html", fulllanggraph=fulllanggraph)    

@app.route("/trends")
def trends():
    spaintrends = api.trends_place(23424950)
    worldtrends = api.trends_place(1)
    world_trends_set = set([trend['name'] 
                     for trend in worldtrends[0]['trends']])
    
    spain_trends_set = set([trend['name'] 
                     for trend in spaintrends[0]['trends']]) 
    
    common_trends = list(world_trends_set.intersection(spain_trends_set))
    return render_template("trends.html", common_trends=common_trends)
    
if __name__ == "__main__":
    app.debug = True
    app.run(debug = True)
