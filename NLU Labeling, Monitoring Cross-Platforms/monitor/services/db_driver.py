import mysql.connector
import time
from datetime import datetime 
import random
import csv

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

# sql = "INSERT INTO actions_action (actionbot_id, commander_id, performed, method, target_user, target_content,\
#         contents, url, created_at, performed_at) VALUES (%s, %s, %s, %s, %s,%s,%s,%s, NOW(),%s)"
# val = (4, 4, 0, "tweet", 0,0,"test","https://twitter.com",  "2019-10-20")
# mycursor.execute(sql, val)


def get_actions(bot_id):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM actions_action WHERE performed=0 AND bot_id=" + str(bot_id)
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  return myresult

def get_urls(client_id):
  return_urls = []
  try:
    
    mycursor = mydb.cursor()
    sql = "SELECT name FROM monitor_client WHERE id=" + str(client_id)
    mycursor.execute(sql)
    name = mycursor.fetchone()
    return_urls.append("https://twitter.com/{}/with_replies".format(name[0]))
    
    sql = "SELECT * FROM monitor_monitoringpage WHERE client_id=" + str(client_id)
    mycursor.execute(sql)
    pages = mycursor.fetchall()
    for page in pages:
      if page[1] == "Hashtage":
        return_urls.append( "https://twitter.com/hashtag/{}?src=hashtag_click&f=live".format(page[2]))
      elif page[1] == "Query":
        return_urls.append( "https://twitter.com/search?q={}&src=typed_query&f=live".format(page[2]))
      else:
        return_urls.append(page[2])
  except:
    pass
  return return_urls
def get_client_name(client_id):
  try:
    mycursor = mydb.cursor()
    sql = "SELECT name FROM monitor_client WHERE id=" + str(client_id)
    mycursor.execute(sql)
    name = mycursor.fetchone()
    return name[0]
  except Exception as e:
    print(e)
    return "client_{}".format(random.randint(1,10000))

def performed_action(action_id, response=""):
  try:
    mycursor = mydb.cursor()
    sql = "UPDATE actions_action SET performed=1, performed_at='{}', site_response='{}' WHERE id={}".format(str(datetime.utcnow()),response,str(action_id))
    mycursor.execute(sql)
    mydb.commit()
    return True
  except Exception as e:
    print(e)
    return False
def download_all_tweets(client_id):
  try:
    mycursor = mydb.cursor()
    sql = "SELECT id, what FROM monitor_tweet WHERE client_id=" + str(client_id)
    mycursor.execute(sql)
    rows= mycursor.fetchall()
    with open('all_tweet_data.csv', 'w', encoding="cp1251", errors='ignore') as f:
      writer = csv.writer(f, delimiter=',')
      writer.writerow(["id", "comment_text", "defense_AH", "support_AH", "offense_AH", "defense_against_AH"])
      for row in rows:
        text = str(row[1])
        if not text.startswith('#'):
          writer.writerow([str(row[0]),str(row[1]), 0, 0, 0, 0, 0])
      return "success download all_tweet_data.csv from tweets"

  except Exception as e:
    print(e)
    return "error"

def delete_all_invalid_nlu_text():
  try:
    mycursor = mydb.cursor()
    sql = "SELECT id, what FROM monitor_tweet WHERE client_id=" + str(client_id)
    mycursor.execute(sql)
    rows= mycursor.fetchall()
    with open('all_tweet_data.csv', 'w', encoding="cp1251", errors='ignore') as f:
          writer = csv.writer(f, delimiter=',')
          writer.writerow(["id", "comment_text", "defense_AH", "support_AH", "offense_AH", "defense_against_AH"])
          for row in rows:
              writer.writerow([str(row[0]),str(row[1]), 0, 0, 0, 0, 0])
          return "success download all_tweet_data.csv from tweets"

  except Exception as e:
    print(e)
    return "error"
print(download_all_tweets(1))
# set_action([1, 1,1,1,T,N])
# set_action((1, 1, 1, 0, 'T', None, None, "Amber Heard is a hero to domestic violence victims. She's strong, beautiful and smart.", 'https://twitter.com/home', datetime.datetime(2021, 2, 25, 4, 53, 52, 316469), None, 'T'))