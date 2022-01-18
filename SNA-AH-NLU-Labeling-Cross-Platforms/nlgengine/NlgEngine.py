
import sys
from time import sleep, time
import shutil
from datetime import datetime
import json
import os

import codecs
import torch
import random
import argparse
import numpy as np
from GPT2.model import (GPT2LMHeadModel)
from GPT2.utils import load_weight
from GPT2.config import GPT2Config
from GPT2.sample import sample_sequence
from GPT2.encoder import get_encoder


# linux
workedPath = "/var/lib/jenkins/workspace/NlpEngine/nlgengine"
# windows
if os.name =='nt':
    workedPath = os.getcwd()

class NlgEngine():

    def __init__(self, data):
        print('Bot start!')
        if os.name =='nt':
            self.setBot(data['job_settings_win'])
        else:
            self.setBot(data['job_settings_linux'])
        seed = random.randint(0, 2147483647)
        np.random.seed(seed)
        torch.random.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load Model
        self.enc = get_encoder()
        config = GPT2Config()
        self.model = GPT2LMHeadModel(config)
        state_dict = torch.load('gpt2-pytorch_model.bin', map_location='cpu' if not torch.cuda.is_available() else None)
        self.model = load_weight(self.model, state_dict)
        self.model.to(self.device)
        self.model.eval()

    def __del__(self):
        print("Bot stop !")

    def setBot(self, settings):
        print(settings)
        self.sourcePath = workedPath + settings['sourcePath']
        self.resultPath = workedPath + settings['resultPath']
        
    def get_samples(self, text, length, nsamples):

        # init variables
        batch_size = 1
        temperature = 0.7
        top_k = 40
        quiet = False
        unconditional = False

        print(text)
        context_tokens = self.enc.encode(text)
        return_list = []
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sample_sequence(
                model=self.model, length=length,
                context=context_tokens if not  unconditional else None,
                start_token=self.enc.encoder['<|endoftext|>'] if unconditional else None,
                batch_size=batch_size,
                temperature=temperature, top_k=top_k, device=self.device
            )
            out = out[:, len(context_tokens):].tolist()
            for i in range(batch_size):
                generated += 1
                return_text = self.enc.decode(out[i])
                if quiet is False:
                    print("=" * 40 + " SAMPLE " + str(generated) + " " + "=" * 40)
                print(return_text)
                return_list.append(return_text)
        return return_list


    def deleteSourceFile(self, filename):
        try:
            os.remove(self.sourcePath + filename)
            # shutil.move(self.sourcePath + filename, self.backupPath + filename)
            return True
        except Exception as e:

            print(e)
            return False

    def saveTextfile(self, filename, save_text):
        try:
            file_name = self.resultPath + str(filename.split(".")[0]) + '.txt'
            # file_name = os.path.join(self.resultPath, str(filename.split(".")[0]) + '_prepocessor.txt')
            file1 = open(file_name,"w")#write mode 
            file1.write(save_text) 
            print('success save file!', file_name)
            print('success save contents!', save_text)
            file1.close()
            self.deleteSourceFile(filename)
            return True
        except Exception as e:
            print(e)
            return False
    def get_nlu_labels(self, text):
        file_name = str(round(time()*1000)%1000000)+".txt"
        if os.name =='nt':
            NLP_REQUEST_FILE_PATH = self.sourcePath + "..\\..\\nlp_channel\\"
        else:
            NLP_REQUEST_FILE_PATH = self.sourcePath + "../../nlp_channel/"

        NLP_CLASSIFICATION_MAX_SECONDS = 10
        NLP_CLASSIFICATION_CHECK_GAP_SECONDS = 0.01
        try: 
            file = codecs.open(NLP_REQUEST_FILE_PATH + "input/" + file_name, "w","utf-8") 
            file.write(text)
            file.close()
        except Exception as e:
            print(e)
            return "{'defense_AH': 0, 'support_AH': 0, 'offense_AH': 0, 'defense_against_AH': 0}"
        counter_sec = NLP_CLASSIFICATION_MAX_SECONDS / NLP_CLASSIFICATION_CHECK_GAP_SECONDS
        return_label = "Server Error!"
        while counter_sec > 0:
            if os.path.exists(NLP_REQUEST_FILE_PATH + "output/" + file_name):
                file = open(NLP_REQUEST_FILE_PATH + "output/" + file_name, "r") 
                return_label = file.read()
                file.close()
                # nlu_result = json.loads(return_label.replace("'", '"'))
                if return_label == '':
                    continue
                break
            sleep(NLP_CLASSIFICATION_CHECK_GAP_SECONDS)
            counter_sec -= 1
        # if return_label != "Server Error!":
        #     saveNlutext(text, return_label)
        return return_label
    def nlu_support_rate(self, text):
        labels = self.get_nlu_labels(text)
        nlu_result = json.loads(labels.replace("'", '"'))
        return_support_rate = nlu_result['support_AH']
        if nlu_result['defense_AH'] > nlu_result['support_AH']:
            return_support_rate = nlu_result['defense_AH']
        return return_support_rate
    def pre_process_nlg_text(self, text):
        nlg_text = text.replace("\n", " ") # .replace("'", " ").replace('"', " ")
        if nlg_text.find('.') == -1:
            nlg_text += '.'
        elif nlg_text[-1] !='.':
            nlg_text += '.'

        # else:
        #     nlg_text = nlg_text[0:nlg_text.find('.')+1]
        return nlg_text
    def get_top_support_text(self, text):
        return_text =""
        while True:
            if self.nlu_support_rate(text) > 0.5:
                results = self.get_samples(text, random.randint(15, 50), 1)
            else:
                results = self.get_samples(text+" but Amber Heard is an actor, activist and humanitarian.", random.randint(15, 50), 1)
            top_support_rate = 0
            for nlg_text in results:
                nlg_text = self.pre_process_nlg_text(nlg_text)
                support_rate = self.nlu_support_rate(nlg_text)
                if support_rate > 0.6 and support_rate > top_support_rate:
                    top_support_rate = support_rate
                    return_text = nlg_text
            if return_text != "":
                return return_text

    def run(self):
        # print('running bots.')
        # print(os.listdir(self.sourcePath))
        for filename in os.listdir(self.sourcePath):
            file_name = os.path.join(self.sourcePath, filename)
            save_text = ''
            if '.txt' in file_name:
                try:
                    try:
                        file1 = open(file_name,"r", encoding='utf-8')#write mode 
                        test_sen1 = file1.read() 
                    except Exception as e:
                        print(e)
                        file1 = open(file_name,"r", encoding='cp1252')#write mode 
                        test_sen1 = file1.read() 
                    finally:
                        file1.close()
                    print("Now text classfication this contents :   ", test_sen1)
                    results = self.get_top_support_text(test_sen1)
                    print("Prediction Result : ", str(results))
                    self.saveTextfile(filename, str(results))
                except Exception as e:
                    print(e)

def main():
    with open(os.path.join(workedPath ,'NlgEngineSettings.json')) as json_file:
        print('loaded config.json file')
        data = json.load(json_file)
        my_bot = NlgEngine(data)
        while True:
            my_bot.run()
            # print('bot sleeping :', data['job_settings']['monitoringgaps'])
            sleep(data['job_settings']['monitoringgaps']/1000)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "-c",
    #     "--config",
    #     default="configs/classification_BERT_For_Amber.json",
    #     type=str,
    #     help="config file path (default: None)",
    # )
    # parser.add_argument(
    #     "-d",
    #     "--device",
    #     default=None,
    #     type=str,
    #     help="indices of GPUs to enable (default: all)",
    # )
    # args = parser.parse_args()
    # config = json.load(open(args.config))

    # if args.device is not None:
    #     config["device"] = args.device
    #     os.environ["CUDA_VISIBLE_DEVICES"] = args.device

    main()

