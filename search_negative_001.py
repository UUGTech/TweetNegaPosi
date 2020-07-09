# -*- coding: utf-8 -*-
import tweet_search
import pandas as pd
import pickle

#---------------------------------------------------------------
# main function 
#---------------------------------------------------------------
def main():
    exclude_positive_emoji = " -\"😀\" -\"😁\" -\"😂\" -\"🤣\" -\"😃\" -\"😄\" \
                                -\"😅\" -\"😆\" -\"😉\" -\"😊\" -\"😋\" -\"😎\" \
                                -\"😍\" -\"😘\" -\"🥰\" -\"😙\" -\"😚\" -\"🙂\" \
                                -\"🤩\" -\"🤗\""

    # search with 👎
    keyword = "👎 lang:ja -filter:links -filter:replies -filter:images exclude:retweets" + exclude_positive_emoji
    df = tweet_search.search(keyword=keyword)

    # save as pickle file
    f = open("negative_001.pkl", "wb")
    pickle.dump(df, f)
    f.close()

    print("saved negative_002.pkl")
    print("-len(df)-")
    print(len(df))
    print("-df[\"tweet\"].head()-")
    print(df["tweet"].head())
    print("-df[\"tweet\"]tail()-")
    print(df["tweet"].tail())


if __name__ == "__main__":
    main()