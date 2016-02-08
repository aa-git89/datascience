#Program to insert csv file to MySql

#importing the necessary packages
import csv
import mysql.connector

# creating connector for MySql
cnx = mysql.connector.connect(user= 'your username', password = 'your password', database='test')
cursor = cnx.cursor()
tweets_test = open("File with tweets", encoding='utf-8')
csv_data = csv.reader(tweets_test, delimiter=',')
row_count = 0

# Loop to iterate csv and insert data into MySql
for row in csv_data:
	try:
		row_count+=1
		cursor.execute("INSERT INTO superbowl_data"
		"(tweet_id, tweet_text, tweet_time, tweet_author, tweet_author_id, tweet_author_geo, tweet_author_followers,tweet_language, tweeet_geo, tweet_media ,tweet_hastag_tagged)" 
		"VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)
	except (mysql.connector.Error, mysql.connector.Warning) as e:
		print(e,"on row",row_count)

cnx.commit()
cursor.close()
print ("Done")