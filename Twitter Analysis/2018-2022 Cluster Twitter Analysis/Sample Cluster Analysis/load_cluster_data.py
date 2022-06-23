import pandas as pd
import os
import json 
import pickle
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import helpers

## Load Tweets Data
with open('../../Clustering Results/2020 Clustering Twitter Result/data/nov/tweets1.json') as f:
    tweets1 = json.load(f)

df = pd.DataFrame(tweets1)
tweets2 = helpers.clean_data(df)
# print(tweets2.shape)
# tweets2.head(1)


## Load Tweets Metrics Data (Cluster 1 - Nov)
df_metrics = pd.read_csv("../../DATA/tweets_metrics_zip.csv", compression='zip')
df_metrics['id'] = df_metrics['id'].astype('str')
# print(df_metrics.shape)
# df_metrics.head(1)


# Merge Tweets and Metrics
tweets = pd.merge(tweets2, df_metrics, left_on='tweet_id', right_on='id', how='left')
tweets.drop(columns='id', inplace=True)

tweets['tweet_id'] = tweets['tweet_id'].astype('str')
tweets['user_id'] = tweets['user_id'].astype('str')
tweets["created_at"] = pd.to_datetime(tweets["created_at"])
tweets["user_created_at"] = pd.to_datetime(tweets["user_created_at"])
tweets["date"] = pd.to_datetime(tweets["date"])
tweets.sort_values(by='created_at', inplace=True)


# Filter on Aquaman petition Links
aquaman = tweets[tweets.text.str.contains('aquaman|petition')]
tmp = aquaman[aquaman.text.str.contains('sign|fire|remov')]
aquaman_petition = tmp[tmp.text.str.contains('http')]


# aquaman_petition.info()
# helpers.isnull(aquaman_petition)
# aquaman_petition.dropna(subset=['text'], inplace=True)

# for col in ['text', 'year', 'username', 'user_location', 'is_verified']:
#     print('The value counts of ' + col)
#     print(aquaman_petition[col].value_counts().head())
#     print('\n')



## Load Users Data

users1 = pd.read_csv('../../Clustering Results/2020 Clustering Twitter Result/data/nov/1.csv')
users = users1.drop(columns='user.lang')

users['user.id_str'] = users['user.id_str'].astype('str')
users['user.created_at'] = pd.to_datetime(users["user.created_at"], format="%Y-%m-%d %H:%M:%S+00:00") 
users.sort_values(by='user.created_at', inplace=True)





# Create a daily creation dataframe for "Aquaman Petition Links"

### DailyCreation (USERS)
tmb = pd.DataFrame(columns=['date', 'year', 'month', 'dayofmonth', 'hour'])
tmb['date'] = users['user.created_at'].dt.date
tmb['year'] = users['user.created_at'].dt.year
tmb['month'] = users['user.created_at'].dt.strftime("%b")
tmb['dayofmonth'] = users['user.created_at'].dt.day
tmb['hour'] = users['user.created_at'].dt.hour

df_creations_u = tmb.groupby(['date', 'year', 'month', 'dayofmonth', 'hour']).size().reset_index(name='#created_accounts')
df_creations_u.sort_values('#created_accounts', ascending=False, inplace=True)
df_creations_u["date"] = pd.to_datetime(df_creations_u["date"])
# print(df_creations_u.shape)
# df_creations_u.head()


### DailyCreation  (TWEETS)
# # t --> tweets

df_creations_t = aquaman_petition.groupby(['date', 'year', 'month', 'dayofmonth', 'hour']).agg({'text':'count', 'user_id': 'nunique'}).reset_index(
).rename(columns={'text':'n_tweets', 'user_id':'by_#accounts'}).sort_values('n_tweets', ascending=False)
# print(df_creations_t.shape)
# df_creations_t.head()


# Sorted by the number of tweets (created on each hour)
df_creations = pd.merge(df_creations_t, df_creations_u,  how='left', 
                        on=['date', 'year', 'month', 'dayofmonth', 'hour'])
# print(df_creations.shape)
# df_creations.head()
# df_creations.date.min(), df_creations.date.max()


df_creations2 = pd.merge(df_creations_t, df_creations_u,  how='outer', 
                        on=['date', 'year', 'month', 'dayofmonth', 'hour'])

# Sort by the number of created accounts (on each hour)
# df_creations2.sort_values('#created_accounts', ascending=False).head(10)


