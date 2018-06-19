# -*-  coding: utf-8 -*-
import tweepy
import time
import sys
import json
import datetime
import re
import os
from mtranslate import translate

CONSUMER_KEY = 'DvgGYj5LHwUc3dc2JKGdfETfc'
CONSUMER_SECRET = 'qJYyFfJ6YdnbXHLp4E1as7AiVezdjRd2oNq0KiZ9W4OFJbeDof'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
ACCESS_TOKEN = '141266322-B0rmRdtC6nwrXBYtabc1gq2HPD27lub0ovVozCAq'
ACCESS_SECRET = 'xXZB9MVWAplVo1giItnd3j0mgRsISNlbLyjjvXEbMp536'
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# ------- EDIT -------- #
#query1 = 'こんにちわ'
#query = ["Bangkok"]
label = "HAM_de-en"
languages = ["en", "de"]
longlat = [9.943682,53.501085,10.043682,53.601085]
# ------- EDIT -------- #
tweet_list=set()

def writefile(tweet):
    f = open(label+'_tweets.txt','a',encoding='utf-8')
    tweet_id = tweet.id_str
    if tweet_id not in tweet_list:
        tweet_list.add(tweet_id)
        tweet_user_id = tweet.user.id_str
        tweet_user = tweet.user.screen_name
        tweet_text = str(tweet.text).encode("utf_8", "ignore").decode("utf_8")
        tweet_text = tweet_text.replace('\n', ' ')
        tweet_text_trans = translate(tweet_text, 'en')
        tweet_time = str(tweet.created_at).encode("utf_8", "ignore").decode("utf_8")
        tweet_lang = str(tweet.lang).encode("utf_8", "ignore").decode("utf_8")
        tweet_reply_id = tweet.in_reply_to_status_id_str if tweet.in_reply_to_status_id_str != None else '-1'
        tweet_reply_user_id = tweet.in_reply_to_user_id_str if tweet.in_reply_to_user_id_str != None else '-1'
        tweet_reply_username = tweet.in_reply_to_screen_name if tweet.in_reply_to_screen_name != None else '-1'
        tweet_coord = tweet.coordinates
        geo = str(tweet_coord).encode("utf_8", "ignore").decode("utf_8")
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
            location = str(tweet.place.name).encode("utf_8", "ignore").decode("utf_8")
            location_trans = translate(location, 'en')
            locat_sw = str(tweet.place.bounding_box.coordinates[0][0])[1:-1].encode("utf_8", "ignore").decode("utf_8")
            locat_ne = str(tweet.place.bounding_box.coordinates[0][2])[1:-1].encode("utf_8", "ignore").decode("utf_8")

        #tweet_with_time_and_geo = tweet_user_id + "\t" + tweet_user + "\t" + tweet_id + "\t" + tweet_text + "\t" + tweet_time + "\t" + latitude + "\t" + longitude + "\t" + location + "\t" + locat_sw + "\t" + locat_ne + "\t" + tweet_lang + "\n"
        tweet_with_time_and_geo = tweet_user_id + "\t" + tweet_user + "\t" + tweet_id + "\t" + tweet_text + "\t" + tweet_text_trans + "\t" + tweet_time + "\t" + latitude + "\t" + longitude + "\t" + location+ "\t" + location_trans + "\t" + locat_sw + "\t" + locat_ne + "\t" + tweet_reply_id + "\t" + tweet_reply_user_id + "\t" + tweet_reply_username + "\t" + tweet_lang + "\n"

        f.write(tweet_with_time_and_geo.encode("utf_8", "ignore").decode("utf_8"))
    f.close()

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print("text: ", status.text)
        writefile(status)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            print('limit break')
            return

        # returning non-False reconnects the stream, with backoff.

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(locations=longlat, languages=languages, async=True)

