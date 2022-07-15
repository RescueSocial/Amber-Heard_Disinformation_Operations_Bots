import plotly.io as pio
from datetime import datetime
import pandas as pd
import os
import ast
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import warnings
import re
import seaborn as sb

warnings.filterwarnings("ignore")


def isnull(df):
    for col in df.columns:
        print(f"The number of NaNs in {col}:", df[col].isnull().sum())


def get_top(df, col, n, column_name, count_name):
    """
    A function return neat df to be plotted (count categorical values)
    Args:
        - df--> data frame
        - col --> ctegorical values column.
        - n --> number of records to show (0 --> means all)
        - column_name --> categorical value to be named
        - count_name --> count column name
    Return:
        - df of two columns (categorical values and counter)
    """
    if n != 0:
        return (
            df[col]
            .value_counts()
            .head(n)
            .to_frame()
            .reset_index()
            .rename(columns={"index": column_name, col: count_name})
        )
    else:
        return (
            df[col]
            .value_counts()
            .to_frame()
            .reset_index()
            .rename(columns={"index": column_name, col: count_name})
        )


def pie(df, title, c=0):
    """
    A function to plot pie graph
    Args:
        - df--> DataFrame.
        - title --> the graph title
    """
    colors = px.colors.qualitative.T10
    
    fig = px.pie(
        df,
        values=f"{df.columns[1]}",
        names=f"{df.columns[0]}",
        color_discrete_sequence = colors if c==0 else c,
        title=title,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label+value",
        textfont=dict(size=12, color="white"),
    )
    fig.show("svg")
    
    
# https://plotly.com/python/discrete-color/    
def go_pie(title, labels, values, c=px.colors.qualitative.T10):  
    labels = labels
    values = values
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    
    fig.update_traces(textinfo='percent+label+value', 
                      textfont=dict(size=12, color="white"),
                      marker=dict(colors=c))
    fig.update_layout(title=title, font=dict(size=18))
    fig.show("svg")
    


def bar(df, x, y, title, text=0, margin=np.inf):
    """
    A function to plot bar graph
    Args:
        - df--> DataFrame.
        - x --> x axis values.
        - y --> y axis values.
        - text --> values for text.
        - margin --> margin value.
        - title --> the graph title.
    """
    if text == 0:
        text = y
    fig = px.bar(df, x=f"{x}", y=f"{y}", text=f"{y}", title=title)

    fig.update_layout(xaxis=dict(title=f"{x}", tickmode="linear", dtick=1))

    clrs = ["red" if (y > margin) else "#5296dd" for y in df[f"{y}"]]

    fig.update_traces(
        marker_color=clrs, marker_line_width=1.5, opacity=1, textposition="auto"
    )
    fig.show("svg")


def barh(df, title, threshold=float("inf"), c=0):
    """
    A function to plot barh graph
    Args:
        - df--> DataFrame.
        - title --> the graph title.
        - threshold --> plot in red if excced the value.
    """
    clrs = ["red" if (y > threshold) else "#5296dd" for y in df[f"{df.columns[1]}"]]

    fig = (
        px.bar(
            df,
            y=f"{df.columns[0]}",
            x=f"{df.columns[1]}",
            text=f"{df.columns[1]}",
            height=500,
            title=title,
        )
        .update_traces(marker_color=c if c != 0 else clrs)
        .update_layout()
    )

    fig.update_yaxes(autorange="reversed")
    fig.show("svg")


def bar_peaks(df_head, title, threshold=0, xlabel='tweets Creation Date'):
    """
    A function to plot bar graph for peaks
    Args:
        - df_head -->  dataframe contains top values.
        - title --> the graph title.
    """
    fig = px.bar(df_head, x=f"{df_head.columns[0]}", y=f"{df_head.columns[1]}", 
                 text=f"{df_head.columns[1]}", title=title)

    fig.update_layout(
        xaxis=dict(
            title=xlabel, tickmode="array", tickvals=df_head[f"{df_head.columns[0]}"]
        )
    )

    clrs = ["red" if (y > threshold) else "#5296dd" for y in df_head[f"{df_head.columns[1]}"]]
    fig.update_traces(marker_color=clrs, opacity=1, textposition="auto")
    fig.update_xaxes(tickangle=45)
    fig.show("svg")

