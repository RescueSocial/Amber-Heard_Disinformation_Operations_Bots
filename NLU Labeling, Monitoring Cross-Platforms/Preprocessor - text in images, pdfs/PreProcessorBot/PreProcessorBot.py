from time import sleep
import json
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import shutil
from pdf2image import convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
    )
# linux
workedPath = "/var/www/html/bots.worldie.com/PreProcessorBot"
# windows
if os.name =='nt':
    workedPath = os. os.getcwd()
    # pre_processor_out_path = os.getcwd() + '\\output'
    tesseract_cmd_path = r'c:\Program Files\Tesseract-OCR\tesseract.exe'
else:
# linux
    # pre_processor_out_path = os.getcwd() + '/output'
    tesseract_cmd_path = '/var/www/html/bots.worldie.com/PreProcessorBot/tesseract-4.1.1/'

class PreProcessorBot():

    def __init__(self, data):
        print('Bot start!')
        if os.name =='nt':
            self.setBot(data['job_settings_win'])
        else:
            self.setBot(data['job_settings_linux'])

    
    def __del__(self):
        print("Bot stop !")

    def setBot(self, settings):
        print(settings)
        self.sourcePath = workedPath + settings['sourcePath']
        self.resultPath = workedPath + settings['resultPath']
        self.backupPath = workedPath + settings['backupPath']

    def moveSourceFile(self, filename):
        shutil.move(self.sourcePath + filename, self.backupPath + filename)
        return True

    def saveTextfile(self, filename, save_text):
        file_name = self.resultPath + str(filename.split(".")[0]) + '.txt'
        # file_name = os.path.join(self.resultPath, str(filename.split(".")[0]) + '_prepocessor.txt')
        file1 = open(file_name,"w")#write mode 
        file1.write(save_text) 
        print('success save file!', file_name)
        print('success save contents!', save_text)
        file1.close()
        self.moveSourceFile(filename)
        return True

    def run(self):
        # print('running bots.')
        print(os.listdir(self.sourcePath))
        for filename in os.listdir(self.sourcePath):
            file_name = os.path.join(self.sourcePath, filename)
            print("Now pre-processing this file : ", filename)
            save_text = ''
            if '.pdf' in file_name:
                try:
                    images = convert_from_bytes(open(file_name,'rb').read())
                    print('all pages:', len(images))
                    for i, image in enumerate(images):
                        try:
                            print('recognition for page:', i)
                            save_text += '\nPage ' + str(i + 1) + '\n'
                            if os.name =='nt':
                                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
                            save_text += pytesseract.image_to_string(image)
                        except Exception as e:
                            print(e)
                            continue
                    
                except Exception as e:
                    print(e)
                self.saveTextfile(filename, save_text)
            
            elif '.png' in file_name or '.jpg' in file_name:
                try:
                    if os.name =='nt':
                        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd_path
                    save_text = pytesseract.image_to_string(Image.open(file_name))
                except Exception as e:
                    print(e)  
                self.saveTextfile(filename, save_text)

def main():
    with open(os.path.join(workedPath ,'PreprocessorBotSetting.json')) as json_file:
        print('loaded config.json file')
        data = json.load(json_file)
        my_bot = PreProcessorBot(data)
        counts = data['job_settings']['counts']
        while counts > 0:
            my_bot.run()
            print('bot sleeping :', data['job_settings']['monitoringgaps'])
            sleep(data['job_settings']['monitoringgaps']/1000)
            counts -= 1

if __name__ == '__main__':
    main()



