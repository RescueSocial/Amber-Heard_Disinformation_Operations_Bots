from django.shortcuts import render
from django.core.serializers import serialize
import json
from .models import Client, Tweeter
from django.db import connection
from base.views import nlpclassify, analyze_db_label
from datetime import datetime, timedelta

def getClientName(client_id):
    return_json = []
    query = "SELECT * FROM monitor_client WHERE id=" + str(client_id)
    models_json = json.loads(serialize('json', Client.objects.raw(query)))
    for one_model_json in models_json:
        return_json.append(one_model_json['fields'])
    return return_json

def analysis_tweeters():
    return True

def change_labels_json2class(labels_json):
    nlu_result = json.loads(labels_json.replace("'", '"'))
    max_label = 0
    return_label = 'None'
    if nlu_result['defense_AH'] > max_label and nlu_result['defense_AH'] >0.5:
        return_label = 'Supporter'
        max_label = nlu_result['defense_AH']
    if nlu_result['support_AH'] > max_label and nlu_result['support_AH'] >0.5:
        return_label = 'Supporter'
        max_label = nlu_result['support_AH']
    if nlu_result['offense_AH'] > max_label and nlu_result['offense_AH'] >0.5:
        return_label = 'Offender'
        max_label = nlu_result['offense_AH']
    if nlu_result['defense_against_AH'] > max_label and nlu_result['defense_against_AH'] >0.5:
        return_label = 'Offender'
        max_label = nlu_result['defense_against_AH']
    return return_label

def postAnalysisForTweet(client_id):
    return_json = []
    query = 'SELECT who, what, estimation_label FROM monitor_tweet WHERE who like "@%" AND not what like "#%" AND client_id=' + str(client_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    who_list = []
    for who_what in rows:
        try:
            try:
                # what_reputation = change_labels_json2class(nlpclassify(who_what[1]))
                what_reputation = analyze_db_label(who_what[2])
                print(what_reputation)
            except Exception as e:
                print(who_what[1], e)
                what_reputation = "None"
            if who_what[0] in who_list:
                query = "SELECT * FROM monitor_tweeter WHERE handle='{}'".format(who_what[0])
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    row = cursor.fetchone()
                supports = row[2]
                offenses = row[3]
                total_tweets = row[8]
                unbiased = row[9]
                if what_reputation == "Supporter":
                    supports += 1
                elif what_reputation == "Offender":
                    offenses += 1
                else:
                    unbiased += 1
                total_tweets += 1
                if (supports + offenses) == 0:
                    score = 0.5
                else:
                    score = supports/(supports + offenses)

                if score > 0.6:
                    category = "Supporter"
                elif score < 0.4:
                    category = "Offender"
                else:
                    category = "None"
                query = "UPDATE monitor_tweeter SET support='{}', offense='{}', \
                    score={},category='{}', total_tweets={}, unbiased={} WHERE id={}".format(\
                    supports, offenses, score, category, total_tweets, unbiased, row[0])
                with connection.cursor() as cursor:
                    cursor.execute(query)

            else:
                id = len(who_list) + 1
                handle = who_what[0]
                supports = 0
                offenses = 0
                unbiased = 0
                total_tweets = 1
                if what_reputation == "Supporter":
                    score = 1
                    supports = 1
                    category = "Supporter"
                elif what_reputation == "Offender":
                    score = 0
                    offenses = 1
                    category = "Offender"
                else:
                    score = 0.5
                    unbiased = 1
                    category = "None"

                query = "INSERT INTO monitor_tweeter \
                        VALUES ({}, '{}', {}, {}, {}, '{}', {},'{}',{},{})".format(\
                            id, handle, supports, offenses, score, category, client_id, \
                            str(datetime.utcnow()), total_tweets, unbiased)
                who_list.append(who_what[0])  
                with connection.cursor() as cursor:          
                    cursor.execute(query)   
        except Exception as e:
            print(e)
    return rows
def query_db(query, args=(), one=False):
    with connection.cursor() as cur:
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return (r[0] if r else None) if one else r

def get_start_date_ago(type, ago_counts):
    if type=="Day":
        return str(datetime.utcnow().date() - timedelta(ago_counts))
def get_end_date_ago(type, ago_counts):
    if type=="Day":
        return str(datetime.utcnow().date() - timedelta(ago_counts-1))
def get_query_category_tweets(category, type, counts):
    return_query = "SELECT "
    for i in range(counts):
        if i != 0:
            return_query += ", \n"
        convert_i = counts - i - 1 
        return_query += 'COUNT(CASE WHEN `when` BETWEEN "' + get_start_date_ago(type, convert_i)
        return_query += '" AND "' + get_end_date_ago(type, convert_i) + '" THEN 1 END) AS "'
        return_query += type+str(convert_i) +'"'
    return_query += " \nFROM monitor_tweet WHERE "
    if category == "Support":
        return_query += 'estimation_label LIKE "support_AH %" OR estimation_label LIKE "defense_AH %"'
    elif category == "Offense":
        return_query += 'estimation_label LIKE "offense_AH %" OR estimation_label LIKE "defense_against_AH %"'
    elif category == "Biased":
        return_query += 'estimation_label = "null"'
    return return_query

def get_labels(type="Day", counts=30):
    return_labels = []
    for i in range(counts):
        convert_i = counts - i - 1 
        return_labels.append(get_start_date_ago(type, convert_i))
    return return_labels


def get_query_for_tweets(type="Day", counts=30):
    return_query = ""
    return_query = get_query_category_tweets("Support", type, counts) + "\n UNION \n"
    return_query += get_query_category_tweets("Offense", type, counts) + "\n UNION \n"
    return_query += get_query_category_tweets("Biased", type, counts)
    return return_query

def getDashboard(client_id = 1, site = "twitter"):
    return_json = {}
    query = 'SELECT COUNT(*) AS "All", COUNT(CASE WHEN category="Supporter" THEN 1 END) AS "Suppporter"\
            , COUNT(CASE WHEN category="Offender" THEN 1 END) AS "Offender"\
            , COUNT(CASE WHEN category="None" THEN 1 END) AS "None"\
            FROM twitterbotdev.monitor_tweeter where client_id=1;'
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        return_json['users'] = row
    print(return_json)

    query = 'SELECT COUNT(*) AS "Total_Tweets",\
        COUNT(CASE WHEN estimation_label LIKE "support_AH %" OR estimation_label LIKE "defense_AH %" THEN 1 END) AS "support_AH ",\
        COUNT(CASE WHEN estimation_label LIKE "offense_AH %" OR estimation_label LIKE "defense_against_AH %" THEN 1 END) AS "offense_AH"\
        FROM twitterbotdev.monitor_tweet'
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()
        return_json['total_tweets'] = row
    print(return_json)

    query = get_query_for_tweets(type="Day", counts=30)
    labels = get_labels(type="Day", counts=30)
    tweets_result = {}
    tweets_result['labels'] = labels
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        tweets_result['datas'] = rows
    return_json['tweets'] = tweets_result
    print(return_json)
    return return_json