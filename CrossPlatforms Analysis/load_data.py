
# https://stackoverflow.com/questions/33862420/ipython-notebook-how-to-reload-all-modules-in-a-specific-python-file

import pandas as pd
import os
import pickle
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import helpers

# To Apply helpers updates without resarting the kernel
import importlib
importlib.reload(helpers)


# from zipfile import ZipFile 
# from io import StringIO

# zfile = ZipFile('../../Twitter Clustering/Data_Kaggle.zip', 'r')
# filename = '../../Twitter Clustering/Data_Kaggle/2017-2022 Twitter all_quotes retweets Amber Heard Timeline_Data.csv'
# with zfile.open(filename) as f:
#     twitter_all_quotes = pd.read_csv(StringIO(f.read().decode()), lineterminator='\n')

# -------------------------------------------------------------------------------------------------------------------------------

# Load All Twitter Data (2018-2022)
tweets = pd.read_csv('../../Twitter Clustering/DATA/merged_all_years_zip.csv', compression='zip', lineterminator='\n')
# tweets.rename(columns={'total_count': 'total_retweets'}, inplace=True);
    
tweets['tweet_id'] = tweets['tweet_id'].astype('str')
tweets['user_id'] = tweets['user_id'].astype('str')
tweets["created_at"] = pd.to_datetime(tweets["created_at"])
tweets["user_created_at"] = pd.to_datetime(tweets["user_created_at"])
tweets["date"] = pd.to_datetime(tweets["date"])
tweets.sort_values(by='created_at', inplace=True)

tweets["tweets_interactions"] = tweets.loc[
    :,
    [
        "total_retweets",
        "reply_count",
        "like_count",
    ],
].sum(axis=1)

# Load All Users Data (Tweeted between 2018-2022)
# > **NOTE:**
# > - All Users Data Exists in The Tweets Data
# > - Those are the users tweeted in the past 5 years (2018-2022)

users = pd.read_csv('../../Twitter Clustering/DATA/users_data_zip.csv', compression='zip', lineterminator='\n')
users['user_id'] = users['user_id'].astype('str')
users['user_created_at'] = pd.to_datetime(users["user_created_at"], format="%Y-%m-%d %H:%M:%S") 
users.sort_values(by='user_created_at', inplace=True)

# All Users Data (Tweeted Between 2018 and 2022) 
# print(users.shape) # (452088, 13)
# users.head(2)

# users["user_created_at"].dt.date.min(), users["user_created_at"].dt.date.max()

# Create a daily creation dataframe 
# t --> tweets 
# u --> users

### DailyCreation (USERS)
tmp = pd.DataFrame(columns=['date', 'year', 'month', 'dayofmonth', 'hour'])
tmp['date'] = users['user_created_at'].dt.date
tmp['year'] = users['user_created_at'].dt.year
tmp['month'] = users['user_created_at'].dt.strftime("%b")
tmp['dayofmonth'] = users['user_created_at'].dt.day
tmp['hour'] = users['user_created_at'].dt.hour

df_creations_u = tmp.groupby(['date', 'year', 'month', 'dayofmonth', 'hour']).size().reset_index(name='#created_accounts')
df_creations_u.sort_values('#created_accounts', ascending=False, inplace=True)
df_creations_u["date"] = pd.to_datetime(df_creations_u["date"])
# print(df_creations_u.shape)
# df_creations_u.head()

### DailyCreation  (TWEETS)
# # t --> tweets
df_creations_t = (tweets.groupby(['date', 'year', 'month', 'dayofmonth', 'hour'])
                  .agg({'text':'count', 'user_id': 'nunique', 'tweets_interactions':'sum'}).reset_index()
                  .rename(columns={'text':'n_tweets', 'user_id':'by_#accounts'})
                  .sort_values('n_tweets', ascending=False)
                 )
# print(df_creations_t.shape)
# df_creations_t.head()

### DailyCreation  (TWEETS)
# # t --> tweets
# df_creations_t = aquaman_petition.groupby(['date', 'year', 'month', 'dayofmonth', 'hour']).size().reset_index(name='n_tweets')
# df_creations_t.sort_values('n_tweets', ascending=False, inplace=True)
# print(df_creations_t.shape)
# df_creations_t.head()


# Sorted by the number of tweets (created in each hour)
df_creations_twitter = pd.merge(df_creations_t, df_creations_u,  how='left', 
                        on=['date', 'year', 'month', 'dayofmonth', 'hour'])
# print(df_creations.shape)
# df_creations.head()
# df_creations.date.min(), df_creations.date.max()

df_creations2_twitter = pd.merge(df_creations_t, df_creations_u,  how='outer', 
                        on=['date', 'year', 'month', 'dayofmonth', 'hour'])

# Sort by the number of created accounts (on each hour)
# df_creations2.sort_values('#created_accounts', ascending=False).head(10)

