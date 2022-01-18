from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from .serializers import NlutextSerializer
from .models import Nlutext
from datetime import datetime
from base.settings import NLU_TEXT_FIELD_LIST, NLU_TRAIN_FILE_PATH
import csv
from django.db import connection


# import asyncio
from time import sleep
# import httpx

# from celery.decorators import task

class NlutextView(generics.ListCreateAPIView):
    serializer_class = NlutextSerializer
    queryset = Nlutext.objects.all()

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


# @task(name="save nlu text row")
def save_nlu_text(row):
    try:
        fieldnames = [*row]
        nlu_text_field = fieldnames[NLU_TEXT_FIELD_LIST[-1]]
        for fieldname in fieldnames:
            if fieldname in NLU_TEXT_FIELD_LIST[:-1]:
                nlu_text_field = fieldname
                break
        if len(row[nlu_text_field]) > 2:
            text_json = {'defense_AH':0, 'support_AH':0, 'offense_AH':0, 'defense_against_AH':0}
            
            with connection.cursor() as cursor:
                # query = "SELECT * FROM nlpengine_nlutext WHERE text=%s"
                # cursor.execute(query,(row[nlu_text_field]))
                # repr
                query = "SELECT * FROM nlpengine_nlutext WHERE text='{}'".format(row[nlu_text_field].replace("'", "\\'"))
                cursor.execute(query)
                row_db = cursor.fetchone()
                text_json['text'] = row[nlu_text_field]
                if 'defense_AH' in fieldnames:
                    try:
                        text_json['defense_AH'] = float(row['defense_AH'])
                    except:
                        print('Insert error')
                if 'support_AH' in fieldnames:
                    try:
                        text_json['support_AH'] = float(row['support_AH'])
                    except:
                        print('Insert error')
                if 'offense_AH' in fieldnames:
                    try:
                        text_json['offense_AH'] = float(row['offense_AH'])
                    except:
                        print('Insert error')
                if 'defense_against_AH' in fieldnames:
                    try:
                        text_json['defense_against_AH'] = float(row['defense_against_AH'])
                    except:
                        print('Insert error')
                text_json['created_at'] = str(datetime.utcnow())

                if row_db is not None:
                    if not (row_db[5] ==text_json['defense_AH'] and \
                            row_db[8] ==text_json['support_AH'] and \
                            row_db[7] ==text_json['offense_AH'] and \
                            row_db[6] ==text_json['defense_against_AH']):
                        sql = "UPDATE nlpengine_nlutext SET defense_AH={}, support_AH={}, offense_AH={}, defense_against_AH={}, created_at='{}' WHERE id={}"\
                            .format(str(text_json['defense_AH']), str(text_json['support_AH']), str(text_json['offense_AH']), str(text_json['defense_against_AH']), text_json['created_at'], str(row_db[0]))
                        cursor.execute(sql)
                        print('update one nlutext: ', text_json)
                        return row_db[0]
                    else:
                        return row_db[0]
                else:
                    nlutextSerializer = NlutextSerializer(data=text_json)
                    print('add one nlutext: ', text_json)
                    if nlutextSerializer.is_valid():
                        obj = nlutextSerializer.save()
                        return obj.id
                    else:
                        print('serializer validation error.')
                        print(nlutextSerializer.errors)
                        return 0
    except Exception as e:
        print(e)
        return -1