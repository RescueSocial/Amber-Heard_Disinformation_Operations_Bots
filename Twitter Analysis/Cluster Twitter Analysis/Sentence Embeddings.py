#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pandas as pd
import pickle
import re
import itertools
import leidenalg
import igraph


from wordcloud import WordCloud
from IPython.display import Image, HTML
import matplotlib.pyplot as plt
import numpy as np

import umap.umap_ as umap
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import stopwordsiso as stopwords
import hdbscan
from scipy.spatial.distance import squareform
from scipy.special import binom
import preprocessor.api as p
import emoji
from sklearn.preprocessing import Normalizer
import scipy.sparse
import tensorflow_hub as hub
import tensorflow as tf
import collections

pd.options.mode.chained_assignment = None


# In[3]:


# Loading the embedder


# In[4]:


embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")


# In[13]:


year = '22'


# In[14]:


with open('data/tweets{0}.obj'.format(year), 'rb') as fp:
    tweets_users = pickle.load(fp)


# In[7]:


# Function to save clusters in html file


# In[15]:


def path_to_image_html(path):
    return '<img src="'+ path + '" style=max-height:124px;"/>'

def output_clusters(groups, df_month_lang, month, lang, folder):
    i=0
    stop_words = ["https", "RT"] + list(stopwords.stopwords(lang)) + list(stopwords.stopwords('en'))
    lenghts = []
    
    for c, group in groups.items():
        if c == -1:
            continue
        if len(group) < 10:
            continue
        lenghts.append(len(group))
            
    fig, ax = plt.subplots()
    ax.bar(np.arange(1, max(lenghts) + 1), np.bincount(lenghts, minlength= max(lenghts))[1:])
    display(fig)
    plt.close()
    
    with open(folder + '/data/' + lang + '/' + month[1] +'/cluster', 'wb') as fp:
        pickle.dump(groups, fp)
    
    with open(folder + '/data/' + lang + '/' + month[1] +'/cluster.txt', 'w') as file:
        for c, group in groups.items():
            if c == -1:
                continue
                
            i = i + 1
            print("CLUSTER: " + str(c) +"\tLEN: "+ str(len(group)))
            
            #users_month = df_month_lang[df_month_lang['user.meta.account_updated'].dt.month == month[0]]
            users_month = df_month_lang.drop_duplicates('user.id_str',keep='last')
            # print(users_month[users_month['user.id_str'].duplicated() == True])
            # print(len(users_month))
            features = ['user.id_str', 'user.screen_name', 'user.name', 'user.created_at','user.location', 'user.followers_count', 'user.friends_count', 'user.statuses_count', 'user.profile_image_url', 'user.profile_banner_url', 'user.lang']

            tmp = users_month[users_month['user.id_str'].isin([str(gr) for gr in group])][features].drop_duplicates()
            
            tmp= tmp.rename(columns = {'user.profile_image_url':'profile_image_url'})
            tmp= tmp.rename(columns = {'user.profile_banner_url':'profile_banner_url'})
            
            html = HTML(tmp.to_html(folder + '/viz/' + lang + '/' + month[1] + '/' + str(c) +'.html', escape=False, formatters=dict(profile_image_url=path_to_image_html, profile_banner_url=path_to_image_html)))
            tmp.to_csv(folder + '/data/' + lang + '/' + month[1] + '/'+ str(c) + '.csv')            
            
            cluster_tweeets = df_month_lang[df_month_lang['user.id_str'].isin(list([str(gr) for gr in group]))]
            cluster_tweeets.to_json(folder + '/data/' + lang + '/' + month[1] + '/tweets' + str(c) + '.json', orient='records')

            #create wordcloud
            full_text = ' '.join(df_month_lang[df_month_lang['user.id_str'].isin([str(gr) for gr in group])]['full_text'])
            
            wordcloud = WordCloud(width=2000, height = 2000, min_font_size = 8, max_words = 20, stopwords = stop_words, background_color='white', colormap='tab20', collocations=False).generate(full_text)
            fig = plt.figure( figsize=(20,20) )
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.tight_layout(pad=0)
            plt.savefig(folder + '/viz/' + lang + '/' + month[1] + '/wordcloud_'+ str(c) + '.png')
            display(fig)
            plt.close()
            
            with open(folder + '/viz/' + lang + '/' + month[1] + '/' + str(c) +'.html', 'r+') as html_page:
                content = html_page.read()
                html_page.seek(0, 0)
                html_page.write('<img src="wordcloud_'+ str(c) + '.png' + '" style="display: block;width: 350px;margin-left: auto;margin-right: auto;" />' + '<br>' + content)
            
            file.write("len cluster "+ str(c) +":\t"+str(len(group))+"\n")


# In[16]:


# Function to do community detection


# In[17]:


def communities(edges, month, lang):
    edges.columns = ['source','target','weight']
   
    tuples = [tuple(x) for x in edges.values]
    G = igraph.Graph.TupleList(tuples, directed = False, edge_attrs=['weight'])
    del tuples
    partition = leidenalg.find_partition(G, leidenalg.ModularityVertexPartition)
    
    partition = partition.membership
    
    dc = pd.DataFrame()
    dc['name'] = G.vs['name']
    del G
    dc['cluster'] = partition
    del partition
    # here you can change the community detection algorithm to use
    clus = dc.groupby(['cluster'])['name'].apply(lambda grp: list(grp.value_counts().index)).to_dict()
    return clus

def create_graph(data):
    print('Started')
    net = pd.DataFrame(columns = ['from', 'to'])
    links = []
    tmp = data[['cluster','user.id_str']].groupby('cluster').count().reset_index()
    tmp2 = tmp[tmp['user.id_str']>2].sort_values('user.id_str', ascending=False)
    tmp_list = tmp2['cluster'].unique()
    for el in tmp_list:
        users = data.loc[data['cluster'] == el]
        links += list(itertools.combinations(users['user.id_str'].sort_values().unique(), 2))
    print('Done')
    print('Converting links in dataframe')
    net = pd.DataFrame(links, columns=['from', 'to'])
    print('Done')
    return net


# In[18]:


# For each month, finds clusters


# In[19]:


# months = [(1, 'jan'), (2, 'feb'), (3, 'mar'), (4, 'apr'), (5, 'may'), (6, 'jun'), (7, 'jul'), (8, 'aug'), (9, 'sep'), (10, 'oct'), (11, 'nov'), (12, 'dec')]
months = [(1, 'jan'), (2, 'feb'), (3, 'mar'), (4, 'apr')]

# months = [(11, 'nov'), (12, 'dec')]

langs = ['en']
for i in months:
    df_month = tweets_users[tweets_users['created_at'].dt.month == i[0]]
    for lang in langs:
        
        if not os.path.exists('result/' + year + '/'):
            os.makedirs('result/' + year + '/')
        if not os.path.exists('result/' + year + '/data'):
            os.makedirs('result/' + year + '/data')
        if not os.path.exists('result/' + year + '/data' + '/' + lang):
            os.makedirs('result/' + year + '/data' + '/' + lang)
        if not os.path.exists('result/' + year + '/data' + '/' + lang + '/' + i[1]):
            os.makedirs('result/' + year + '/data' + '/' + lang + '/' + i[1])
        
        if not os.path.exists('result/' + year + '/viz'):
            os.makedirs('result/' + year + '/viz')
        if not os.path.exists('result/' + year + '/viz' + '/' + lang):
            os.makedirs('result/' + year + '/viz' + '/' + lang)
        if not os.path.exists('result/' + year + '/viz' + '/' + lang + '/' + i[1]):
            os.makedirs('result/' + year + '/viz' + '/' + lang + '/' + i[1])
        
        df_month_lang = df_month[df_month['lang'] == lang]
        df_month_lang['proc_text'] = df_month_lang['full_text']
        df_month_lang['proc_text'] =df_month_lang['proc_text'].apply(lambda text: emoji.get_emoji_regexp().sub("",text).strip())
        df_month_lang['proc_text'] =df_month_lang['proc_text'].apply(lambda text: re.sub(r'[^\w\s]',' ',text))


        df_month_lang['proc_text'] = df_month_lang['proc_text'].apply(lambda text: p.clean(text))
        df_month_lang['proc_text'] = df_month_lang['proc_text'].apply(lambda text: re.sub(r'[^\w\s]',' ',text))
        df_month_lang['proc_text'] = df_month_lang['proc_text'].apply(lambda text: re.sub(r'\n',' ',text))
        df_month_lang['proc_text'] = df_month_lang['proc_text'].apply(lambda text: str(text).strip())
        df_month_lang['proc_text'] = df_month_lang['proc_text'].apply(lambda text: re.sub(r' +',' ',text))

        data = df_month_lang['proc_text'].values
        
        embeddings = embed(data)
        
        model = umap.UMAP(metric="cosine")
        embeddings_umap = model.fit_transform(embeddings)
        
        labels = hdbscan.HDBSCAN(core_dist_n_jobs=-1, cluster_selection_method='leaf').fit_predict(embeddings_umap)
        
        df_month_lang['cluster'] = labels
        
        with open('result/' + year + '/data' + '/' + lang + '/' + i[1] +'/dataframe', 'wb') as fp:
            pickle.dump(df_month_lang, fp)
        
        df_month_lang_clean = df_month_lang[df_month_lang['cluster'] != -1]
        
        net = create_graph(df_month_lang_clean)
        edges = net.groupby(['from','to']).size().reset_index()
        del net
        edges.columns = ['from','to','label']
        edges.reset_index().to_csv('result/' + year + '/data' + '/' + lang + '/' + i[1] + '/edges_' + i[1] + '_'  + lang + '.csv')

        clusters = communities(edges, i[1], lang)
        
        output_clusters(clusters, df_month_lang, i, lang, 'result/' + year + '/')

