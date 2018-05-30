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
languages = ["en", "th"]
longlat = [100.484605,13.685780,100.584605,13.785780] 
# ------- EDIT -------- #
tweet_list=set()

def writefile(tweet):
    f = open(label+'_tweets.txt','a')
    tweet_id = tweet.id_str
    if tweet_id not in tweet_list: 
        tweet_list.add(tweet_id)
        tweet_user_id = tweet.user.id_str
        tweet_user = tweet.user.screen_name
        tweet_text = str(tweet.text).encode("CP874", "ignore").decode("CP874")
        tweet_text = tweet_text.replace('\n', ' ')
        tweet_time = str(tweet.created_at).encode("CP874", "ignore").decode("CP874")
        tweet_lang = str(tweet.lang).encode("CP874", "ignore").decode("CP874")
        tweet_coord = tweet.coordinates
        geo = str(tweet_coord).encode("CP874", "ignore").decode("CP874")
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
            location = str(tweet.place.name).encode("CP874", "ignore").decode("CP874")
            locat_sw = str(tweet.place.bounding_box.coordinates[0][0])[1:-1].encode("CP874", "ignore").decode("CP874")
            locat_ne = str(tweet.place.bounding_box.coordinates[0][2])[1:-1].encode("CP874", "ignore").decode("CP874")

        tweet_with_time_and_geo = tweet_user_id + "\t" + tweet_user + "\t" + tweet_id + "\t" + tweet_text + "\t" + tweet_time + "\t" + latitude + "\t" + longitude + "\t" + location + "\t" + locat_sw + "\t" + locat_ne + "\t" + tweet_lang + "\n" 

        f.write(tweet_with_time_and_geo.encode("CP874", "ignore").decode("CP874"))
    f.close()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print("text: ", status.text, str(status.text).encode("CP874", "ignore").decode("CP874"))
        writefile(status)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return 
        else:
            print('ok')

        # returning non-False reconnects the stream, with backoff.

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(locations=longlat, languages=languages, async=True)