def contr_peaks(df, user, n=5, threshold=0):
    """
    A function to filter user contributions and plot bar graph for peaks
    Args:
        - df --> the dataframe to be used.
        - user (str) --> the username to filter on.
    """
    df_user = df.query(" username == @user ")
    print(f'\ntotal number of tweets by "{user}": {df_user.shape[0]}')
    df_user_daily = df_user.groupby('date')['text'].count().to_frame().reset_index().rename(columns={'text': 'ntweets'})
    df_user_daily.sort_values(['ntweets', 'date'], ascending=[False, False], inplace=True)
    
    bar_peaks(df_user_daily.head(n), f'"{user}"' + ' Top Contributions', threshold=threshold)
    
def keyword_peaks(df, keyword, n=5, threshold=0):
    """
    A function to filter on specific keyword contributions and plot bar graph for peaks
    Args:
        - df --> the dataframe to be used.
        - keyword (str) --> the keyword to filter on.
    """
    df_keyword = df[df.text.str.contains(keyword)]
    df_keyword_daily = df_keyword.groupby('date')['text'].count().to_frame().reset_index().rename(columns={'text': 'ntweets'})
    df_keyword_daily.sort_values(['ntweets', 'date'], ascending=[False, False], inplace=True)
    
    bar_peaks(df_keyword_daily.head(n), f'"{keyword}"' + ' Peak Contributions', threshold=threshold)
    
def text_peaks(df, mytext, n=5, threshold=0):
    """
    A function to filter on specific text contributions and plot bar graph for peaks
    Args:
        - df --> the dataframe to be used.
        - mytext (str) --> the text to filter on.
    """
    df_text = df[df.text == mytext]
    df_text_daily = df_text.groupby('date')['text'].count().to_frame().reset_index().rename(columns={'text': 'ntweets'})
    df_text_daily.sort_values(['ntweets', 'date'], ascending=[False, False], inplace=True)
    
    bar_peaks(df_text_daily.head(n), f'"{mytext}"' + ' Peak Contributions', threshold=threshold)
    
def text_all_peaks(df, mytext, n=5, threshold=0):
    """
    A function to filter on specific text contributions and plot bar graph for peaks
    Args:
        - df --> the dataframe to be used.
        - mytext (str) --> the text to filter on.
    """
    df_text = df[df.text.str.contains(mytext)]
    df_text_daily = df_text.groupby('date')['text'].count().to_frame().reset_index().rename(columns={'text': 'ntweets'})
    df_text_daily.sort_values(['ntweets', 'date'], ascending=[False, False], inplace=True)
    
    bar_peaks(df_text_daily.head(n), f'"{mytext}"' + ' Peak Contributions', threshold=threshold)

def users_peaks(df, mytext, n=5, threshold=0, xlabel='UserName'):
    """
    A function to filter on specific text contributions and plot bar graph for peaks
    Args:
        - df --> the dataframe to be used.
        - mytext (str) --> the text to filter on.
    """
    df_text = df[df.text == mytext]
    df_text_users = df_text.username.value_counts().to_frame().reset_index().rename(columns={'index': 'username',
                                                                                             'username': 'ntweets'})
    
    bar_peaks(df_text_users.head(n), f'"{mytext}"' + ' Top Commented Users', threshold=threshold, xlabel=xlabel)

def users_all_peaks(df, mytext, n=5, threshold=0, xlabel='UserName'):
    """
    A function to filter on specific text contributions and plot bar graph for peaks
    Args:
        - df --> the dataframe to be used.
        - mytext (str) --> the text to filter on.
    """
    df_text = df[df.text.str.contains(mytext)]
    df_text_users = df_text.username.value_counts().to_frame().reset_index().rename(columns={'index': 'username',
                                                                                             'username': 'ntweets'})
    
    bar_peaks(df_text_users.head(n), f'"{mytext}"' + ' Top Commented Users', threshold=threshold, xlabel=xlabel)
    
# # Same as bar_peaks     
# def bar_dates(df, title, threshold=float("inf")):
#     fig = px.bar(df, x="date", y="ntweets", text="ntweets")

#     fig.update_layout(
#         title={"text": title, "x": 0.5, "xanchor": "center", "yanchor": "top"}
#     )
#     fig.update_layout(xaxis=dict(title="tweets Creation Date", tickmode="linear"))

