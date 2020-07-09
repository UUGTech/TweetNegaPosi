# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import MeCab
import pickle
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import model_from_json
from constant import *
import preprocess
mt = MeCab.Tagger("-Owakati -d ./mecab-ipadic-neologd")
dictionaries = pickle.load(open(VOCAB_DICT_PATH, "rb"))
dictionaries_inv = {c:i for i, c in enumerate(dictionaries)}

#---------------------------------------------------------------
# load model and parameters
#---------------------------------------------------------------
def load_model():
    mode_json_str = open(MODEL_FILE_PATH).read()
    model = model_from_json(mode_json_str)
    model.load_weights(PARAMS_PATH)
    return model

#---------------------------------------------------------------
# predict from a text
#---------------------------------------------------------------
def predict_text(text):
    model = load_model()


    input_text = preprocess.clean([text])[0]
    input_text = preprocess.split_word(mt, input_text)
    input_text = preprocess.padding([input_text])[0]
    input_data = []
    for w in input_text:
        try:
            input_data.append(dictionaries_inv[w])
        except KeyError:
            input_data.append(0)
    input_data = np.array(input_data)
    input_data = input_data.astype(np.float32)
    res = model.predict(np.array([input_data]))

    return res[0][0]


#---------------------------------------------------------------
# main function to test
#---------------------------------------------------------------
def main():
    model = load_model()
    dictionaries = pickle.load(open(VOCAB_DICT_PATH, "rb"))
    dictionaries_inv = {c:i for i, c in enumerate(dictionaries)}

    while True:
        tweet = input("ツイートの内容を入力してください >> ")
        print(predict_text(tweet))






if __name__ == "__main__":
    main()

