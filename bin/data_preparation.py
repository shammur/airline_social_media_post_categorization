#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sun June  2 10:33:22 2019

@author: Shammur A Chowdhury

For English News Short Text
"""

import os
import re
import nltk
import numpy as np
import pandas as pd
from nltk import tokenize

import spacy
import string
from emoji import UNICODE_EMOJI
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import *
from nltk.stem import PorterStemmer

from nltk.corpus import stopwords

porter = PorterStemmer()
import wordsegment as ws
# ws.load()


################## Global Variable ##########################
english_stopwords = set(stopwords.words('english'))


#####################################################################

################## Data IO #######################################

def read_data_for_classification(filename, header=True,delim="\t"):
    # ws.load()
    ids = []
    data=[]
    with open(filename, 'rU') as f:
        if header:
            next(f)
        for line in f:
            row =line.split(delim)
            # row should have 2 entries -- ID \t Text_Content
            row_id = row[0]
            text = row[1]
            text = clean_content(text)
            if isinstance(text, str):
                data.append(text)
                ids.append(row_id)
    return data, ids


def read_data_for_evaluation(filename, header=True,delim="\t"):
    # ws.load()
    ids = []
    data=[]
    labels = []
    with open(filename, 'rU') as f:
        if header:
            next(f)
        for line in f:
            row =line.split(delim)
            # row should have 3 entries -- ID \t Text_Content \t Ref_Class_Label
            row_id = row[0]
            text = row[1]
            lab = row[2].lstrip().rstrip()
            text = clean_content(text)
            if isinstance(text, str):
                data.append(text)
                ids.append(row_id)
                labels.append(lab)
    return data, ids, labels


#####################################################################


################## Data Processing for English Text ############################

def clean_content(line):
    if (isinstance(line, float)):
        return None
    line.replace('\n', ' ')
    line = remove_emails(line)
    line = remove_urls(line)

    # Check if # or @ is there with word
    linelst = []

    for w in line.split():
        if ("#" in w or "@" in w):
            # print(w)
            linelst.append(' '.join(ws.segment(w)))
        elif 'http' not in w:
            linelst.append(w)
    line = ' '.join(linelst)

    # add spaces between punc,
    line = line.translate(str.maketrans({key: " {0} ".format(key) for key in string.punctuation}))

    # then remove punc,

    translator = str.maketrans('', '', string.punctuation)
    line = line.translate(translator)

    ## convert to lower case
    line = line.lower()

    # stemming:
    token_words = word_tokenize(line)
    # token_words porter.stem(word)
    stem_sentence = [word if not hasDigits(word) else '<NUM>' for word in token_words]

    stem_sentence = removeConsecutiveSameNum(stem_sentence)

    line = " ".join(stem_sentence)

    removed_stops = [w for w in line.split() if not w in english_stopwords and len(w) != 1]
    line = ' '.join(removed_stops)

    return line

def remove_urls (text):
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
    return text

def remove_emails(text):
    text = re.sub(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", "",  text, flags=re.MULTILINE)
    return text

def is_emoji(s):
    return s in UNICODE_EMOJI

# add space near your emoji
def add_space_with_emojis(text):
    return ''.join(' ' + char if is_emoji(char) else char for char in text).strip()


def removeConsecutiveSameNum(v):
    st = []
    lines=[]

    # Start traversing the sequence
    for i in range(len(v)):

        # Push the current string if the stack
        # is empty
        if (len(st) == 0):
            st.append(v[i])
            lines.append(v[i])
        else:
            Str = st[-1]

            # compare the current string with stack top
            # if equal, pop the top
            if (Str == v[i] and Str == '<NUM>'):
                st.pop()

                # Otherwise push the current string
            else:
                lines.append(v[i])
                st.pop()
                # st.append(v[i])

                # Return stack size
    return lines

def hasDigits(s):
    return any( 48 <= ord(char) <= 57 for char in s)

#####################################################################