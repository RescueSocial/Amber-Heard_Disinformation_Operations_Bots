from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.chrome.options import Options
import math
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui
import numpy as np
import random
import function as fn
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# random integer from 0 to 9

class Twitterbot:

    def __init__(self,username,password,userid):
        self.username = username
        self.password = password
        self.userid = userid
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('--headless')
        self.bot = webdriver.Chrome(executable_path=r"D:\crawler\crawler\\chromedriver.exe",chrome_options=chrome_options)

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        fn.timesleepbysecond()
        bot.find_element_by_xpath('/html/body/div/div/div/div/main/div/div/div/div[1]/div/div[3]/div[5]/a').click()
        fn.smalltimesleepbysecond()
        email = bot.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[5]/label/div/div[2]/div/input')
        email.clear()
        email.send_keys(self.username)
        email.send_keys(Keys.RETURN)
        fn.smalltimesleepbysecond()
        ## uncomment this code if twitter give an extra check for asking username
        # usercheck = bot.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/label/div/div[2]/div/input')
        # usercheck.clear()
        # usercheck.send_keys(self.userid)
        # usercheck.send_keys(Keys.RETURN)
        fn.smalltimesleepbysecond()
        password = bot.find_element_by_xpath('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password.clear()
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        fn.smalltimesleepbysecond()


    def get_like_list(self,id,name):
            bot = self.bot
            twitter = bot.get('https://twitter.com//'+name+'/status/'+str(id))
            fn.timesleepbysecond()
            outertry = 3
            innertry = 3
            innerinnertry = 3
            for i in range(outertry):
                try:
                    #bot.execute_script('window.scrollTo(0, 200)')
                    #xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div[2]/div/a'
                    #element = WebDriverWait(bot, 10).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                    print('First Check Outer')
                    xpath1 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div'
                    #xpath2 = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[10]/div/div[1]/article/div/div/div/div[3]/div[4]/div'
                    count = bot.find_element_by_xpath(xpath1).text
                    count = count.split()
                    count, path = fn.checkdiv(count)
                    count = fn.countnumber(count)
                    # count = count.replace(",", "")
                    if int(count) > 0:
                        bot.find_element_by_xpath(path).click()
                        #element.click()
                        fn.smalltimesleepbysecond()
                        print('First Check Outer Work')
                        n = 0
                        data = []
                        pyautogui.moveTo(32, 39)
                        fn.smalltimesleepbysecond()
                        pyautogui.moveTo(952, 306)
                        fn.smalltimesleepbysecond()
                        pyautogui.click()
                        for j in range(innertry):
                            try:
                                print('First Check Inner')
                               # countpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div/div/a/div'
                                #element = WebDriverWait(bot, 10).until(EC.visibility_of_element_located((By.XPATH, countpath)))
                                number = fn.formatnumber(count)
                                print(number)
                                print('First Check Inner Work')
                                for z in range(innerinnertry):
                                    try:
                                       #test = WebDriverWait(bot, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
                                       test = bot.find_element_by_tag_name('body')
                                       while n < number:
                                           fn.scrolltimesleepbysecond()
                                           test.send_keys(Keys.END)
                                           fn.scrolltimesleepbysecond()
                                           n += 1
                                           print('First Check Inner Inner')
                                           html = bot.find_element_by_xpath("//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/section/div").get_attribute('innerHTML')
                                           soup = BeautifulSoup(html, 'lxml')
                                           f = soup.find_all('span')
                                           for span in f:
                                               data.append(span.text)
                                               print(data)
                                       df = pd.DataFrame(data, columns=['text'])
                                       df = df[df['text'].str.contains('@')]
                                       df = df.drop_duplicates(keep="first")
                                       root = "Tweets"
                                       df.to_csv(str(id), index=False)
                                       print('All Worked')
                                    except NoSuchElementException:
                                       if z < innerinnertry - 1:
                                           fn.timesleepbysecond()
                                           continue
                                       else:
                                           return
                                    break
                            except NoSuchElementException:

                                # if outertry < 0:
                                #     # dft.append(str(id))
                                #     # dtf = dtf + 1
                                #     # print(dtf, "Tweets are not fetch")
                                #     # didntfetchtweet = pd.DataFrame(dft)
                                #     # didntfetchtweet.to_csv(r'didnttweet.txt', header=True, index=None, sep=',', mode='a')

                                if j < innertry - 1:
                                    fn.timesleepbysecond()
                                    continue
                                else:
                                    return
                            break
                    else:
                        # nullt.append(str(id))
                        # null = null + 1
                        # print(null, "Tweets are Empty")
                        # nullfet = pd.DataFrame(nullt)
                        # nullfet.to_csv(r'nulltweet.txt', header=True, index=None, sep=',', mode='a')
                        break
                except NoSuchElementException:
                    if i < outertry - 1:
                        continue
                    else:
                        return
                break


#status = ['bridgecrewio','1471169946902216708']
#for i in status:

data = pd.read_csv('data.txt') ## file to upload consisting of id and tweet_id
n = len(data)
count = 0
null = 0
dtf =0
tweetremoved = []
nullt = []
dft = []
## user email,password,username
ed = Twitterbot('email@gmail.com','password','username')
ed.login()
tweetfetch = []
tweetfet = pd.DataFrame(columns=['fetch'])
nulltweet = pd.DataFrame(columns=['nulltweet'])
didntfetchtweet = pd.DataFrame(columns=['dft'])

for i in range(n):
    response = fn.checkurl(data['user.screen_name'][i], data['id_str'][i])
    if response:
        ed.get_like_list(data['id_str'][i], data['user.screen_name'][i])
        count = count + 1
        tweetfetch.append(str(data['id_str'][i]))
        print(tweetfetch)
        tweetfet = pd.DataFrame(tweetfetch)
        tweetfet.to_csv(r'Tweetfetch.txt', header=True, index=None, sep=',', mode='a')
        #datas = data.drop(data[data['id_str'] == data['id_str'][i]].index)
        #datas.to_csv(r'Teri.txt', header=True, index=None, sep=',', mode='a')
        if count == 10:
            fn.timesleepbyminutes()
            print('wait occur')
    else:
        tweet = 'https://twitter.com/'+ data['user.screen_name'][i] +'/status/'+ str(data['id_str'][i])
        tweetremoved.extend(tweet)
        tweetrem = pd.DataFrame(tweetremoved, columns=['removed'])
        tweetrem.to_csv('tweetremoved.csv', index=False)
        continue