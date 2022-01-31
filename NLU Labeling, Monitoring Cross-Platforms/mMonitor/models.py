from django.db import models
from base.settings import TWEET_MAX_LENGTH, \
                        TWEET_TYPE, \
                        SOCIAL_SITES, \
                        MONITORING_TYPE_TWITTER,\
                        TWEETER_CATEGORY
from base.models import Bot

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=30)
    site = models.CharField(max_length=10, choices=SOCIAL_SITES, default='Twitter')

    def __str__(self):
        return f"{self.name}"

class MonitoringPage(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=10, choices=MONITORING_TYPE_TWITTER, default='Hashtag')
    text = models.CharField(max_length=200, blank=True)

class Tweet(models.Model):
    who = models.CharField(max_length=100)
    how = models.CharField(max_length=10, choices=TWEET_TYPE, default='Tweet')
    what = models.CharField(max_length=TWEET_MAX_LENGTH)
    whom = models.CharField(max_length=TWEET_MAX_LENGTH, blank=True)
    when = models.DateTimeField(null=True, blank=True)
    where = models.URLField(max_length=200)
    replies = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    bot = models.ForeignKey(Bot,on_delete=models.CASCADE, default=1)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)
    monitor_time= models.DateTimeField(null=True, blank=True)
    estimation_label = models.CharField(max_length=120, null=True, blank=True)
    action = models.CharField(max_length=15, null=True, blank=True)
    list_filter = ("year", )
    # class Meta:
    #     unique_together = ("who", "what", )

class Tweeter(models.Model):
    handle = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=1)
    total_tweets = models.IntegerField(default=0)
    support = models.IntegerField(default=0)
    offense = models.IntegerField(default=0)
    unbiased = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    category = models.CharField(max_length=10, choices=TWEETER_CATEGORY, default='None')
    add_time= models.DateTimeField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Users"
