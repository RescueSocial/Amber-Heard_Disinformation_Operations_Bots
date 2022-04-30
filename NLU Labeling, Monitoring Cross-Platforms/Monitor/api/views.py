from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.parsers import JSONParser 
from django.http import JsonResponse
from base.views import nlpclassify, nlgtextgeneration
from actions.views import getActionfromTweet, getAction, getUrls
from monitor.views import getClientName, postAnalysisForTweet, getDashboard
from django.db import connection
import json

# from monitor.models import Tweet
from monitor.serializers import TweetSerializer

def nlptext(request):
    if request.method == "POST":
        request_json = JSONParser().parse(request)
        if request_json != None and 'text' in request_json:
            return HttpResponse(nlpclassify(request_json['text']))
        return HttpResponse("send text request into json type again.")

def nlutext(request):
    if request.method == "POST":
        request_json = JSONParser().parse(request)
        if request_json != None and 'text' in request_json:
            return HttpResponse(nlpclassify(request_json['text']))
        return HttpResponse("send text request into json type again.")

def nlgtext(request):
    if request.method == "POST":
        request_json = JSONParser().parse(request)
        if request_json != None and 'text' in request_json:
            return HttpResponse(nlgtextgeneration(request_json['text']))
        return HttpResponse("send text request into json type again.")


def action(request):
    if request.method == "GET":
        request_json = JSONParser().parse(request)
        if request_json != None and 'bot_id' in request_json:
            return JsonResponse(getUrls(request_json['bot_id']), safe=False)
        return JsonResponse(response_json, safe=False)
    elif request.method == "POST":
        request_json = JSONParser().parse(request)
        if request_json != None and 'bot_id' in request_json:
            return JsonResponse(postAnalysisForTweet(request_json['bot_id']), safe=False)
        return JsonResponse(response_json, safe=False)

def tweets(request):
    if request.method == "POST":
        response_json = {}
        response_json['estimation'] = 'None'
        response_json['method'] = 'None'
        response_json['id'] = 0
        try:
            request_json = JSONParser().parse(request)
            # new_tweet = Tweet(request_json)
            with connection.cursor() as cursor:
                query = 'SELECT * FROM monitor_tweet WHERE what="{}"'.format(request_json['what'])
                cursor.execute(query)
                row_db = cursor.fetchone()
                if row_db is None and len(request_json['what'].split()) > 1:
                    print(len(request_json['what'].split()))
                    print(request_json['what'])
                    response_json = getActionfromTweet(request_json)
                    request_json['estimation_label'] = response_json['estimation_label']
                    request_json['action'] = response_json['method']
                    tweetserializer = TweetSerializer(data=request_json)
                    if tweetserializer.is_valid():
                        obj = tweetserializer.save()
                        print(obj.id)
                    else:
                        response_json['status'] = 'error'
                else:
                    response_json['status'] = 'already'
        except Exception as e:
            print(e)
            response_json['status'] = 'error'
        return JsonResponse(response_json, safe=False)
def handle_uploaded_file(f):
    with open('files/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def fileupload(request):
    if request.method == "POST":
        response_json = {}
        response_json['estimation'] = 'None'
        response_json['method'] = 'None'
        response_json['id'] = 0

        handle_uploaded_file(request.FILES['file'])

        try:
            request_json = JSONParser().parse(request)
            # new_tweet = Tweet(request_json)
            if len(request_json['what'].split()) > 3:
                print(len(request_json['what'].split()))
                print(request_json['what'])
                tweetserializer = TweetSerializer(data=request_json)
                if tweetserializer.is_valid():
                    obj = tweetserializer.save()
                    response_json = getActionfromTweet(request_json)
                    print(obj.id)
                else:
                    response_json['status'] = 'error'
        except Exception as e:
            print(e)
            response_json['status'] = 'error'
        return JsonResponse(response_json, safe=False)
def dashboard(request):
    if request.method == "GET":
        client_id = 1
        return JsonResponse(getDashboard(client_id=client_id), safe=False)
        # request_json = JSONParser().parse(request)
        # if request_json != None and 'client_id' in request_json:
        #     return JsonResponse(getDashboard(client_id=request_json['client_id']), safe=False)
        # return JsonResponse(response_json, safe=False)
    elif request.method == "POST":
        request_json = JSONParser().parse(request)
        if request_json != None and 'bot_id' in request_json:
            return JsonResponse(postAnalysisForTweet(request_json['bot_id']), safe=False)
        return JsonResponse(response_json, safe=False)