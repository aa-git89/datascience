# This program is a pre-process step required to clean the tweet
# so that it can be used for classification and sentiment analysis purposes
# In this the tweet is picked up from the file and the same file is replaced with a clean version of the tweet
# uncleaned_tweet.txt and the cleaned_tweet.txt show what will be the input and how will be the final o\p
# the training positive data is train_pos3.txt, training negative data is train_neg3.txt
#

import re
import difflib
import math
import sys
from tempfile import mkstemp
from shutil import move
from os import remove, close
import json
# -*- coding: latin-1 -*-
# -*- coding: utf-8 -*-

sys.path.append("../any path to look for file")
pos_file_path = "input positive tweet training text file"
neg_file_path = "inputs negative tweet training text file"
test_file_path = "input testing data file"
stp_wrd = "file having all the stop words"
train_num = 400.00
# List containing the politician which should be removed from the tweet
key_word = [r'\b[Tt]rump\b',r'\b[Dd]onald\b',r'\b[Cc]linton\b',r'\b[Hh]illary\b',r'\b[Cc]ruz\b',\
            r'\b[Tt]ed\b',r'\b[Rr]ubio\b',r'\b[Mm]arco\b']
key_word_regex = ('|'.join(key_word))
stop_word = []
# list consisting of data elements or characters that need to be removed from the tweet
to_match = ['@\S+', 'http\S+', r'[^\w\s]']
#to_match = ['@\S+','http\S+','\,','\"','\.','(',')',';','[',']','{','}']
word_dict = json.load(open("C:/Python27/outgoing/final_dict_cpy.txt"))
#corpus_word_set = set()
word_list = word_dict.keys()

# dictionary of positive and negative emoticons. This will be removed from the tweet
emoticons_dict = {':-)': 'positive',	':)': 'positive',	':D': 'positive',	':o)': 'positive',	\
                  ':]': 'positive',	':3': 'positive',	':c)': 'positive',	':>': 'positive',	\
                  '=]': 'positive',	'8)': 'positive',	'=)': 'positive',	':}': 'positive',	\
                  ':^)': 'positive',	':?)': 'positive', ':-D': 'positive',	'8-D': 'positive',	'8D': 'positive',	\
                  'x-D': 'positive',	'xD': 'positive',	'X-D': 'positive',	'XD': 'positive',	'=-D': 'positive',	\
                  '=D': 'positive',	'=-3': 'positive',	'=3': 'positive',	'B^D': 'positive',	\
                  ':-))': 'positive', ":'-)": 'positive',	":')": 'positive',	';-)': 'positive',	\
                  ';)': 'positive',	'*-)': 'positive',	'*)': 'positive',	';-]': 'positive',	\
                  ';]': 'positive',	';D': 'positive',	';^)': 'positive',	':-,': 'positive',	\
                  'o/\o': 'positive',	'^5': 'positive',	'>_>^': 'positive',	'^<_<': 'positive', \
                  '\o/': 'positive', ">:[": 'negative',	":-(": 'negative',	":(": 'negative',	\
                  ":-c": 'negative',	":c": 'negative',	":-<": 'negative',	":?C": 'negative',	\
                  ":<": 'negative',	":-[": 'negative',	":[": 'negative',	":{": 'negative',    \
                  ";(": 'negative', ":-||": 'negative',	":@": 'negative',	">:(": 'negative',	\
                  ":'-(": 'negative',	":'(": 'negative', "D:<": 'negative',	"D:": 'negative',	\
                  "D8": 'negative',	"D;": 'negative',	"D=": 'negative',	"DX": 'negative',	\
                  "v.v": 'negative',	"D-':": 'negative',	':L': 'negative', "=L": 'negative',	":S": 'negative',	">.<": 'negative'
                }

# will be used to remove handler, url and apostrophe
url_handlers_oth = ('|'.join(to_match))
# Since each smiley has characters that regex may not recognize, re.escape is called on each element
positive_smileys = [re.escape(i) for i, val in emoticons_dict.iteritems() if val == 'positive']
# An OR condition helps to create a regex which helps in matching any of the emoticons
positive_smileys_regex = ('|'.join(positive_smileys))
negative_smileys = [re.escape(i) for i, val in emoticons_dict.iteritems() if val == 'negative']
negative_smileys_regex = ('|'.join(negative_smileys))

# pattern=re.compile("[^\w']") # did not incorporate this. Taken care in url match list.
# This has an extra "'" need to check what difference it will make

with open(stp_wrd) as sw_file:
    for line in sw_file:
        # removed " ' " from the stop words as our clean process is removing it
        # between characters e.g. didn't = didnt
        stop_word.append(line.strip())

# replacing multiple charcters by 3 characters
# e.g. coooool = coool, not made it as cool to give it an extra emphasis
# and higher points
def replace_multiple_chars(s):
    s = re.sub(r'(.)\1{2,}', r'\1\1\1',s, flags=re.IGNORECASE)
    return s

# removing handlers, url and english apostrophe
def handler_url(s):
    s = re.sub(url_handlers_oth, "", s.lower())
    return s


# classifying tweets based on the smiley present
def classify_input_tweets(s):
    # Searches for any positive smiley in the string
    is_positive = any(x in s for x in positive_smileys)
    # Searches for any negative smiley in the string
    is_negative = any(x in s for x in negative_smileys)
    if is_positive:
        if not is_negative:
            return 'positive'
        else:
            return 'null'
    elif is_negative:
        return 'negative'
    else:
        return 'null'