#     clrs = ["red" if (y > threshold) else "#5296dd" for y in df["ntweets"]]
#     fig.update_traces(
#         marker_color=clrs, marker_line_width=1.5, opacity=1, textposition="auto"
#     )
#     fig.update_xaxes(tickangle=45)
#     fig.show("svg")
    

def draw_heatmap(*args, **kwargs):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = kwargs.pop('data')
    d = data.pivot(index=args[1], columns=args[0], values=args[2])
    d = d.reindex(index=months[::-1])
    sb.heatmap(d, **kwargs)    

def facet_heat(df, title='title', heat_col='n_tweets', n_col=2, vmax=100):
    g = sb.FacetGrid(df, col='year', col_wrap=n_col, height=4.5)
    g.map_dataframe(draw_heatmap, 'dayofmonth', 'month', heat_col, cmap='rocket_r', vmin=0, vmax=vmax);

    plt.suptitle(title, y=1.06, fontsize=22)
    g.set_titles("{col_name}", size=16)
#     g.set_yticklabels(size = 4)
#     g.set_xticklabels(size = 8)
   
    g.fig.subplots_adjust(wspace=0.18, hspace=0.2)
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True, labelleft=True)
        axis.set_yticklabels(axis.get_yticklabels(), rotation=0)
    
    
def facet_day_month(df, x, y, facet_on='month', n_col=4, year_str='2018'):
    """
    A function to plot bar graph for all months
    Args:
        - df -->  dataframe.
    """
    months_ordered = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",]
    days_ordered = list(range(1, 32, 2))

    g = sb.FacetGrid(data=df, col=facet_on, col_wrap=n_col, col_order=months_ordered if facet_on=='month' else None)
    g.map(sb.barplot, x, y, 
          order=days_ordered if facet_on=='month' else months_ordered, 
          palette=["#5296dd"])
    
    g.set_xticklabels(rotation=90)
    g.set_titles("{col_name}", size=16, y=-0.30)
    
    if facet_on=='month':
        title = '"Aquman Petition" ' + y + ' Created in Each Day of ' + year_str 
    else:
        title = '"Aquman Petition" ' + y + ' Created in Each Month'
    g.fig.suptitle(title, fontsize=22, y=1.05)
#     g.set_yticklabels(size = 4)
#     g.set_xticklabels(size = 10)

    g.fig.subplots_adjust(wspace=0.1, hspace=0.32)
    g.set_xlabels("")
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True)
        
        
# https://matplotlib.org/stable/gallery/color/named_colors.html
def months_cross(df_month, x="month", y="contributions", facet_on='year', n_col=2, h=5, loc=-0.17, ratio=1.3, fs=8, 
                 year_str='', c=None):
    """
    A function to plot bar graph for all months (CrossPlatforms)
    Args:
        - df -->  dataframe.
    """
    months_ordered = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",]
    g = sb.catplot(data=df_month, x=x, y=y, hue='type', col=facet_on, kind='bar', col_wrap=n_col, 
           order=months_ordered, aspect=ratio, height=h, palette=c);

    g.set_xticklabels(rotation=90, fontsize=fs)
    g.set_ylabels(fontsize=fs)
    g.set_titles("{col_name}", size=16, y=loc) 
    plt.suptitle(f"CrossPlatforms {y} over Months ({year_str})", y=1.01, fontsize=22)
    
    g.fig.subplots_adjust(wspace=0.18, hspace=0.25)
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True, labelleft=True)
        axis.set_yticklabels(axis.get_yticklabels(), rotation=0, fontsize=fs)
        
    import matplotlib.ticker as tkr
    for ax in g.axes.flatten():
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=fs)
#         ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y, pos: '{:,.0f}'.format(y/1000) + 'K'))
        ax.yaxis.set_major_formatter(tkr.EngFormatter())
        

