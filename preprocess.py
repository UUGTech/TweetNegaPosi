# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import pickle
import MeCab
import neologdn
import itertools
import emoji
import re
import sys
import os
from constant import *
from collections import Counter

#---------------------------------------------------------------
# eliminate emoji and some noises
#---------------------------------------------------------------
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')
def normalize(tweets):
    normalized_tweets = []
    for tweet in tweets:
        normalized_tweets.append(neologdn.normalize(tweet))
    return normalized_tweets

def eliminate_emoji(tweets):
    tweets_without_emoji = []
    for tweet in tweets:
        tweet.translate(non_bmp_map)
        tweets_without_emoji.append(''.join(['' if c in emoji.UNICODE_EMOJI else c for c in tweet]))
    return tweets_without_emoji

def eliminate_noise(tweets):
    tweets_without_noise = []
    for tweet in tweets:
        tweet = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "", tweet)
        tweet = re.sub(r"　", " ", tweet)
        tweets_without_noise.append(tweet)
    return tweets_without_noise

def clean(tweets):
    cleaned_tweets = eliminate_emoji(tweets)
    cleaned_tweets = normalize(cleaned_tweets)
    cleaned_tweets = eliminate_noise(cleaned_tweets)
    return cleaned_tweets


#---------------------------------------------------------------
# make dataframe from pkl data
#---------------------------------------------------------------
def make_df(pklname, label):
    f = open(pklname, "rb")
    df = pickle.load(f)
    f.close()
    df_2 = pd.DataFrame([label]*len(df), columns=["label"])
    df = pd.concat([df_2, df["tweet"]], axis=1)
    return df
    
    
#---------------------------------------------------------------
# digitize tweets
#---------------------------------------------------------------
# split tweets using neologd
def split_word(tagger, t):
    tagger.parse("")
    words = tagger.parse(t).split(" ")
    return words

# padding
def padding(tweets):
    padded_tweets = []
    for i in range(len(tweets)):
        t = tweets[i]
        padded_tweets.append(t + ["<PAD/>"] * (MAX_LENGTH_OF_TWEETS - len(t)))
    return padded_tweets

# digitization
def tweets_digitization(tweets):
    mt = MeCab.Tagger("-Owakati -d ./mecab-ipadic-neologd")
    tweets = [split_word(mt, t) for t in tweets]
    tweets = padding(tweets)

    ctr = Counter(itertools.chain(*tweets))
    dictionaries = [c[0] for c in ctr.most_common()]
    dictionaries_inv = {c:i for i, c in enumerate(dictionaries)}

    vocab_size = len(dictionaries)
    data = [[dictionaries_inv[w] for w in t] for t in tweets]
    data = np.array(data)

    f = open(VOCAB_DICT_PATH, "wb")
    pickle.dump(dictionaries, f)
    f.close()
    
    return data, vocab_size


#---------------------------------------------------------------
# load_data
#---------------------------------------------------------------
def load_data_with_labels():
    tweets, labels, vocab_size = main()
    return tweets, labels, vocab_size


#---------------------------------------------------------------
# main function
#---------------------------------------------------------------
def main():
    df = pd.DataFrame(columns=["label", "tweet"])
    for f in TWEETS_PKLFILES:
        df = df.append(make_df(f[0], f[1]), ignore_index=True)
    tweets = df["tweet"].values
    tweets = clean(tweets)
    tweets, vocab_size = tweets_digitization(tweets)
    tweets = tweets.astype(np.float32)
    labels = np.array(df["label"].values).astype(np.float32)
    
    # save
    f = open("data_with_labels.pkl", "wb")
    pickle.dump([tweets, labels, vocab_size], f)
    f.close()
    
    return tweets, labels, vocab_size
    


if __name__ == "__main__":
    main()