# Function to remove simleys after classifying
def remove_smileys(s):
    s = re.sub(positive_smileys_regex, "", s)
    s = re.sub(negative_smileys_regex, "", s)
    return s

# The function below replaces the words in the string with the closes matches from the dictionary
def find_close_matches(clean_tweet, word_list) :
    final_tweet = ""
    for word in clean_tweet.split():
        # Begin of Changes 3/13
        if word in word_list:
            final_tweet = final_tweet + word + " "
        elif word[len(word.strip())-2:] == 'nt':
            final_tweet = final_tweet + word + " "
        elif word[:-1] in word_list:
            final_tweet = final_tweet + word[:-1] + " "
        elif word[:-2] in word_list:
            final_tweet = final_tweet + word[:-2] + " "
        elif word[:-3] in word_list:
            final_tweet = final_tweet + word[:-3] + " "
        else:
            final_tweet = final_tweet + word + " "
        #final_tweet = final_tweet + difflib.get_close_matches(word, word_list)[0] + " "
        # End of Changes 3/13
    final_tweet = final_tweet.strip()
    return final_tweet

# This function cleans the original tweet to remove components
# like handlers, urls and apostrophe's and others
def replace(file_path):
    # Create temp file
    #global corpus_word_set
    corpus_word_set = set()
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                #rep = line.split(',', 1)
                #clean_tweet = handler_url(replace_multiple_chars(rep[1]))
                clean_tweet = handler_url(replace_multiple_chars(line))
                clean_tweet = re.sub(r'#([^\s]+)', r'\1', clean_tweet)
                clean_tweet = re.sub(key_word_regex, '', clean_tweet, flags=re.IGNORECASE)
                clean_tweet = remove_smileys(clean_tweet)
                # consider removing words less than 4 characters
                clean_tweet = re.sub(r'\b\w{1,3}\b', '', clean_tweet)
                clean_tweet = find_close_matches(clean_tweet, word_list) # removed as it's messing up data
                # removing less than 4 chars again as words might have got converted
                # because of the above statement
                clean_tweet = re.sub(r'\b\w{1,3}\b', '', clean_tweet)
                clean_tweet = re.sub(' +', ' ', clean_tweet)
                clean_tweet, corpus_word_set = remove_stop_words(clean_tweet, corpus_word_set)
                #new_file.write(rep[0] + "," + clean_tweet + "\n")
                new_file.write(clean_tweet + "\n")
    close(fh)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)
    return corpus_word_set

# removes the list of stop words from the tweet
def remove_stop_words(txt, corpus_word_set):
    tweet_word_set = set([word for word in txt.split() if word not in stop_word])
    txt = ' '.join(tweet_word_set)
    corpus_word_set.update(tweet_word_set)
    return txt, corpus_word_set

# Create new dict with probabilities
def senti_word_probability(senti_file_path, corpus,sent_ty, opo_sent_ty):
    # do we want to add words to dict with prob > 5% only???
    with open(senti_file_path,'r') as tweet_file:
        txt = tweet_file.readlines()
        for word in corpus:
            occur_cnt = 0
            for line in txt:
                if re.findall('\\b'+word+'\\b', line):
                    occur_cnt = occur_cnt + 1
                else:
                    pass
            try:
                word_dict[word][sent_ty+'Prob'] = round(occur_cnt/train_num, 3)
            except KeyError:
                word_dict[word] = {}
                word_dict[word][sent_ty+'Prob'] = round(occur_cnt/train_num, 3)
                word_dict[word]['PosScore'] = 0.5
                word_dict[word]['NegScore'] = 0.5
            try:
                word_dict[word][opo_sent_ty+'Prob']
            except KeyError:
                word_dict[word][opo_sent_ty+'Prob'] = 0
        #return word_dict

# The below code is used to classify tweets
def classify_tweets(test_file_path, final_dict):
    with open(test_file_path,'r') as senti_analysis:
        for tweet in senti_analysis:
            positive_score = 1.0
            negative_score = 1.0
            for word in tweet.split():
                value = final_dict.get(word)
                if value != None:
                    try:
                        final_dict[word]['PosProb']
                        if final_dict[word]['PosProb'] == 0.0:
                            positive_score = positive_score*.0001*math.exp(float(final_dict[word]['PosScore']))
                        else:
                            positive_score = positive_score*(float(final_dict[word]['PosProb']))*math.exp(float(final_dict[word]['PosScore']))
                    except KeyError:
                        pass
                    try:
                        final_dict[word]['NegProb']
                        if final_dict[word]['NegProb'] == 0.0:
                            negative_score = negative_score*(0.0001)*math.exp(float(final_dict[word]['NegScore']))
                        else:
                            negative_score = negative_score*(float(final_dict[word]['NegProb']))*math.exp(float(final_dict[word]['NegScore']))
                    except KeyError:
                        pass
            if positive_score > negative_score:
                prediction = 'positive'
            elif positive_score < negative_score:
                prediction = 'negative'
            else:
                prediction = 'neutral'
            print tweet.strip(), prediction

pos_corpus_set = replace(pos_file_path)
neg_corpus_set = replace(neg_file_path)
senti_word_probability(pos_file_path, pos_corpus_set, "Pos", "Neg")
senti_word_probability(neg_file_path, neg_corpus_set, "Neg", "Pos")
test_corpus = replace(test_file_path)
classify_tweets(test_file_path, word_dict)