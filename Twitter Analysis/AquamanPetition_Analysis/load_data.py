
# https://stackoverflow.com/questions/33862420/ipython-notebook-how-to-reload-all-modules-in-a-specific-python-file

import pandas as pd
import os
import pickle
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import helpers

# Load All Twitter Data (2018-2022)
tweets = pd.read_csv('DATA/merged_all_years_zip.csv', compression='zip', lineterminator='\n')
# tweets.rename(columns={'total_count': 'total_retweets'}, inplace=True);
    
tweets['tweet_id'] = tweets['tweet_id'].astype('str')
tweets['user_id'] = tweets['user_id'].astype('str')
tweets["created_at"] = pd.to_datetime(tweets["created_at"])
tweets["user_created_at"] = pd.to_datetime(tweets["user_created_at"])
tweets["date"] = pd.to_datetime(tweets["date"])
tweets.sort_values(by='created_at', inplace=True)

# All Twitter Data (2018-2022)
# print(tweets.shape) # (1720317, 30)
# tweets.head(2)

# tweets.created_at.dt.date.min(), tweets.created_at.dt.date.max()
# tweets.user_created_at.dt.date.min(), tweets.user_created_at.dt.date.max()


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



# Load All Users Data (Tweeted between 2018-2022)
# > **NOTE:**
# > - All Users Data Exists in The Tweets Data
# > - Those are the users tweeted in the past 5 years (2018-2022)

users = pd.read_csv('DATA/users_data_zip.csv', compression='zip', lineterminator='\n')
users['user_id'] = users['user_id'].astype('str')
users['user_created_at'] = pd.to_datetime(users["user_created_at"], format="%Y-%m-%d %H:%M:%S") 
users.sort_values(by='user_created_at', inplace=True)

# All Users Data (Tweeted Between 2018 and 2022) 
# print(users.shape) # (452088, 13)
# users.head(2)

# users["user_created_at"].dt.date.min(), users["user_created_at"].dt.date.max()

# Filter on users in the aquaman_petition datafram
# u --> users
aquaman_petition_u = users[users['user_id'].isin(list(aquaman_petition.user_id))]




# Create a daily creation dataframe for "Aquaman Petition Links"
# t --> tweets 
# u --> users

### DailyCreation (USERS)
tmb = pd.DataFrame(columns=['date', 'year', 'month', 'dayofmonth', 'hour'])
tmb['date'] = users['user_created_at'].dt.date
tmb['year'] = users['user_created_at'].dt.year
tmb['month'] = users['user_created_at'].dt.strftime("%b")
tmb['dayofmonth'] = users['user_created_at'].dt.day
tmb['hour'] = users['user_created_at'].dt.hour

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

### DailyCreation  (TWEETS)
# # t --> tweets
# df_creations_t = aquaman_petition.groupby(['date', 'year', 'month', 'dayofmonth', 'hour']).size().reset_index(name='n_tweets')
# df_creations_t.sort_values('n_tweets', ascending=False, inplace=True)
# print(df_creations_t.shape)
# df_creations_t.head()


# Sorted by the number of tweets (created in each hour)
df_creations = pd.merge(df_creations_t, df_creations_u,  how='left', 
                        on=['date', 'year', 'month', 'dayofmonth', 'hour'])
# print(df_creations.shape)
# df_creations.head()
# df_creations.date.min(), df_creations.date.max()


df_creations2 = pd.merge(df_creations_t, df_creations_u,  how='outer', 
                        on=['date', 'year', 'month', 'dayofmonth', 'hour'])

# Sort by the number of created accounts (on each hour)
# df_creations2.sort_values('#created_accounts', ascending=False).head(10)




