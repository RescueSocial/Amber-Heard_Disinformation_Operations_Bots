import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="---",
  database='twitterbot_dev',
  user="user",
  password="user"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM monitor_tweeter")

myresult = mycursor.fetchall()

header = ['id', 'user', 'support_count', 'offense_count', 'support_score', 'category', 'client_id', 'timestamp', 'analysis_total_tweets', 'unbiased_count']

with open('tweeter_analysis_result.csv', 'w', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for data in myresult:
        writer.writerow(data)