import plotly.io as pio
from datetime import datetime
import pandas as pd
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import warnings
import re
import seaborn as sb
warnings.filterwarnings("ignore")
from ast import literal_eval as le


def neat_display(objects):
    """
    Prints the investigtions in a neat way.

            Parameters:
                objects (list): List of Objects to be displyed
    """
    for _, __ in objects:
        print(_)
        display(__,)
        print(
            "______________________________________________________________________________"
        )
        print()

def list_clean(list_or_none):
    """
    Returns None if the list is empty.

            Parameters:
                    l (list): A List

            Returns:
                    list or None
    """
    if len(list_or_none) == 0:
        list_or_none = None
    return list_or_none

def merge_lists(lists):
    """
   Merge Tow lists or more.

            Parameters:
                    lists (list): A List of lists to be merged

            Returns:
                    Merged List or None
    """
    non_empty_lists = [l for l in lists if l is not None]

    if len(non_empty_lists) == 0:
        return []

    non_empty_lists = [x for list_ in non_empty_lists for x in list_]

    return list(set(non_empty_lists))


def data_investigation(df):
    """
    Prints some investigtions of the Data Frame.

            Parameters:
                    df (DataFrame): The Data Frame to be investigated.
    """
    list_columns_has_one_value = []
    for c in df.columns:
        if df[[c]].value_counts().max() / df[[c]].shape[0] == 1:
            list_columns_has_one_value.append((c, df[[c]].values[0][0]))
    to_drop_one = list_clean(list_columns_has_one_value)
    if to_drop_one is not None:
        to_drop_one = pd.Series(
            [i[1] for i in list_columns_has_one_value],
            index=[i[0] for i in list_columns_has_one_value],
        )

    to_drop_null = list(df.columns[df.isnull().mean() == 1])
    to_drop_null = list_clean(to_drop_null)

    try:
        dtypes = pd.Series(
            [
                re.findall(r"<class '(.*)'>", str(type(i)))[0]
                for i in df.dropna(how="any").head(1).values[0]
            ],
            index=list(df.columns),
        )

    except:
        if to_drop_one is not None:
            if merge_lists([to_drop_null, list(to_drop_one.index)]) is not None:
                df_temp = df.drop(
                    columns=merge_lists([to_drop_null, list(to_drop_one.index)])
                )
        else:
            df_temp = df_temp = df.drop(columns=merge_lists([to_drop_null]))

        try:
            dtypes = pd.Series(
                [
                    re.findall(r"<class '(.*)'>", str(type(i)))[0]
                    for i in df_temp.dropna(how="any").head(1).values[0]
                ],
                index=list(df.columns),
            )
        except:

            types = []
            for col in df_temp.columns:
                types.append(
                    re.findall(
                        r"<class '(.*)'>",
                        str(type(df_temp[[col]].dropna().head(1).values[0][0])),
                    )[0]
                )
            dtypes = pd.Series(types, index=list(df_temp.columns))

    neat_display(
        [
            ("Data Head", df.head(2)),
            (
                "Data Shape",
                f"The data has {df.shape[0]} rows and {df.shape[1]} columns",
            ),
            ("Columns", list(df.columns)),
            ("Columns Must be Dropped (ALL NULLS)", to_drop_null,),
            ("Columns Must be Dropped (HAS ONLY ONE UNIQUE VALUE)", to_drop_one,),
            ("Column Data Type", dtypes),
            (
                "Number of Nulls in Each Column",
                df.isnull().sum().sort_values(ascending=False),
            ),
            (
                "Percentge of Nulls in Each Column",
                df.isnull().mean().sort_values(ascending=False),
            ),
            ("Numeric Columns' Staticts", df.describe()),
        ]
    )


def get_columns_to_drop(df):
    """
    Return List of Columns to be dropped.

            Parameters:
                    df (DataFrame): The Data Frame to get the columns to drop from it.
            Returns:
                    List of columns to be dropped.
    """
    list_columns_has_one_value = []
    for c in df.columns:
        if df[[c]].value_counts().max() / df[[c]].shape[0] == 1:
            list_columns_has_one_value.append((c, df[[c]].values[0][0]))
    to_drop_one = list_clean(list_columns_has_one_value)
    if to_drop_one is not None:
        to_drop_one = pd.Series(
            [i[1] for i in list_columns_has_one_value],
            index=[i[0] for i in list_columns_has_one_value],
        )

    to_drop_null = list(df.columns[df.isnull().mean() == 1])
    to_drop_null = list_clean(to_drop_null)
    return merge_lists([to_drop_null, list(to_drop_one.index)])

def isnull(df):
    for col in df.columns:
        print(f"The number of NaNs in {col}:", df[col].isnull().sum())

def handler(x, default, *types):
    """
    A function to use Try Except in Lambda expressions
    While converting timestmaps into datetime (to solve nan occurence)
    Args:
        - x--> TimeStamp value.
        - default --> return value in case of NaN.
        - *types --> data types
    Return:
        - datetime or Null.
    """
    for t in types:
        try:
            return datetime.fromtimestamp(x)
        except (ValueError, TypeError):
            continue
    return default

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

