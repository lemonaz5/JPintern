import pandas as pd
from mtranslate import translate
import pickle

path = r'C:\Users\sociocom\Desktop\Crawler\backup\playing'
#path = r"/home/wannita/crawler/backup/playing"

def save_obj(file, obj):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(file, obj):
    with open(file, 'rb') as f:
        obj = pickle.load(f)

def open_to_pandas(spath):
    tweets = open(spath, "r", encoding="utf-8")
    tweets_list = []
    for line in tweets:
        tweets_list.append(line.split('\t'))
    labels = ['acc_id','acc','tweet_id','text','text_trans','created_time','ex_lat','ex_long','place','place_trans','lot_sw','lot_ne','tweet_reply_id','tweet_reply_user_id','tweet_reply_username','lang']
    name = pd.DataFrame(tweets_list,columns=labels)
    filt = ((name["lang"] == "th\n") | (name["lang"] == "en\n") | (name["lang"] == "ja\n") | (name["lang"] == "de\n") | (name["lang"] == "pt\n"))
    name = name[filt]
    name['lang'] = name['lang'].apply(lambda x: x.strip())
    print("all data :" ,len(name), "tweets")
    return name

print("1: SFC\n 2: HAM\n 3: SPL\n 4: KYT\n 5: BKK\n")
print("Input file name (with .txt): ")
name = str(input())
if name == "5":
    name = "BKK_th-en_tweets.txt"
elif name == "4":
    name = "KYT_ja-en_tweets.txt"
elif name == "3":
    name = "SPL_pt-en_tweets.txt"
elif name == "2":
    name = "HAM_de-en_tweets.txt"
elif name == "1":
    name = "SFC_en_tweets.txt"
print("Output file name: ")
out_name = str(input())
if out_name == "5":
    out_name = "translated_bkk_tweet"
elif out_name == "4":
    out_name = "translated_kyt_tweet"
elif out_name == "3":
    out_name = "translated_spl_tweet"
elif out_name == "2":
    out_name = "translated_ham_tweet"
elif out_name == "1":
    out_name = "translated_sfc_tweet"
df_bkk = open_to_pandas(path + "\\" + name)

save_obj(path + "\\" + out_name, df_bkk)