def days_cross(df, x="dayofmonth", y="contributions", facet_on='month', n_col=2, h=5, loc=-0.2, ratio=1.3, fs=8, 
               year_str='', c=None):
    """
    A function to plot bar graph for all days (CrossPlatforms)
    Args:
        - df -->  dataframe.
    """
    days_ordered = list(range(1, 32, 2))
    months_ordered = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",]
    g = sb.catplot(data=df, x=x, y=y, hue='type', col=facet_on, kind='bar', col_wrap=n_col, col_order=months_ordered,
           order=days_ordered, aspect=ratio, height=h, palette=c);

    g.set_xticklabels(rotation=90, fontsize=fs)
    g.set_ylabels(fontsize=fs)
    g.set_titles("{col_name}", size=16, y=loc) 
    plt.suptitle(f"CrossPlatforms {y} over Days ({year_str})", y=1.01, fontsize=22)
    
    g.fig.subplots_adjust(wspace=0.18, hspace=0.25)
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True, labelleft=True)
        axis.set_yticklabels(axis.get_yticklabels(), rotation=0, fontsize=fs)
    
    import matplotlib.ticker as tkr
    for ax in g.axes.flatten():
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=fs)
#         ax.yaxis.set_major_formatter(tkr.FuncFormatter(lambda y, pos: '{:,.0f}'.format(y/1000) + 'K'))
        ax.yaxis.set_major_formatter(tkr.EngFormatter())
        


def get_amber_text(row):
    """
    A function to get texts related to amber.
    Args:
        - row -->  row of column in df.
    """
    row = row.lower()
    result = list(set(re.findall(r"#?[a-z\s]*amber[a-z\s]*", row)))
    neat = []
    for i in result:
        neat.append(i.strip())
    return neat



# -------------------------------------------------------------------------------------------------

def clean_youtube_comments(df):
    """   
    INPUT: YouTube Comments DataFrame
    OUTPUT: Cleaned YouTube Comments DataFrame
    """
    
    df.drop_duplicates(inplace=True)

# 0) Filter on Specific columns
    cols_to_drop = {'kind', "snippet.topLevelComment.kind", "snippet.topLevelComment.snippet.videoId",
                    "snippet.topLevelComment.snippet.textDisplay", "snippet.topLevelComment.snippet.authorProfileImageUrl",
                    "snippet.topLevelComment.snippet.authorChannelUrl", "snippet.topLevelComment.snippet.canRate", 
                    "snippet.topLevelComment.snippet.viewerRating", "snippet.canReply", "snippet.isPublic" }
    df.drop(columns=cols_to_drop, inplace=True)
    

# 1) Rename Columns & Change Dtypes
    df.rename(columns={"snippet.videoId": "video_id",
                          "snippet.topLevelComment.etag": "tl_etag",
                          "snippet.topLevelComment.id": "tl_id",
                          "snippet.topLevelComment.snippet.textOriginal": "tl_text",
                          "snippet.topLevelComment.snippet.authorDisplayName": "tl_username",
                          "snippet.topLevelComment.snippet.authorChannelId.value": "tl_author_ch_id",
                          "snippet.topLevelComment.snippet.likeCount": "tl_nlikes",
                          "snippet.topLevelComment.snippet.publishedAt": "tl_p_dtime",
                          "snippet.topLevelComment.snippet.updatedAt": "tl_u_dtime",
                          "snippet.totalReplyCount": "tl_nreplies",
                          "snippet.topLevelComment.snippet.moderationStatus": "tl_moderation_status",
                          'replies.comments': "replies_data"}, inplace=True);
    
    df.drop_duplicates(subset=['tl_id'], inplace=True)
    
    
#     Extracting The replies.comments Data
    df_filterd = df[df['replies_data'].notnull()]

    replies_list = [] 
    for reply in df_filterd['replies_data']:
        reply_list = ast.literal_eval(reply)
        replies_list += reply_list # Sine we cannot append more than one element at a time
        
      
    df_replies = pd.json_normalize(replies_list)
    
    drop_list = ['kind', 'snippet.viewerRating', 'snippet.canRate']
    df_replies.drop(columns=drop_list, inplace=True)
    
    df.drop(columns='id', inplace=True)
    
    df_replies.rename(columns={'snippet.videoId': 'video_id', 
                   'snippet.parentId': 'tl_id', 
                   'snippet.textDisplay': 'text_display', 
                   'snippet.textOriginal': 'text_original', 
                   'snippet.authorDisplayName': 'username', 
                   'snippet.authorProfileImageUrl': 'author_profile_image', 
                   'snippet.authorChannelUrl': 'author_ch_url', 
                   'snippet.authorChannelId.value': 'author_ch_id', 
                   'snippet.likeCount': 'nlikes', 
                   'snippet.publishedAt': 'p_dtime', 
                   'snippet.updatedAt': 'u_dtime', 
                   'snippet.moderationStatus': 'moderation_status'}
          , inplace=True)
    
    
