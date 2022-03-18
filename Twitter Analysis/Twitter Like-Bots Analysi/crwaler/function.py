import random
import time
import requests
from selenium.common.exceptions import NoSuchElementException
import math

def timesleepbysecond():
    number = random.randint(3, 12)
    time.sleep(number)
    return time.sleep(number)

def smalltimesleepbysecond():
    number = random.randint(2, 10)
    time.sleep(number)
    return time.sleep(number)

def timesleepbyminutes():
    number = random.randint(30, 100)
    time.sleep(number)
    return time.sleep(number)


def scrolltimesleepbysecond():
    number = random.randint(1, 3)
    time.sleep(number)
    return time.sleep(number)

def checkurl(name,id):
    response = requests.get('https://twitter.com//'+name+'/status/'+str(id))
    if response.status_code == 200:
        return True
    else:
        return False


def check_exists_by_xpath(xpath,bot):
    try:
        bot.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def countnumber(number):
    try:
        if ',' in number:
            number = number.replace(",", "")
            y = int(number)
            return  y
        elif 'K' in number:
            number = number.replace("K", "")
            number = number.replace(".", "")
            y = int(number)
            y = y * 100
            return y
        elif 'M' in number:
            number = number.replace("M", "")
            number = number.replace(".", "")
            y = int(number)
            y = y * 10000
            return y
        else:
            y = int(number)
            return y
    except:
        y = int(number)
        return y

def formatnumber(number):
    y = number / 23 + 1
    y = math.floor(y)
    return y
    # elif number >= 1000 and number < 10000:
    #     #umber = number.replace(",", "")
    #     y = int(number)
    #     y = y / 23 + 1
    #     y = math.floor(y)
    #     return  y
    # elif number >= 10000 and number < 1000000:
    #     number = number.replace("K", "")
    #     number = number.replace(".", "")
    #     number = number * 10000
    #     y = int(number)
    #     y = y / 23 + 1
    #     y = math.floor(y)
    #     return y
    # else:
    #     number = number.replace("M", "")
    #     number = number.replace(".", "")
    #     number = number * 1000000
    #     y = int(number)
    #     y = y / 23 + 1
    #     y = math.floor(y)
    #     return y

def checkdiv(count):
    print(count)
    print(len(count))

    if not count:
        return 0,0
    elif count[1] in (('Retweet','Retweets')) and (int(len(count)) == 2):
        return 0, 0
    elif count[1] in (('Quote', 'Quotes','Tweets')) and (int(len(count)) == 3):
        return 0, 0
    elif count[1] in (('Quote', 'Tweet', 'Quotes')) and (count[4] != 'Likes' or count[4] != 'Like') and (int(len(count)) == 5):
        return 0, 0
    elif count[1] in (('Quote', 'Tweet', 'Quotes','Retweet','Retweets'))  and (int(len(count)) == 5):
        return 0, 0
    elif (int(len(count)) >7 ):
        return 0, 0
    elif str(count[1]) == 'Like' or str(count[1]) == 'Likes':
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div/div/a'
        return count[0], path
    elif count[1] in ('Retweet','Retweets') and (int(len(count)) == 4):
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div[2]/div/a'
        return count[2], path
    elif count[1] in ('Quote', 'Tweet', 'Quotes'):
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div[2]/div/a'
        return count[3], path
    elif count[1] in (('Quote', 'Tweet', 'Quotes', 'Retweet', 'Retweets','Likes')) and (int(len(count)) == 7):
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div[3]/div/a'
        return count[5], path
    else:
        path = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[1]/div/div[1]/article/div/div/div/div[3]/div[4]/div/div[3]/div/a'
        return count[4], path
