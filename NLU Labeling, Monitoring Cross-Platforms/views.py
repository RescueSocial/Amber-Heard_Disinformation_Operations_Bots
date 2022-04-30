from django.shortcuts import render
from rest_framework import generics
from .serializers import ActionSerializer
from monitor.serializers import TweeterSerializer
from .models import Action
from base.views import nlpclassify, nlu_return_json2db_label, analyze_db_label
from random import random
from datetime import datetime
from django.core.serializers import serialize
import json
from django.db import connection

class ActionsView(generics.ListCreateAPIView):
    serializer_class = ActionSerializer
    queryset = Action.objects.all()

def saveAction(action_json):
    try:
        actionSerializer = ActionSerializer(data=action_json)
        if actionSerializer.is_valid():
            obj = actionSerializer.save()
            return obj.id
        else:
            return 0
    except Exception as e:
        print(e)
        return -1
def update_tweeters_from_new_tweet(who, what_reputation, client):
    if who[0] != "@":
        return
    query = "SELECT * FROM monitor_tweeter WHERE handle='{}' AND client_id={}".format(who, client)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            if row is not None:
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
                cursor.execute(query)
            else:
                tweeter_serialization = {}
                tweeter_serialization['handle'] = who
                tweeter_serialization['client'] = client
                # tweeter_serialization['supports'] = 0
                # tweeter_serialization['offenses'] = 0
                # tweeter_serialization['unbiased'] = 0
                tweeter_serialization['total_tweets'] = 1
                tweeter_serialization['add_time'] = str(datetime.utcnow())
                if what_reputation == "Supporter":
                    tweeter_serialization['score'] = 1
                    tweeter_serialization['support'] = 1
                    tweeter_serialization['category'] = "Supporter"
                elif what_reputation == "Offender":
                    tweeter_serialization['score'] = 0
                    tweeter_serialization['offense'] = 1
                    tweeter_serialization['category'] = "Offender"
                else:
                    tweeter_serialization['score'] = 0.5
                    tweeter_serialization['unbiased'] = 1
                    tweeter_serialization['category'] = "None"
                tweeterSerializer = TweeterSerializer(data=tweeter_serialization)
                if tweeterSerializer.is_valid():
                    obj = tweeterSerializer.save()
                    return obj.id
                else:
                    return 0
        except Exception as e:
            print(e)


def getActionfromTweet(tweet_json):
    action_json = {}
    action_json['bot']=tweet_json['bot']
    action_json['commander_id']="BotManager"
    action_json['performed']=0
    action_json['bot_checked']=1
    action_json['site']="Twitter"
    action_json['method']="None"
    action_json['target_user']=tweet_json['who']
    action_json['target_content']=tweet_json['what']
    # action_json['estimation_label']="Compliment"
    nlu_json = nlpclassify(tweet_json['what'])
    action_json['estimation_label']=nlu_return_json2db_label(nlu_json)
    what_reputation = analyze_db_label(action_json['estimation_label'])
    print(what_reputation)

    update_tweeters_from_new_tweet(tweet_json['who'], what_reputation, 1)

    action_json['contents']=""
    action_json['url']=tweet_json['where']
    action_json['created_at']=str(datetime.utcnow())
    action_json['performed_at']=str(datetime.utcnow())
    action_json['site_response']=""

    if what_reputation == "Supporter":
        check_method = random()
        method_probability = [1, 0, 0] # [None, Retweet, Like]
        if check_method > method_probability[0] + method_probability[1]:#Like
            action_json['method']="Like"
        elif check_method > method_probability[0]:
            action_json['method']="Retweet"
        else:
            action_json['method']="None"
        if action_json['method']!="None":
            obj_id =saveAction(action_json)
            action_json['id']=obj_id
            if obj_id < 1:
                action_json['method']="None"
    elif what_reputation == "Offender":
        check_method = random()

    return action_json

def getAction(bot_id):
    return_json = []
    query = 'SELECT * FROM actions_action WHERE performed=0 AND bot_id=' + str(bot_id)
    models_json = json.loads(serialize('json', Action.objects.raw(query)))
    for one_model_json in models_json:
        return_json.append(one_model_json['fields'])
    return return_json

def getUrls(client_id):
    return_json = []
    query = "SELECT * FROM monitor_monitoringpage WHERE client_id=" + str(client_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    return {"test":rows}