#     Merging both the TopLevel and Replies DataFrames
# Preparing For Restructring the data

    # Comments Data
    # Add a Column to Classify after concatenating
    df['comment_reply'] = 'comment'
    
    df['parent_id'] = 'none'
    df['author_ch_url'] = 'none'
    df['author_profile_image'] = 'none'
    # Drop
    df.drop(columns=['etag', 'replies_data'], inplace=True)
    
    # Rename
    df.rename(columns={'tl_etag': 'comment_etag', 
                   'tl_id': 'comment_id', 
                   'tl_text': 'text', 
                   'tl_username': 'username', 
                   'tl_author_ch_id': 'author_ch_id', 
                   'tl_nlikes': 'nlikes', 
                   'tl_p_dtime': 'p_dtime', 
                   'tl_u_dtime': 'u_dtime', 
                   'tl_nreplies': 'nreplies', 
                   'tl_moderation_status': 'moderation_status'}
          , inplace=True)
    
    # Replies Data
    # Add a Column to Classify after concatenating
    df_replies['comment_reply'] = 'reply'
    df_replies['nreplies'] = 0
    # Drop
    df_replies.drop(columns=['text_display'], inplace=True)
    # Rename
    df_replies.rename(columns={'etag': 'comment_etag', 
                   'tl_id': 'parent_id', 
                   'id': 'comment_id', 
                   'text_original': 'text'}
          , inplace=True)
    
    
#     Merging the Structured DataFrames
    df_final = pd.concat( (df, df_replies), ignore_index = True)
    
#     Some Text Adjustments for the Analysis
    df_final.text = df_final.text.str.lower()
    df_final.text.fillna('isnan', inplace=True)
#     df_final.dropna(subset=['text'], inplace=True)
     
#     df_final.text = df_final.text.str.replace('â€œ', '"')
#     df_final.text = df_final.text.str.replace('â€™', "'")
#     df_final.text = df_final.text.str.replace('â€‌ ', '"')
#     df_final.text = df_final.text.str.replace('â€‌', '"')
#     df_final.text = df_final.text.str.replace('â€ک', "")
#     df_final.text = df_final.text.str.replace('â€', '"')
#     df_final.text = df_final.text.str.replace("man'", "man")

#     df_final.text = df_final.text.str.replace('\n\n\n', ' ')
#     df_final.text = df_final.text.str.replace('\n\n', " ")
#     df_final.text = df_final.text.str.replace('\n', ' ')


#     df_final.text = df_final.text.str.replace('آ«آ ', '')
#     df_final.text = df_final.text.str.replace('آ«آ', '')
#     df_final.text = df_final.text.str.replace('آ آ»', '')
#     df_final.text = df_final.text.str.replace('آ آ» ', '')
#     df_final.text = df_final.text.str.replace('آ« ', '')
#     df_final.text = df_final.text.str.replace('آ«', '')
#     df_final.text = df_final.text.str.replace('آ» ', '')
#     df_final.text = df_final.text.str.replace('آ»', '')
#     df_final.text = df_final.text.str.replace('آ ', '')


#     df_final.text = df_final.text.str.replace("you're", 'you are')
#     df_final.text = df_final.text.str.replace("she's", 'she is')

#     df_final.text = df_final.text.str.replace('"', '')
#     df_final.text = df_final.text.str.replace('.', '')
#     df_final.text = df_final.text.str.replace(',', '')
#     df_final.text = df_final.text.str.replace('-', ' ')


#     df_final.text = df_final.text.str.replace('\t', ' ')
#     df_final.text = df_final.text.str.replace('   ', ' ')
#     df_final.text = df_final.text.str.replace('  ', ' ')


    
    
    
#     df['user_id'] = df['user_id'].astype('str')
#     df['tweet_id'] = df['tweet_id'].astype('str')

