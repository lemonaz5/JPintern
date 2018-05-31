# -*-  coding: utf-8 -*-
import tweepy
import time
import sys
import json
import datetime
import re
import os

CONSUMER_KEY = 'uSejwN4tAXj3B3W3ylmJ1bJva'
CONSUMER_SECRET = 'cQe4OMJnkLyPrrLlah0U4FhH3HyyQb8T23jUTMBCedZK1T8GeU'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = '141266322-Qe0r39hsxzWzcvGgHJQdvYDnhQ93ZVTrWlflaeJN'
ACCESS_SECRET = 'RSKQS2ZkZ0TVlFn4EBLOJJbF4IZxySfeuBH0krGFy7qRw'
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# ------- EDIT -------- #
#query1 = 'こんにちわ'
#query = ["Bangkok"]
label = "BKK_th-en" 
languages = ["en", "jp"]
longlat = [135.685300,34.931461,135.785300,35.031461] 
# ------- EDIT -------- #
tweet_list=set()

def writefile(tweet):
    f = open(label+'_tweets.txt','a',encoding='utf-8')
    tweet_id = tweet.id_str
    if tweet_id not in tweet_list: 
        tweet_list.add(tweet_id)
        tweet_user_id = tweet.user.id_str
        tweet_user = tweet.user.screen_name
        tweet_text = str(tweet.text).encode("CP932", "ignore").decode("CP932")
        tweet_text = tweet_text.replace('\n', ' ')
        tweet_time = str(tweet.created_at).encode("CP932", "ignore").decode("CP932")
        tweet_lang = str(tweet.lang).encode("CP932", "ignore").decode("CP932")
        tweet_reply_id = tweet.in_reply_to_status_id_str if tweet.in_reply_to_status_id_str != None else '-1'
        tweet_reply_user_id = tweet.in_reply_to_user_id_str if tweet.in_reply_to_user_id_str != None else '-1'
        tweet_reply_username = tweet.in_reply_to_screen_name if tweet.in_reply_to_screen_name != None else '-1'
        tweet_coord = tweet.coordinates
        geo = str(tweet_coord).encode("CP932", "ignore").decode("CP932")
        location = "none"
        locat_sw = '-1'
        locat_ne = '-1'
        latitude = '-1'
        longitude = '-1'
        
        if len(geo) > 10:
            ind = geo.find("[")
            ind2 = geo.find("]")
            latlong = geo[ind+1:ind2].split(",")
            longitude = latlong[0]
            latitude = latlong[1]
        if tweet.place != None:
            location = str(tweet.place.name).encode("CP932", "ignore").decode("CP932")
            locat_sw = str(tweet.place.bounding_box.coordinates[0][0])[1:-1].encode("CP932", "ignore").decode("CP932")
            locat_ne = str(tweet.place.bounding_box.coordinates[0][2])[1:-1].encode("CP932", "ignore").decode("CP932")

        #tweet_with_time_and_geo = tweet_user_id + "\t" + tweet_user + "\t" + tweet_id + "\t" + tweet_text + "\t" + tweet_time + "\t" + latitude + "\t" + longitude + "\t" + location + "\t" + locat_sw + "\t" + locat_ne + "\t" + tweet_lang + "\n" 
        tweet_with_time_and_geo = tweet_user_id + "\t" + tweet_user + "\t" + tweet_id + "\t" + tweet_text + "\t" + tweet_time + "\t" + latitude + "\t" + longitude + "\t" + location + "\t" + locat_sw + "\t" + locat_ne + "\t" + tweet_reply_id + "\t" + tweet_reply_user_id + "\t" + tweet_reply_username + "\t" + tweet_lang + "\n" 

        f.write(tweet_with_time_and_geo.encode("CP932", "ignore").decode("CP932"))
    f.close()