# -------------------------------------------------------------------------------------------------------------------------------

# # LOAD YouTube Comments DATA
# youtube_comments = pd.read_csv("../../YouTube_Bot_Analysis/Filtered Data/comments_cleaned/comments_cleaned_zipped.csv", compression='zip', low_memory=False, lineterminator='\n')

# # Filter on 2018-2022
# youtube_comments["p_dtime"] = pd.to_datetime(youtube_comments["p_dtime"])
# youtube_comments = youtube_comments[youtube_comments["p_dtime"].dt.year.isin([2018, 2019, 2020, 2021, 2022])]

# youtube_comments["date"] = pd.to_datetime(youtube_comments["date"])
# youtube_comments["u_dtime"] = pd.to_datetime(youtube_comments["u_dtime"])
# youtube_comments = youtube_comments.sort_values('p_dtime')

# youtube_comments.text.fillna('isnan', inplace=True)

# df_creations_youtube = pd.read_csv('../../YouTube_Bot_Analysis/Filtered Data/comments_cleaned/daily_creations.csv')
# df_creations_youtube.rename(columns={'ncomments': 'youtube_comments'}, inplace=True)
# # Filter on 2018-2022
# df_creations_youtube.date = pd.to_datetime(df_creations_youtube.date)
# df_creations_youtube = df_creations_youtube[df_creations_youtube["date"].dt.year.isin([2018, 2019, 2020, 2021, 2022])]

# -------------------------------------------------------------------------------------------------------------------------------

# LOAD YouTube Comments DATA
youtube_comments = pd.read_csv("../../YouTube_Bot_Analysis/new_data/comments/all_youtube_comments.csv", low_memory=False, lineterminator='\n')

# Filter on 2018-2022
youtube_comments["p_dtime"] = pd.to_datetime(youtube_comments["p_dtime"])
youtube_comments = youtube_comments[youtube_comments["p_dtime"].dt.year.isin([2018, 2019, 2020, 2021, 2022])]

# Creating a DailyCreation DataFrame

# Create a data frame with the number of comments in each date
df_creations_youtube = (
    youtube_comments.groupby(['date', 'year', 'month', 'dayofmonth', 'hour'])
    .agg({'text':'count', 'nreplies': 'sum', 'nlikes': 'sum'}).reset_index()
    .rename(columns={'text':'youtube_comments'}).sort_values('youtube_comments', ascending=False)
)
             
df_creations_youtube["date"] = pd.to_datetime(df_creations_youtube["date"])
df_creations_youtube.ncomments = df_creations_youtube.youtube_comments.astype('int')
df_creations_youtube.nreplies = df_creations_youtube.nreplies.astype('int')
df_creations_youtube.nlikes = df_creations_youtube.nlikes.astype('int')   

# -------------------------------------------------------------------------------------------------------------------------------

# LOAD Instagram Comments DATA
instagram_comments = pd.read_csv("../../Instagram_Bot_Analysis/Data/comments_text.csv", low_memory=False, lineterminator='\n')

# Filter on 2018-2022
instagram_comments["datetime"] = pd.to_datetime(instagram_comments["datetime"])
instagram_comments["date"] = pd.to_datetime(instagram_comments["date"])
instagram_comments = instagram_comments[instagram_comments["datetime"].dt.year.isin([2018, 2019, 2020, 2021, 2022])]

instagram_comments = instagram_comments.sort_values('datetime')


instagram_comments["instagram_comments_interactions"] = instagram_comments.loc[
    :,
    [
        "n_replies",
        "n_likes",
    ],
].sum(axis=1)


### DailyCreation  (TWEETS)
# # t --> tweets
df_creations_instagram = (instagram_comments.groupby(['date', 'year', 'month', 'dayofmonth', 'hour'])
                          .agg({'message':'count', 'user_id': 'nunique', 'instagram_comments_interactions':'sum'}).reset_index()
                          .rename(columns={'message':'instagram_comments', 'user_id':'by_#accounts'})      
                          .sort_values('instagram_comments', ascending=False)
                         )

df_creations_instagram.date = pd.to_datetime(df_creations_instagram.date)

# -------------------------------------------------------------------------------------------------------------------------------

# LOAD Reddit Contributions DATA
reddit_18 = pd.read_csv("../../Reddit_Bot_Analysis/Reddit-Full work/cleaned_data/reddit_merged_2018.csv")
reddit_19 = pd.read_csv("../../Reddit_Bot_Analysis/Reddit-Full work/cleaned_data/reddit_merged_2019.csv")
reddit_20 = pd.read_csv("../../Reddit_Bot_Analysis/Reddit-Full work/cleaned_data/reddit_merged_2020.csv")
reddit_21 = pd.read_csv("../../Reddit_Bot_Analysis/Reddit-Full work/cleaned_data/reddit_merged_2021.csv")

