# -*- coding: utf-8 -*-
import json
import pandas as pd
from time import sleep
from requests_oauthlib import OAuth1Session
from datetime import datetime
from api_keys import *

#---------------------------------------------------------------
# API keys
#---------------------------------------------------------------
Consumer_key = CONSUMER_KEY
Consumer_secret = CONSUMER_SECRET
Access_token = ACCESS_TOKEN
Access_secret = ACCESS_SECRET
twitter = OAuth1Session(Consumer_key, Consumer_secret, Access_token, Access_secret)


#---------------------------------------------------------------
# search function
#---------------------------------------------------------------
def search(keyword = " ", count = 100, loop = 200):
    cnt=0
    max_id = -1
    url = "https://api.twitter.com/1.1/search/tweets.json"
    columns = ["time", "tweet"]
    df = pd.DataFrame(columns = columns)
    
    if keyword == " ":
        return df
    
    params = {"q" : keyword, "count" : count, "max_id" : max_id}
    while True:
        # loop_check
        if cnt >= loop:
            print("loop_end")
            break

        # max_id for the next request
        if max_id != -1:
            params["max_id"] = max_id - 1
        
        # make a request
        req = twitter.get(url, params = params)

        # the request is accepted
        if req.status_code == 200:
            timeline = json.loads(req.text)

            if timeline["statuses"] == []:
                print("no more tweets")
                break

            for tweet in timeline["statuses"]:
                text = tweet["text"]
                time = tweet["created_at"]
                
                df = df.append(pd.DataFrame([[time, text]], columns=columns), ignore_index=True)
            
            max_id = timeline["statuses"][-1]["id"]
            # count
            cnt+=1
            print("loop_count : ", str(cnt))
        
        # wait for 15 min if the request is rejected
        else:
            print("Wait for 15minutes from: " +  datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            sleep(60*16)

    twitter.close()
    return df