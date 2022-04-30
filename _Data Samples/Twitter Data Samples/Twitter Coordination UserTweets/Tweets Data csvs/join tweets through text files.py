import pickle
import pandas as pd

import glob
# All files ending with .txt
screenname = glob.glob("D:/json_text/tweets/*.txt") ## your file location

filtered_tweet = []
list_ = []
count =0
for i in screenname:
  with open(i , "rb") as fp:   # Unpickling
    fetched_tweets = pickle.load(fp)
    for tweet in fetched_tweets:
      filtered_tweet.append(tweet)
      list_.append(tweet.text)
    count = count + 1
    print(count)


hashtags = []
tweets = []

tweet_id = []
user_mentions = []
URLs = []
Retweets = []
likes = []
date = []
location = []
username = []
fc = []
ffc = []
rt = []
ft = []
data = pd.DataFrame(columns = ['tweet_id','text','username','Retweets','hashtags','user_mentions','urls','likes','date','location','friends_count','followers_count','retweet_count'])
for tweet in filtered_tweet:
  tweets.append(tweet.text)
  tweet_id.append(tweet.id)
  username.append(tweet.user.screen_name)
  Retweets.append(tweet.retweet_count)
  user_mentions.append(tweet.entities['user_mentions'])
  hashtags.append(tweet.entities['hashtags'])
  URLs.append(tweet.entities['urls'])
  likes.append(tweet.favorite_count)
  location.append(tweet.user.location)
  date.append(tweet.created_at)
  fc.append(tweet.user.friends_count)
  ffc.append(tweet.user.followers_count)
  rt.append(tweet.retweet_count)


data['tweet_id'] = tweet_id
data['text'] = tweets
data['username'] = username
data['Retweets'] = Retweets
data['hashtags'] = hashtags
data['user_mentions'] = user_mentions
data['urls'] = URLs
data['likes'] = likes
data['date'] = date
data['location'] = location
data['friends_count'] = fc
data['followers_count'] = ffc
data['retweet_count'] = rt

print('here')
data.to_csv('275 tweets_new_2021.csv')