def pie(df, title):
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
        color_discrete_sequence=colors,
        title=title,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label+value",
        textfont=dict(size=12, color="white"),
    )
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
    fig = px.bar(df, x=f"{x}", y=f"{y}", text=f"{y}")

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

def bar_peaks(df_head, title):
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
            title="Comments Creation Date", tickmode="array", tickvals=df_head.date
        )
    )

    fig.update_traces(marker_color="red", opacity=1, textposition="auto")
    fig.update_xaxes(tickangle=45)
    fig.show("svg")

def draw_heatmap(*args, **kwargs):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    data = kwargs.pop('data')
    d = data.pivot(index=args[1], columns=args[0], values=args[2])
    d = d.reindex(index=months[::-1])
    sb.heatmap(d, **kwargs)
    
def facet_heat(df, title='title', n_col=2, vmax=100):
    daily_counts = df.groupby(['year', 'dayofmonth', 'month']).size().reset_index(name='count')
    
    g = sb.FacetGrid(daily_counts, col='year', col_wrap=n_col, height=4.5)
    g.map_dataframe(draw_heatmap, 'dayofmonth', 'month', 'count', cmap='rocket_r', vmin=0, vmax=vmax);

    plt.suptitle(title, y=1.06, fontsize=18)
    g.fig.subplots_adjust(wspace=0.15, hspace=0.2)
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True, labelleft=True)
        
def facet_days(df, year_str):
    """
    A function to plot bar graph for all months
    Args:
        - df -->  dataframe.
    """
    months_ordered = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    days_ordered = list(range(1, 32, 2))

    g = sb.FacetGrid(data=df, col="month", col_wrap=4, col_order=months_ordered)
    g.map(sb.countplot, "dayofmonth", order=days_ordered, palette=["#5296dd"])
    g.set_xticklabels(rotation=90)
    g.set_titles("{col_name}", size=14, y=-0.28)
    g.fig.suptitle("Comments Created in Each Day of " + year_str, fontsize=18, y=1.05)

    g.fig.subplots_adjust(wspace=0.1, hspace=0.3)
    g.set_xlabels("")
    for axis in g.axes.flat:
        axis.tick_params(labelbottom=True)

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

class SameText:
    def __init__(self, df, token, add_more):
        if add_more:
            self.token_df = df[
                df.text_tokens.isin(
                    [
                        set(le(str(i)))
                        for i in values[
                            values.tokens.apply(
                                lambda x: len(set(le(str(token))) - x) == 0
                            )
                        ].tokens.values
                    ]
                )
            ]
        else:
            self.token_df = df[df.text_tokens == set(le(str(token)))]
        self.token = str(token)

    def n_commnets_unique(self):
        print(
            f"This comment appeared in {self.token_df.clean_text.value_counts().shape[0]} shape"
        )

    def get_df(self):
        return self.token_df

    def get_stats(self):
        users = self.token_df.user_name.nunique()
        print(
            f"This text appeared {self.token_df.shape[0]} in {self.token_df.clean_text.value_counts().shape[0]} shape from {users} users "
        )

    def users(self):
        return self.token_df.user_name.value_counts()

    def dates(self):
        return self.token_df.date.value_counts()

    def head(self, n):
        return self.token_df.head(n)

    def shapes(self, n):
        return self.token_df.clean_text.value_counts().head(n)

    def peak(self, n):
        bar_peaks(
            self.dates()
            .to_frame()
            .reset_index()
            .head(n)
            .rename(columns={"date": "n_comments"})
            .rename(columns={"index": "date"}),
            f"Peak Dates for {self.token}",
        )

    def date_info(self):
        min = self.dates().index.min()
        max = self.dates().index.max()
        print(f"The commentes were made between {min} and  {max}")
        print(
            self.token_df.groupby(self.token_df.created_at.dt.year)
            .count()["clean_text"]
            .to_frame()
            .rename(columns={"clean_text": "n_tweets"})
        )
        pie(
            self.token_df.groupby(self.token_df.created_at.dt.year)
            .count()["clean_text"]
            .to_frame()
            .reset_index(),
            "Numner of Comments Per Year",
        )

        facet_heat(self.token_df, title="Number of tweets Per Day")

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
        df = df.sort_values("created_at")
        df["diff"] = df.created_at.diff()
        return pd.concat([df, df["diff"].dt.components.iloc[:, 0:3]], axis=1)

    def get_groups(self, date):
        df = self.df_timing()
        return set(
            df[(df.days == 0) & (df.hours == 0) & (df.date.astype(str) == date)]
            .username.value_counts()
            .index
        )

    def get_metrics(self):
        df_with_merics = pd.merge(self.token_df, df_metrics_2022, how="left")
        metrics_dict = {
            "retweet_count": df_with_merics["retweet_count"].sum(),
            "reply_count": df_with_merics["reply_count"].sum(),
            "like_count": df_with_merics["like_count"].sum(),
            "quote_count": df_with_merics["quote_count"].sum(),
        }
        display(pd.Series(metrics_dict.values(), index=metrics_dict.keys(),))

    def get_times(self):
        df = self.df_timing().query(" days == 0  and  hours == 0  and minutes == 0")
        print(
            f"{df.shape[0]} tweets from {self.token_df.shape[0]} tweets made in less than 1 min from previous tweet by {df.user_name.nunique()} users"
        )