reddit_contributions = pd.concat([reddit_18, reddit_19, reddit_20, reddit_21])
reddit_contributions.created_at = pd.to_datetime(reddit_contributions.created_at)
reddit_contributions.user_created_at = pd.to_datetime(reddit_contributions.user_created_at)

reddit_contributions = reddit_contributions.sort_values('created_at')

reddit_contributions['year'] = reddit_contributions['created_at'].dt.year
reddit_contributions['date'] = reddit_contributions['created_at'].dt.date
reddit_contributions['month'] = reddit_contributions['created_at'].dt.strftime('%b')
reddit_contributions['dayofmonth'] = reddit_contributions['created_at'].dt.day
reddit_contributions['hour'] = reddit_contributions['created_at'].dt.hour

### DailyCreation 
df_creations_reddit = (
    reddit_contributions.groupby(['date', 'year', 'month', 'dayofmonth', 'hour'])
    .agg({'text':'count', 'user_name': 'nunique', 'score':'sum'}).reset_index()
    .rename(columns={'text':'reddit_contributions', 'user_name':'by_#accounts', 'score':'reddit_contributions_score'})
    .sort_values('reddit_contributions', ascending=False)
)

df_creations_reddit.date = pd.to_datetime(df_creations_reddit.date)

# -------------------------------------------------------------------------------------------------------------------------------

# # Compare Interactions
# # LOAD YouTube Video DATA
# youtube_videos = pd.read_csv("../../YouTube_Bot_Analysis/SNA-AH-Case-YouTube/clean_data/video_data_cleaned.csv")

# # Filter on 2018-2022
# youtube_videos["p_dtime"] = pd.to_datetime(youtube_videos["p_dtime"], format="%Y-%m-%d %H:%M:%S+00:00")
# youtube_videos = youtube_videos[youtube_videos["p_dtime"].dt.year.isin([2018, 2019, 2020, 2021, 2022])]

# youtube_videos = youtube_videos.sort_values('p_dtime')

# youtube_videos['date'] = youtube_videos['p_dtime'].dt.date
# youtube_videos['month'] = youtube_videos['p_dtime'].dt.strftime('%b')
# youtube_videos['dayofmonth'] = youtube_videos['p_dtime'].dt.day
# youtube_videos['hour'] = youtube_videos['p_dtime'].dt.hour

# youtube_videos["youtube_videos_interactions"] = youtube_videos.loc[
#     :,
#     [
#         "n_views",
#         "n_likes",
#         "n_dislikes",
#         "n_comments",
#     ],
# ].sum(axis=1)


# youtube_videos["date"] = pd.to_datetime(youtube_videos["date"])


# ### DailyCreation 
# youtube_videos_creations = (
#     youtube_videos.groupby(['date', 'year', 'month', 'dayofmonth', 'hour'])
#     .agg({'id':'count', 'ch_id': 'nunique', 'youtube_videos_interactions':'sum'}).reset_index()
#     .rename(columns={'id':'youtube_videos', 'ch_id':'by_#channels'})
#     .sort_values('youtube_videos', ascending=False)
# )

# -------------------------------------------------------------------------------------------------------------------------------

# Compare Interactions
# LOAD YouTube Video DATA
videos = pd.read_csv("../../YouTube_Bot_Analysis/new_data/all_vid_data_7613v.csv")
youtube_videos = helpers.clean_youtube_videos(videos)

# Filter on 2018-2022
youtube_videos = youtube_videos[youtube_videos["p_dtime"].dt.year.isin([2018, 2019, 2020, 2021, 2022])]

youtube_videos["youtube_videos_interactions"] = youtube_videos.loc[
    :,
    [
        "n_views",
        "n_likes",
#         "n_dislikes",
        "n_comments",
    ],
].sum(axis=1)


### DailyCreation 
youtube_videos_creations = (
    youtube_videos.groupby(['date', 'year', 'month', 'dayofmonth', 'hour'])
    .agg({'id':'count', 'ch_id': 'nunique', 'youtube_videos_interactions':'sum'}).reset_index()
    .rename(columns={'id':'youtube_videos', 'ch_id':'by_#channels'})
    .sort_values('youtube_videos', ascending=False)
)

# -------------------------------------------------------------------------------------------------------------------------------

### Merge DailyCreation DataFrames

cols = ['date', 'year', 'month', 'dayofmonth', 'hour']
tmp = df_creations_twitter.merge(df_creations_youtube, on=cols, how='outer')
tmp2 = tmp.merge(df_creations_instagram, on=cols, how='outer') 
tmp3 = tmp2.merge(df_creations_reddit, on=cols, how='outer') 
df_creations = tmp3.merge(youtube_videos_creations, on=cols, how='outer') 

# -------------------------------------------------------------------------------------------------------------------------------








