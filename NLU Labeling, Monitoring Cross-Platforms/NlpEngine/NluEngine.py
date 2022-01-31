
import sys
from time import sleep
import shutil

from multiclassification import MultiClassification

from datetime import datetime

import argparse
import json
import os


# linux
workedPath = "/var/lib/jenkins/workspace/NlpEngine/nlpengine"
# windows
if os.name =='nt':
    workedPath = os.getcwd()

class NlpEngine():

    def __init__(self, data, config):
        print('Bot start!')
        if os.name =='nt':
            self.setBot(data['job_settings_win'])
        else:
            self.setBot(data['job_settings_linux'])
        self.classification = MultiClassification('original', config=config)
    
    def __del__(self):
        print("Bot stop !")

    def setBot(self, settings):
        print(settings)
        self.sourcePath = workedPath + settings['sourcePath']
        self.resultPath = workedPath + settings['resultPath']
        


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
                    results = self.classification.predict(test_sen1)
                    print("Prediction Result : ", str(results))
                    self.saveTextfile(filename, str(results))
                except Exception as e:
                    print(e)
                


def main(config='null'):
    with open(os.path.join(workedPath ,'NluEngineSettings.json')) as json_file:
        print('loaded config.json file')
        data = json.load(json_file)
        my_bot = NlpEngine(data, config=config)
        while True:
            my_bot.run()
            # print('bot sleeping :', data['job_settings']['monitoringgaps'])
            sleep(data['job_settings']['monitoringgaps']/1000)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        default="configs/classification_BERT_For_Amber.json",
        type=str,
        help="config file path (default: None)",
    )
    parser.add_argument(
        "-d",
        "--device",
        default=None,
        type=str,
        help="indices of GPUs to enable (default: all)",
    )
    args = parser.parse_args()
    config = json.load(open(args.config))

    if args.device is not None:
        config["device"] = args.device
        os.environ["CUDA_VISIBLE_DEVICES"] = args.device

    main(config=config)

