#!/usr/bin/env python
# coding: utf-8

# In[1]:


from elasticsearch import Elasticsearch
from pandasticsearch import Select
import pandas as pd
import pickle
pd.options.mode.chained_assignment = None

es_hostname = "----"
es = Elasticsearch([es_hostname])


# In[28]:


def helper_query_es(es, index, query):
    size = 10000
    # Init scroll by search
    data = es.search(
        index=index,
        scroll='2m',
        size=size,
        body=query
    )
    # Get the scroll ID
    sid = data['_scroll_id']
    scroll_size = len(data['hits']['hits'])
    hits = []
    i = 0
    while scroll_size > 0:
        # Before scroll, process current batch of hits
        for hit in data['hits']['hits']:
            hits.append(hit)
        # process_hits(data['hits']['hits'])
        data = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = data['_scroll_id']
        # Get the number of results returned in the last scroll
        scroll_size = len(data['hits']['hits'])
    es.clear_scroll(scroll_id=sid)
    result_dict = {'took': 0, 'hits': {'hits': hits}}
    return result_dict


# In[ ]:


# Use dates19 for data from 2019, dates20 for 2020 etc...


# In[29]:


tweets = pd.DataFrame()

dates21 = ['2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01', '2021-05-01']

dates20 = ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01', '2020-08-01',
         '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-01', '2021-01-01']

dates19 = ['2019-01-01', '2019-02-01', '2019-03-01', '2019-04-01', '2019-05-01', '2019-06-01', '2019-07-01', '2019-08-01',
         '2019-09-01', '2019-10-01', '2019-11-01', '2019-12-01', '2020-01-01']

dates18 = ['2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01', '2018-06-01', '2018-07-01', '2018-08-01',
         '2018-09-01', '2018-10-01', '2018-11-01', '2018-12-01', '2019-01-01']

for i in range(0, len(dates20)-1):
    start = dates21[i]
    end = dates21[i+1]
    query = {"query": {
        "range": {
          "created_at": {
            "gte": start,
            "lt": end,
            "format": "yyyy-MM-dd"
          }
        }
      }, "_source": ['id_str','created_at','full_text', 'lang', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 
                            'entities.hashtags', 'entities.media', 'entities.symbols', 'entities.urls', 'entities.user_mentions',
                           'source', 'retweeted_status.id_str','retweeted_status.created_at','retweeted_status.full_text', 'retweeted_status.lang', 'retweeted_status.in_reply_to_status_id_str', 'retweeted_status.in_reply_to_user_id', 
                            'retweeted_status.entities.hashtags', 'retweeted_status.entities.media', 'retweeted_status.entities.symbols', 'retweeted_status.entities.urls', 'retweeted_status.entities.user_mentions',
                           'retweeted_status.user.id_str', 'retweeted_status.user.screen_name', 'retweeted_status.source', 'quoted_status.id_str','quoted_status.created_at','quoted_status.full_text', 'quoted_status.lang', 'quoted_status.in_reply_to_status_id_str', 'quoted_status.in_reply_to_user_id', 
                            'quoted_status.entities.hashtags', 'quoted_status.entities.media', 'quoted_status.entities.symbols', 'quoted_status.entities.urls', 'quoted_status.entities.user_mentions',
                           'quoted_status.user.id_str', 'retweeted_status.user.screen_name', 'quoted_status.source',
                    'user.id_str','user.created_at', 'user.description', 'user.followers_count', 'user.friends_count', 'user.lang', 'user.location', 'user.name', 'user.screen_name', 'user.profile_banner_url', 'user.profile_image_url', 'user.statuses_count', 'user.url', 'user.verified']}
    res = helper_query_es(es, "tweets", query)
    tweets_tmp = Select.from_dict(res).to_pandas()
    del res
    # tweets_tmp = tweets_tmp.filter(['id_str','created_at','full_text', 'lang', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 
#                             'entities.hashtags', 'entities.media', 'entities.symbols', 'entities.urls', 'entities.user_mentions',
#                            'user.id_str', 'source',
#                            'retweeted_status.id_str','retweeted_status.created_at','retweeted_status.full_text', 'retweeted_status.lang', 'retweeted_status.in_reply_to_status_id_str', 'retweeted_status.in_reply_to_user_id', 
#                             'retweeted_status.entities.hashtags', 'retweeted_status.entities.media', 'retweeted_status.entities.symbols', 'retweeted_status.entities.urls', 'retweeted_status.entities.user_mentions',
#                            'retweeted_status.user.id_str', 'retweeted_status.user.screen_name', 'retweeted_status.source',
#                            'quoted_status.id_str','quoted_status.created_at','quoted_status.full_text', 'quoted_status.lang', 'quoted_status.in_reply_to_status_id_str', 'quoted_status.in_reply_to_user_id', 
#                             'quoted_status.entities.hashtags', 'quoted_status.entities.media', 'quoted_status.entities.symbols', 'quoted_status.entities.urls', 'quoted_status.entities.user_mentions',
#                            'quoted_status.user.id_str', 'retweeted_status.user.screen_name' 'quoted_status.source'], axis=1)
    tweets = pd.concat([tweets, tweets_tmp])
    del tweets_tmp
    print(len(tweets))
    print(i)
    


# In[30]:


tweets = tweets.filter(['id_str','created_at','full_text', 'lang', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 
                            'entities.hashtags', 'entities.media', 'entities.symbols', 'entities.urls', 'entities.user_mentions',
                            'source', 'retweeted_status.id_str','retweeted_status.created_at','retweeted_status.full_text', 'retweeted_status.lang', 'retweeted_status.in_reply_to_status_id_str', 'retweeted_status.in_reply_to_user_id', 
                            'retweeted_status.entities.hashtags', 'retweeted_status.entities.media', 'retweeted_status.entities.symbols', 'retweeted_status.entities.urls', 'retweeted_status.entities.user_mentions',
                           'retweeted_status.user.id_str', 'retweeted_status.user.screen_name', 'retweeted_status.source', 'quoted_status.id_str','quoted_status.created_at','quoted_status.full_text', 'quoted_status.lang', 'quoted_status.in_reply_to_status_id_str', 'quoted_status.in_reply_to_user_id', 
                            'quoted_status.entities.hashtags', 'quoted_status.entities.media', 'quoted_status.entities.symbols', 'quoted_status.entities.urls', 'quoted_status.entities.user_mentions',
                           'quoted_status.user.id_str', 'retweeted_status.user.screen_name', 'quoted_status.source',
                    'user.id_str','user.created_at', 'user.description', 'user.followers_count', 'user.friends_count', 'user.lang', 'user.location', 'user.name', 'user.screen_name', 'user.profile_banner_url', 'user.profile_image_url', 'user.statuses_count', 'user.url', 'user.verified'], axis=1)


# In[31]:


tweets['created_at'] = pd.to_datetime(tweets['created_at'])
tweets['user.created_at'] = pd.to_datetime(tweets['user.created_at'])
with open('tweets21.obj', 'wb') as fp:
    pickle.dump(tweets, fp)


# In[6]:


# res = helper_query_es(es, 'tweets', {"query": {"match_all": {}}, "fields": ['id_str','created_at','full_text', 'lang', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 
#                             'entities.hashtags', 'entities.media', 'entities.symbols', 'entities.urls', 'entities.user_mentions',
#                            'user.id_str', 'source', 'retweeted_status.id_str','retweeted_status.created_at','retweeted_status.full_text', 'retweeted_status.lang', 'retweeted_status.in_reply_to_status_id_str', 'retweeted_status.in_reply_to_user_id', 
#                             'retweeted_status.entities.hashtags', 'retweeted_status.entities.media', 'retweeted_status.entities.symbols', 'retweeted_status.entities.urls', 'retweeted_status.entities.user_mentions',
#                            'retweeted_status.user.id_str', 'retweeted_status.user.screen_name', 'retweeted_status.source', 'quoted_status.id_str','quoted_status.created_at','quoted_status.full_text', 'quoted_status.lang', 'quoted_status.in_reply_to_status_id_str', 'quoted_status.in_reply_to_user_id', 
#                             'quoted_status.entities.hashtags', 'quoted_status.entities.media', 'quoted_status.entities.symbols', 'quoted_status.entities.urls', 'quoted_status.entities.user_mentions',
#                            'quoted_status.user.id_str', 'retweeted_status.user.screen_name' 'quoted_status.source']})

# df = Select.from_dict(res).to_pandas()
# del res
# df['created_at'] = pd.to_datetime(df['created_at'])
# df['user.created_at'] = pd.to_datetime(df['user.created_at'])


# In[32]:


print(tweets)


# In[33]:


tweets[['id_str', 'created_at', 'full_text', 'user.id_str', 'user.screen_name', 'user.name', 'user.created_at', 'user.description', 'user.profile_image_url', 'user.profile_banner_url', 'user.url', 'user.statuses_count', 'user.followers_count', 'user.friends_count']].to_csv('tweets_2021_lite.csv', mode = 'w' ,index=False, header=True)


# In[34]:


tweets.to_csv('tweets_2021.csv', mode = 'w' ,index=False, header=True)


# In[35]:


tweets.drop_duplicates(subset=['user.id_str'], keep='last')[['user.id_str', 'user.screen_name', 'user.name', 'user.created_at', 'user.description', 'user.profile_image_url', 'user.profile_banner_url', 'user.url', 'user.statuses_count', 'user.followers_count', 'user.friends_count']].to_csv('users_2021.csv', mode = 'w' ,index=False, header=True)


# In[36]:


tmp = tweets.drop_duplicates(subset=['user.id_str'], keep='last')
tmp = tmp[tmp['user.created_at'].dt.year == 2021]
tmp[['user.id_str', 'user.screen_name', 'user.name', 'user.created_at', 'user.description', 'user.profile_image_url', 'user.profile_banner_url', 'user.url', 'user.statuses_count', 'user.followers_count', 'user.friends_count']].to_csv('users_created_in_2021.csv', mode = 'w' ,index=False, header=True)


# In[37]:


created_2020 = tweets[tweets['user.created_at'].dt.year == 2021]

daily_distribution = created_2020.groupby(pd.Grouper(freq='1D', key='user.created_at')).agg({'user.id_str': pd.Series.nunique})


# In[38]:


daily_distribution.reset_index().to_csv('daily_creation21.csv', mode = 'w' ,index=False, header=True)

