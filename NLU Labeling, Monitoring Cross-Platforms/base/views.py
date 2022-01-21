from django.shortcuts import render
from base.settings import NLP_REQUEST_FILE_PATH, NLG_REQUEST_FILE_PATH
from base.settings import NLP_CLASSIFICATION_MAX_SECONDS
from base.settings import NLP_CLASSIFICATION_CHECK_GAP_SECONDS
from nlpengine.serializers import Nlutext
import os
import time
import json
import codecs

def saveNlutext(text, label):
    row = {}
    row['text'] = text
    row['label'] = label
    row['response_text'] = ''
    row['trained'] = 0
    row['trained_at'] = ""
    try:
        nlptext = Nlutext(data=row)
        if nlptext.is_valid():
            obj = nlptext.save()
            return True
    except Exception as e:
        print(e)
        return False
# analysis db label
def analyze_db_label(label):
    if 'support_AH' in label:
        return "Supporter"
    elif 'defense_AH' in label:
        return "Supporter"
    elif 'offense_AH' in label:
        return "Offender"
    elif 'defense_against_AH' in label:
        return "Offender"
    else:
        return "None"

# nlu_return_json2label
def nlu_return_json2db_label(labels_json):
    nlu_result = json.loads(labels_json.replace("'", '"'))
    max_label = 0
    return_label = 'null'
    if nlu_result['defense_AH'] > max_label and nlu_result['defense_AH'] >0.5:
        return_label = 'defense_AH : ' + str(round(nlu_result['defense_AH']*100)/100)
        max_label = nlu_result['defense_AH']
    if nlu_result['support_AH'] > max_label and nlu_result['support_AH'] >0.5:
        return_label = 'support_AH : ' + str(round(nlu_result['support_AH']*100)/100)
        max_label = nlu_result['support_AH']
    if nlu_result['offense_AH'] > max_label and nlu_result['offense_AH'] >0.5:
        return_label = 'offense_AH : ' + str(round(nlu_result['offense_AH']*100)/100)
        max_label = nlu_result['offense_AH']
    if nlu_result['defense_against_AH'] > max_label and nlu_result['defense_against_AH'] >0.5:
        return_label = 'defense_against_AH : ' + str(round(nlu_result['defense_against_AH']*100)/100)
        max_label = nlu_result['defense_against_AH']
    return return_label


def nlpclassify(text):
    file_name = str(round(time.time()*1000)%1000000)+".txt"
    try: 
        file = codecs.open(NLP_REQUEST_FILE_PATH + "input/" + file_name, "w","utf-8") 
        file.write(text)
        file.close()
    except Exception as e:
        print(e)
        return "{'defense_AH': 0, 'support_AH': 0, 'offense_AH': 0, 'defense_against_AH': 0}"
    counter_sec = NLP_CLASSIFICATION_MAX_SECONDS / NLP_CLASSIFICATION_CHECK_GAP_SECONDS
    return_label = "Server Error!"
    # file_name = "4748.txt"
    while counter_sec > 0:
        if os.path.exists(NLP_REQUEST_FILE_PATH + "output/" + file_name):
            file = open(NLP_REQUEST_FILE_PATH + "output/" + file_name, "r") 
            return_label = file.read()
            file.close()
            # nlu_result = json.loads(return_label.replace("'", '"'))
            if return_label == '':
                continue
            break
        time.sleep(NLP_CLASSIFICATION_CHECK_GAP_SECONDS)
        counter_sec -= 1
    # if return_label != "Server Error!":
    #     saveNlutext(text, return_label)
    return return_label

def nlgtextgeneration(text):
    file_name = str(round(time.time()*1000)%1000000)+".txt"
    try: 
        file = codecs.open(NLG_REQUEST_FILE_PATH + "input/" + file_name, "w","utf-8") 
        file.write(text)
        file.close()
    except Exception as e:
        print(e)
        return "{'defense_AH': 0, 'support_AH': 0, 'offense_AH': 0, 'defense_against_AH': 0}"
    counter_sec = NLP_CLASSIFICATION_MAX_SECONDS / NLP_CLASSIFICATION_CHECK_GAP_SECONDS * 5
    return_label = "Server Error!"
    # file_name = "4748.txt"
    while counter_sec > 0:
        if os.path.exists(NLG_REQUEST_FILE_PATH + "output/" + file_name):
            file = open(NLG_REQUEST_FILE_PATH + "output/" + file_name, "r") 
            return_label = file.read()
            file.close()
            # nlu_result = json.loads(return_label.replace("'", '"'))
            if return_label == '':
                continue
            break
        time.sleep(NLP_CLASSIFICATION_CHECK_GAP_SECONDS)
        counter_sec -= 1
    # if return_label != "Server Error!":
    #     saveNlutext(text, return_label)
    return return_label



