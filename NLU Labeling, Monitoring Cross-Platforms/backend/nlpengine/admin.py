from django.contrib import admin
from .models import Nlutext, DataFile
from base.admin import BaseModelAdmin
from django.conf import settings
from django.conf.urls.static import static
from base.settings import NLU_UPLOAD_FILE_PATH, NLU_TEXT_FIELD_LIST, NLU_TRAIN_FILE_PATH
from .views import save_nlu_text
from .forms import DataFileForm, NlutextForm
import csv
from django.db import connection
from io import TextIOWrapper
from asgiref.sync import sync_to_async
from django.http import HttpResponse, Http404
from django.conf.urls import url 
from django.utils.html import format_html
from django.urls import reverse

from django.db.models.signals import post_save
from django.dispatch import receiver

from celery.decorators import task

import asyncio

@admin.register(Nlutext)
class NlutextAdmin(BaseModelAdmin):
    form = NlutextForm
    list_display = ('text', 'defense_AH', 'support_AH', 'offense_AH'
                    , 'defense_against_AH','trained', 'created_at', 'trained_at')
    list_display_links = ('text',)
    date_hierarchy = 'created_at'
    # ordering = ['label']
    readonly_fields = ('trained', 'created_at', 'trained_at')
    list_per_page = 20
    search_fields = ('text', )

@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):  
    form = DataFileForm
    readonly_fields = ('download_link','uploaded_at', )
    date_hierarchy = 'uploaded_at'
    search_fields = ('data', )
    list_per_page = 20
    list_display_links = ('id',)
    list_display = ['id', 'data', 'uploaded_at', 'download_link']
    # list_display = ['id', 'data']
    actions = ['download_csv']
    # add custom view to urls
    def get_urls(self):
        urls = super(DataFileAdmin, self).get_urls()
        urls += [
            url(r'^download-file/(?P<filename>[\/\w\-]+\.csv)$', self.download_file, 
                name='applabel_modelname_download-file'),
        ]
        return urls

    # custom "field" that returns a link to the custom function
    def download_link(self, obj):
        return format_html(
            '<a href="{}">Download file</a>',
            # reverse('admin:applabel_modelname_download-file', args=['upload/nlu/files/up_load.csv'])
            reverse('admin:applabel_modelname_download-file', args=[obj.data.url.split('/')[-1]])
        )
    download_link.short_description = "File Link"

    # add custom view function that downloads the file
    def download_file(self, request, filename):
        try:
            url = "upload/"+ NLU_UPLOAD_FILE_PATH + "/" + filename
            with open(url, 'r', encoding="cp1251", errors='ignore') as f:
                response = HttpResponse(f, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename='+filename
                return response
        except Exception as e:
            print(e)
            raise Http404

    def download_csv(self, request, queryset):
        train_nlu_engine()
        try:
            f = open(NLU_TRAIN_FILE_PATH + 'all_data.csv', 'r', encoding="cp1251", errors='ignore')
            response = HttpResponse(f, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=all_data.csv'
            return response
        except Exception as e:
            print(e)
            raise Http404
        download_csv.short_description = "Download Total CSV file."
    def save_model(self, request, obj, form, change):
        user = request.user 
        instance = form.save(commit=False)
        if not change:    # new object
            instance.status = "...."
        else:             # updated old object
            instance.status = "..."
        instance.save()
        form.save_m2m()
        file_name = settings.MEDIA_ROOT + NLU_UPLOAD_FILE_PATH + "/" + request.FILES['data'].name.replace(' ','_')
        # read_csvfile.delay(file_name)
        self.read_csvfile(file_name)
        return instance
    def read_csvfile(self, file_name):
        try:
            with open(file_name, encoding="cp1251", errors='ignore') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                   print('Saved row id : ', save_nlu_text(row))
        except Exception as e:
            print(e)

@task(name="read csv file")
def read_csvfile(file_name):
    try:
        with open(file_name, encoding="utf-8", errors='ignore') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                save_nlu_text(row)
    except Exception as e:
        print(e)

# @task(name="making all trained nlu_file")
def train_nlu_engine():
    query = 'SELECT id, text, defense_AH, support_AH, offense_AH, defense_against_AH FROM nlpengine_nlutext'
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        with open( NLU_TRAIN_FILE_PATH + 'all_data.csv', 'w', encoding="cp1251", errors='ignore') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "comment_text", "defense_AH", "support_AH", "offense_AH", "defense_against_AH"])
            for row in rows:
                writer.writerow([str(row[0]), row[1], str(row[2]), str(row[3]), str(row[4]), str(row[5])])

# @receiver(post_save, sender=DataFile)
# def my_handler(sender, **kwargs):
#     print('post save callback')
