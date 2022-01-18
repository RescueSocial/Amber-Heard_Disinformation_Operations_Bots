from rest_framework import serializers
from .models import Tweet, Tweeter

class TweetSerializer(serializers.ModelSerializer):
    estimation_label = serializers.CharField(required=False)
    action = serializers.CharField(required=False)
    class Meta:
        model = Tweet
        fields = ('who', 'how', 'what', 'whom', 'when', 'where', 'replies',\
                'retweets', 'likes', 'bot', 'monitor_time', 'estimation_label',\
                'action')
class TweeterSerializer(serializers.ModelSerializer):
    # total_tweets = serializers.IntegerField(required=False)
    support = serializers.IntegerField(required=False)
    offense = serializers.IntegerField(required=False)
    unbiased = serializers.IntegerField(required=False)
    # score = serializers.FloatField(required=False)
    # category = serializers.CharField(required=False)
    class Meta:
        model = Tweeter
        fields = ('handle', 'client', 'total_tweets', 'support', 'offense', \
                'unbiased', 'score',\
                'category', 'add_time', )

