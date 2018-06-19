import pandas as pd
from mtranslate import translate
import pickle

#path = r'C:\Users\sociocom\Desktop\Crawler\backup\31May-4June 2018'
#path = r"/home/wannita/crawler/backup/14-15June2018"
filename = "kyoto_all"

def save_obj(file, obj):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)

def load_obj(file):
    with open(file, 'rb') as f:
        return pickle.load(f)

df = load_obj(filename)
df['place'] = df['place'].apply(lambda x: translate(x,'en'))
df['text'] = df['text'].apply(lambda x: translate(x,'en'))
save_obj("kyoto_all_trans", df)
