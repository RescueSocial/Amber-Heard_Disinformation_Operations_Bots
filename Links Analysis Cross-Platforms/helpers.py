
import pandas as pd
from datetime import datetime
import numpy as np
import re
from collections import Counter


class URLS:
    def __init__(self, df):
        self.df = df

    def datetime_from_timestamp(self, timestamp_column):
        """
        converts time stamp to ddatetime object
        """
        return self.df[timestamp_column].apply(
            lambda x: x if np.isnan(x) else datetime.fromtimestamp(x)
        )

    def months_filteration(self, datetime_column, start, end):
        """
        Filter dataframe due to time, get data between two dates
        """
        return (
            self.df[
                (self.df[datetime_column].astype(str) >= start)
                & (self.df[datetime_column].astype(str) < end)
            ]
            .reset_index()
            .drop(columns="index")
        )


def get_urls(string):
    """
    Get links from text
    """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    urls = [x[0] for x in url]
    return urls


def urls_df(filtered_df, column="n_urls"):
    return filtered_df[filtered_df[column] > 0].reset_index().drop(columns="index")


def one_link_df(df, n_urls_column="n_urls", url_column="url", urls="urls"):
    one_link_df = df[df[n_urls_column] == 1]
    one_link_df[url_column] = one_link_df[urls].apply(lambda x: x[0])
    one_link_df = one_link_df.reset_index().drop(columns="index")
    return one_link_df.reset_index().drop(columns="index")


def one_link_urls(one_link_df, column="urls"):
    return one_link_df[column].values


def one_link_urls_with_count(one_link_df, user_column, url_column="url"):
    users = []
    for url in one_link_df[url_column].values:
        n = one_link_df[one_link_df.url == url][user_column].nunique()
        if n != 0:
            users.append(n)

    one_link_df["n_users"] = users

    temp_urls = []
    for i in one_link_df[["url", "n_users"]].values:
        temp_urls.append((i[0], i[1]))
    data_last = dict(Counter(temp_urls))
    links_last = []
    users_last = []
    count_last = []
    for url_users, count in data_last.items():
        links_last.append(url_users[0])
        count_last.append(count)
        users_last.append(url_users[1])

    return (
        pd.DataFrame({"link": links_last, "count": count_last, "n_users": users_last})
        .sort_values("n_users", ascending=False)
        .reset_index()
        .drop(columns="index")
    )


def df_more_than_link(df):
    return df[df.n_urls > 1].reset_index().drop(columns="index")


def more_than_one_link_with_count(df, column_user, column_urls):
    user_link_m = []
    for user_links in df[[column_user, column_urls,]].values:
        for link in user_links[1]:
            user_link_m.append((user_links[0], link))
    temp = pd.DataFrame(
        {"link": [i[1] for i in user_link_m], "user": [i[0] for i in user_link_m]}
    )
    links = temp["link"].unique()
    last_links = []
    last_u = []
    last_c = []
    for link in links:
        last_c.append(temp[temp["link"] == link].shape[0])
        last_u.append(temp[temp["link"] == link]["user"].nunique())
        last_links.append(link)

    return pd.DataFrame({"link": last_links, "count": last_c, "n_users": last_u})


def one_link_urls_with_count_(one_link_df, user_column, url_column="url"):
    users = []
    u = []
    for url in one_link_df[url_column].values:
        nn = tuple(set(one_link_df[one_link_df.url == url][user_column]))
        n = one_link_df[one_link_df.url == url][user_column].nunique()
        if n != 0:
            users.append(n)
            u.append(nn)

    one_link_df["n_users"] = users
    one_link_df["users"] = u
    temp_urls = []
    for i in one_link_df[["url", "n_users", "users"]].values:
        temp_urls.append((i[0], i[1], i[2]))
    data_last = dict(Counter(temp_urls))
    links_last = []
    nusers_last = []
    count_last = []
    users_last = []
    for url_users, count in data_last.items():
        links_last.append(url_users[0])
        count_last.append(count)
        nusers_last.append(url_users[1])
        users_last.append(url_users[2])

    return (
        pd.DataFrame({"link": links_last, "count": count_last, "n_users": nusers_last, "users": users_last})
        .sort_values("n_users", ascending=False)
        .reset_index()
        .drop(columns="index")
    )

def more_than_one_link_with_count_(df, column_user, column_urls):
    user_link_m = []
    n_urls = []
    for user_links in df[[column_user, column_urls]].values:

        for link in user_links[1]:
            user_link_m.append((user_links[0], link, len(user_links[1])))
    temp = pd.DataFrame(
        {
            "link": [i[1] for i in user_link_m],
            "user": [i[0] for i in user_link_m],
            "n_urls": [i[2] for i in user_link_m],
        }
    )
    links = temp["link"].unique()
    last_links = []
    last_u = []
    last_c = []
    last_n = []
    last_nu = []
    for link in links:
        last_c.append(temp[temp["link"] == link].shape[0])
        last_u.append(temp[temp["link"] == link]["user"].nunique())
        last_nu.append(set((temp[temp["link"] == link]["user"].unique())))
        last_n.append(set(temp[temp["link"] == link]["n_urls"].values))
        last_links.append(link)

    return pd.DataFrame(
        {
            "link": last_links,
            "count": last_c,
            "n_users": last_u,
            "users": last_nu,
            "n_urls": last_n,
        }
    )