#     df["created_at"] = pd.to_datetime(df["created_at"], unit='ms')
#     df["user_created_at"] = pd.to_datetime(df["user_created_at"], unit='ms')
   
    
# # use format to remove the +00:00    
    df_final["p_dtime"] = pd.to_datetime(df_final["p_dtime"]) # , format="%Y-%m-%d %H:%M:%S+00:00"
    df_final.sort_values(by='p_dtime', inplace=True)                
                
# 2) Adding More Columns
# Adding year, month, dayofmonth and a diff columns
# https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python

    df_final["date"] = df_final["p_dtime"].dt.date
    df_final["year"] = df_final["p_dtime"].dt.year
    df_final["month"] = df_final["p_dtime"].dt.strftime("%b")
    df_final["dayofmonth"] = df_final["p_dtime"].dt.day
    df_final["hour"] = df_final["p_dtime"].dt.hour
    
    df_final["date"] = pd.to_datetime(df_final["date"])
    
    
# 3) Normalizing Text   


                   
# 4) Return the cleaned dataframe.
    return df_final

# -------------------------------------------------------------------------------------------------

def clean_youtube_videos(df):
    """   
    INPUT: YouTube Videos DataFrame
    OUTPUT: Cleaned YouTube Videos DataFrame
    """
    
    df.drop_duplicates(inplace=True)
    # drop snippet.thumbnails.default.width,snippet.thumbnails.default.height
    df.drop(columns=[],
            inplace=True)
    
    df.drop(
    columns=["snippet.thumbnails.default.width", "snippet.thumbnails.default.height", "kind", "contentDetails.dimension",
             "contentDetails.projection", "status.uploadStatus", "status.privacyStatus",
             "contentDetails.regionRestriction.allowed", "snippet.thumbnails.default.url", "snippet.thumbnails.medium.url",
             "snippet.thumbnails.medium.width", "snippet.thumbnails.medium.height", "snippet.thumbnails.high.url",
             "snippet.thumbnails.high.width", "snippet.thumbnails.high.height", "snippet.thumbnails.standard.url",
             "snippet.thumbnails.standard.width", "snippet.thumbnails.standard.height", "snippet.thumbnails.maxres.url",
             "snippet.thumbnails.maxres.width", "snippet.thumbnails.maxres.height", "snippet.liveBroadcastContent",
             "snippet.localized.title", "snippet.localized.description", "contentDetails.definition", "contentDetails.caption", 
             "status.license", "status.embeddable", "status.publicStatsViewable", "status.madeForKids", 
             "statistics.favoriteCount", "contentDetails.contentRating.ytRating", "contentDetails.regionRestriction.blocked",
    ], 
    inplace=True,
)
    

    # Rename
    df.rename(columns={"snippet.publishedAt": "p_dtime", 
                   "snippet.channelId": "ch_id", 
                   "snippet.title": "title", 
                   "snippet.description": "description", 
                   "snippet.channelTitle": "ch_title", 
                   "snippet.categoryId": "category", 
                   "snippet.defaultAudioLanguage": "audio_language", 
                   "contentDetails.licensedContent": "is_licensed", 
                   "statistics.viewCount": "n_views", 
                   "statistics.likeCount": "n_likes", 
                   "statistics.dislikeCount": "n_dislikes",
                   "statistics.commentCount": "n_comments", 
                   "snippet.defaultLanguage": "language"}
          , inplace=True)
    

    video_category = {
    2: "Autos & Vehicles",
    1: "Film & Animation",
    10: "Music",
    15: "Pets & Animals",
    17: "Sports",
    18: "Short Movies",
    19: "Travel & Events",
    20: "Gaming",
    21: "Videoblogging",
    22: "People & Blogs",
    23: "Comedy",
    24: "Entertainment",
    25: "News & Politics",
    26: "Howto & Style",
    27: "Education",
    28: "Science & Technology",
    29: "Nonprofits & Activism",
    30: "Movies",
    31: "Anime/Animation",
    32: "Action/Adventure",
    33: "Classics",
    34: "Comedy",
    35: "Documentary",
    36: "Drama",
    37: "Family",
    38: "Foreign",
    39: "Horror",
    40: "Sci-Fi/Fantasy",
    41: "Thriller",
    42: "Shorts",
    43: "Shows",
    44: "Trailers",
    }
    
    df["category"] = df["category"].apply(lambda x: video_category[x])
    
    
    # # use format to remove the +00:00    
    df["p_dtime"] = pd.to_datetime(df["p_dtime"]) # , format="%Y-%m-%d %H:%M:%S+00:00"
    df.sort_values(by='p_dtime', inplace=True)                
                
