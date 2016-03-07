# This program is a pre-process step required to clean the tweet
# so that it can be used for classification and sentiment analysis purposes
# In this the tweet is picked up from the file and the same file is replaced with a clean version of the tweet
# uncleaned_tweet.txt and the cleaned_tweet.txt show what will be the input and how will be the final o\p
import re
import sys
from tempfile import mkstemp
from shutil import move
from os import remove, close
# -*- coding: latin-1 -*-
# -*- coding: utf-8 -*-

sys.path.append("../incoming/")
# think of removing Trump from text like #TrumpLies
# Cruz Rubio and Hillary should be removed too
key_word = r'\btrump\b'
stop_word = []
# list consisting of data elements or characters that need to be removed from the tweet
to_match = ['@\S+', 'http\S+', '\,', '\"', '\.', '(', ')', ';', '[', ']', '{', '}']

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

file_path = "Path of the tweets to test: uncleaned_tweet.txt"
# please make a note that this code will replace the same file. In git
# I have both the clean and uncleaned version, name given in the first few lines
stp_wrd = "list of stop words you want to remove: stop_words.txt"

# will be used to remove handler, url and apostrophe
url_handlers_oth = ('|'.join(to_match))
# Since each smiley has characters that regex may not recognize, re.escape is called on each element
positive_smileys = [re.escape(i) for i, val in emoticons_dict.iteritems() if val == 'positive']
# An OR condition helps to create a regex which helps in matching any of the emoticons
positive_smileys_regex = ('|'.join(positive_smileys))
negative_smileys = [re.escape(i) for i, val in emoticons_dict.iteritems() if val == 'negative']
negative_smileys_regex = ('|'.join(negative_smileys))

with open(stp_wrd) as sw_file:
    for line in sw_file:
        stop_word.append(line.strip())

# replacing multiple charcters by 3 characters
# e.g. coooool = coool, not made it as cool to give it an extra emphasis
# and higher points
def replace_multiple_chars(s):
    s = re.sub(r'(.)\1{2,}', r'\1\1\1',s, flags=re.IGNORECASE)
    return s

# removing handlers, url and english apostrophe
def handler_url(s):
    s = re.sub(url_handlers_oth, "", s)
    return s

def remove_stop_words(txt):
    txt = ' '.join([word for word in txt.split() if word not in stop_word])
    return txt

# classifying tweets based on the smiley present
def classify_input_tweets(s):
    # Searches for any positive smiley in the string
    is_positive = any(x in s for x in positive_smileys)
    # Searches for any negative smiley in the string
    is_negative = any(x in s for x in negative_smileys)
    if is_positive:
        if not is_negative:
            return 'positive'
        else :
            return 'null'
    elif is_negative:
        return 'negative'
    else :
        return 'null'

# Function to remove simleys after classifying
def remove_smileys(s):
    s = re.sub(positive_smileys_regex, "", s)
    s = re.sub(negative_smileys_regex, "", s)
    return s

# This function cleans the oiginal tweet to remove components
# like handlers, urls and apostrophe's and others
def replace(file_path):
    # Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                rep = line.split(',', 1)
                clean_tweet = handler_url(replace_multiple_chars(rep[1]))
                clean_tweet = re.sub(r'#([^\s]+)', r'\1', clean_tweet)
                clean_tweet = re.sub(key_word, '', clean_tweet, flags=re.IGNORECASE)
                clean_tweet = remove_stop_words(clean_tweet)
                clean_tweet = remove_smileys(clean_tweet)
                # consider removing words less than 4 characters
                clean_tweet = re.sub(' +', ' ', clean_tweet)
                new_file.write(rep[0] + "," + clean_tweet + "\n")

    close(fh)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)

replace(file_path)