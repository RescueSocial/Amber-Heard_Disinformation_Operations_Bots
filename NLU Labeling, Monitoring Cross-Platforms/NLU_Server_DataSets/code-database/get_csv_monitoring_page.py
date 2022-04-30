import mysql.connector
import csv

mydb = mysql.connector.connect(
  host="---",
  database='twitterbot_dev',
  user="user",
  password="user"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM monitor_monitoringpage")

myresult = mycursor.fetchall()

header = ['id', 'type', 'contents', 'client_id']

with open('tweeter_monitoring_page_result.csv', 'w', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    for data in myresult:
        writer.writerow(data)