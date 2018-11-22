#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:21:16 2018

@author: Marta
"""
import json
import twitter

def oauth_login():
    
    CONSUMER_KEY = "0rT72yTC7BBlYQEBg0McfY4a9"
    CONSUMER_SECRET = "Fa3c9sl2CFZlpx9nKlvcFgyC1KBL7FXSOovX8nv5XGJSmYHYfd"
    OAUTH_TOKEN = "918270670982860801-aS6iKtxCL8DUJNMGRTj3BJfPf3vs3m9"
    OAUTH_TOKEN_SECRET = "8SrXgXCAaSAj5yhs1x37KdD3c0AqJwLTIMKoNBq7R3vPy"
    
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