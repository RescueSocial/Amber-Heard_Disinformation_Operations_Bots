import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="---",
  database='twitterbot_dev',
  user="user",
  password="user"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM monitor_tweet")

myresult = mycursor.fetchall()

header = ['id', 'user', 'method', 'contents', 'to_user', 'create_at', 'url', 'replies', 'retweets', 'likes', 'timestamp', 'bot_id', 'client_id', 'action', 'estimation label']

with open('tweet_nlu_result.csv', 'w', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for data in myresult:
        writer.writerow(data)