# 2) Adding More Columns
# Adding year, month, dayofmonth and a diff columns
# https://stackoverflow.com/questions/1345827/how-do-i-find-the-time-difference-between-two-datetime-objects-in-python

    df["date"] = df["p_dtime"].dt.date
    df["year"] = df["p_dtime"].dt.year
    df["month"] = df["p_dtime"].dt.strftime("%b")
    df["dayofmonth"] = df["p_dtime"].dt.day
    df["hour"] = df["p_dtime"].dt.hour
    
    df["date"] = pd.to_datetime(df["date"])
    
    return df    
    

# -------------------------------------------------------------------------------------------------





class SameText:
    def __init__(self, df, token):
        self.token_df = df[df.tokens == token]
        self.token = token

    def n_commnets_unique(self):
        print(
            f"This comment appeared in {self.token_df.message.value_counts().shape[0]} shape"
        )

    def get_df(self):
        return self.token_df

    def users(self):
        return self.token_df.username.value_counts()

    def dates(self):
        return self.token_df.date.value_counts()

    def head(self, n):
        return self.token_df.head(n)

    def shapes(self, n):
        return self.token_df.message.value_counts().head(n)

    def peak(self, n):
        bar_peaks(
            self.dates()
            .to_frame()
            .reset_index()
            .head(n)
            .rename(columns={"date": "n_tweets"})
            .rename(columns={"index": "date"}),
            f"Peak Dates for {self.token}",
        )

    def date_info(self):
        min = self.dates().index.min()
        max = self.dates().index.max()
        print(f"The commentes were made between {min} and  {max}")
        print(
            self.token_df.groupby("year")
            .count()["message"]
            .to_frame()
            .rename(columns={"message": "n_tweets"})
        )
        pie(
            self.token_df.groupby("year").count()["message"].to_frame().reset_index(),
            "Numner of tweets Per Year",
        )

        facet_heat(self.token_df, title='Numner of tweets Per Day')
        
        for year in self.token_df.year.unique():
            facet_days(self.token_df, str(int(year)))

    def users_dates(self, n):
        return (
            self.token_df.groupby(["username", "date"])
            .count()["message"]
            .sort_values(ascending=False)
            .head(n)
        )

    def df_timing(self):
        df = self.get_df()
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")
        df["diff"] = df.datetime.diff()
        return pd.concat([df, df["diff"].dt.components.iloc[:, 0:3]], axis=1)

    def get_groups(self, date):
        df = self.df_timing()
        return set(
            df[(df.days == 0) & (df.hours == 0) & (df.date.astype(str) == date)]
            .username.value_counts()
            .index
        )

    
    
     
    
# https://stackoverflow.com/questions/68335565/add-two-texts-to-each-bar-chart-in-plotly <br>
# **https://stackoverflow.com/questions/65861823/plotly-python-how-to-add-more-then-one-text-label-in-a-bar-chart**
# https://stackoverflow.com/questions/62803633/timestamp-object-has-no-attribute-dt      
    
# def barh(df, title, threshold=float("inf"), c=0):
#     """
#     A function to plot barh graph
#     Args:
#         - df--> DataFrame.
#         - title --> the graph title.
#         - threshold --> plot in red if excced the value.
#     """
#     clrs = ["red" if (y > threshold) else "#5296dd" for y in df[f"{df.columns[2]}"]]

#     fig = (
#         px.bar(
#             df,
#             y=f"{df.columns[1]}",
#             x=f"{df.columns[2]}",
#             text=[f"day:{row[1].day}, n:{row[3]}" for row in df.itertuples()],
#             height=500,
#             title=title,
#         )
#         .update_traces(marker_color=c if c != 0 else clrs)
#         .update_layout()
#     )

# #     fig.update_traces(texttemplate=[f"day:{row[1].day}, n:{row[3]}" for row in df.itertuples()], textposition='outside')
#     fig.update_yaxes(autorange="reversed")
#     fig.show("svg")
    
# title = 'Users with The Most "Aquaman Petition" Contributions on Each Date'
# barh(df.head(15), title, c='red') # , c=colors    
    
    
    
