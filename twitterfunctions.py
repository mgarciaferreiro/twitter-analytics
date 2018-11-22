#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:21:16 2018

@author: Marta
"""
import json
import twitter

def oauth_login():
    
    CONSUMER_KEY = "insert your own key"
    CONSUMER_SECRET = "insert your own key"
    OAUTH_TOKEN = "insert your own key"
    OAUTH_TOKEN_SECRET = "insert your own key"
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

twitter_api = oauth_login()

def twitter_trends(twitter_api, woe_id):
    return twitter_api.trends.place(_id=woe_id)
WORLD_WOE_ID = 1
world_trends = twitter_trends(twitter_api, WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)
print (json.dumps(world_trends, indent=1))

world_trends_set = set([trend['name'] 
                        for trend in world_trends[0]['trends']])

us_trends_set = set([trend['name'] 
                     for trend in us_trends[0]['trends']]) 

common_trends = world_trends_set.intersection(us_trends_set)

print (common_trends)
