import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="---",
  database='twitterbot_dev',
  user="user",
  password="user"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM nlpengine_nlutext")

myresult = mycursor.fetchall()

header = ['id', 'text', 'trained', 'created_at', 'trained_at', 'defense_AH', 'defense_against_AH', 'offense_AH', 'support_AH']

with open('nlu_text_result.csv', 'w', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for data in myresult:
        writer.writerow(data)