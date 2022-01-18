from django.db import models
from base.settings import TWEET_MAX_LENGTH, NLU_UPLOAD_FILE_PATH
from django.utils.html import format_html

class Nlutext(models.Model):
    text = models.CharField(max_length=TWEET_MAX_LENGTH, null=False)
    # label = models.CharField(max_length=15, null=False)
    defense_AH = models.FloatField(default=0)
    support_AH = models.FloatField(default=0)
    offense_AH = models.FloatField(default=0)
    defense_against_AH = models.FloatField(default=0)
    # response_text = models.CharField(max_length=1500, default='')
    trained = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now=True)
    trained_at = models.DateTimeField(null=True, blank=True)

class DataFile(models.Model):
    data = models.FileField(upload_to= NLU_UPLOAD_FILE_PATH, unique=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return self.data.url.split('/')[-1]
    # def save(self, *args, **kwargs):
    #     super(DataFile, self).save(*args, **kwargs)
    #     filename = self.data.url