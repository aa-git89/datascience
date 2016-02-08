#Program to convert json tweets into csv

#importing the necessary packages
import json
import sys
import codecs
from csv import writer

tweets_file = open("JSON i/p file name", "r")
# encoding is an imp step else windows will throw encoding error
# which seems like python error but is actually a windows error
# used newline for writing to remove extra spaces csv adds for windows
tweets_op = open("CSV o/p file name",'a', encoding='utf-8', newline='')
csv = writer(tweets_op)
tweet_count = 0
data_load_cnt = 0
tweets = []

# Function to tag all #tags in a tweet together
def hash_tagging(tweets):
	tw_hast_pre = []
	tw_hast_together = []
	for x in range(len(tweets['entities']['hashtags'])):
		tw_hast_pre.append(tweet['entities']['hashtags'][x]['text'])
	tw_hast_together.append(tw_hast_pre)
	tw_hast_pre = []
	return tw_hast_together

# Function to get the url used in the tweet
def media_url(tweet):
	if 'media' in tweet['entities']:
		return tweet['entities']['media'][0]['media_url_https']
	else:
		pass
# Loop to iterate through the file and create csv of appropriate fields	
for line in tweets_file:
	tweet_count+=1
	try:
		tweet = (json.loads(line))
	except:
		pass
	row = (
		tweet['id'],
		tweet['text'],
		tweet['created_at'],
		tweet['user']['screen_name'],
		tweet['user']['id_str'],
		tweet['user']['location'],
		tweet['user']['followers_count'],
		tweet['lang'],
		tweet['geo'],
		media_url(tweet),
		hash_tagging(tweet)
		)
	try:
		data_load_cnt +=1
		values = [(value if hasattr(value, 'encode') else value) for value in row]
	except:
		pass
	csv.writerow(values)
print ("# Tweets Received:", tweet_count)
print ("# Tweets Exported:", data_load_cnt)
tweets_op.close()