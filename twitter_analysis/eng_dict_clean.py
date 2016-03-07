# Program to convert a text document which has words with it's positive
# and negative score to a python dictionary. Conversion to python
# dictionary helps in faster access to get the score of the word.
# The score will be used for analyzing the sentiment
# We will use the unigram mode and Naive Bayes in conjunction to give a sentiment
# and classify the tweets.
# **Input file is SentiWord_Test and the o/p is test_dict

import re
from collections import defaultdict
import json

dict_path = "Input file location: SentiWord_Test.txt"
word_dict = defaultdict(dict)
dict_op = open("Output file location: test_dict.txt", 'w')
main_cnt = 0

# Function creates the python dictionary from the file
def create_dict(dict_path):
    with open(dict_path) as orig_dict:
        for line in orig_dict:
            dict_parts = re.split(r'\t+', line)
            same_words = clean_word(dict_parts)
            word_dict.update(assign_score(same_words, dict_parts))
    return word_dict

# Removing the "#" and splitting the keywords to create the dict
def clean_word(words):
    return re.split(r'\s+',re.sub(r'#\S+', "",words[len(words)-2]))

# File has several words with the same meaning in the same line.
# In the python dict each word is a key word. The function below
# creates keys from those words and assigns them the same score
def assign_score(same_meaning, dict_parts):
    global main_cnt
    main_cnt += 1
    try:
        for i in range(0,len(same_meaning)):
            word_dict[same_meaning[i]]['POS'] = dict_parts[0]
            word_dict[same_meaning[i]]['PosScore'] = dict_parts[2]
            word_dict[same_meaning[i]]['NegScore'] = dict_parts[3]
        return word_dict
    except:
        print (main_cnt)

f = create_dict(dict_path)
json.dump(f, dict_op)