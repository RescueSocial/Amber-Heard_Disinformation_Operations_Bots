import os
import subprocess
import shlex
import psutil
from psutil import NoSuchProcess
import signal
import pickle
import ndjson
import json
import calendar
import time
import requests
import threading
import gzip
from stem import Signal
from stem.control import Controller
from file_read_backwards import FileReadBackwards

# SINCE = 1601510400
#QUERY = 'min_replies:20 trump OR biden OR @realDonaldTrump OR @JoeBiden OR usa2020elections OR usa2020 OR Election2020 OR Debates2020 OR VoteRedToSaveAmerica OR VoteRed OR VoteBlue OR VoteBlueToSaveAmerica OR trump2020 OR donaldtrump2020 OR DonaldTrump OR BidenHarris2020 OR joebiden2020 OR NeverTrump OR NeverBiden OR JoeBiden OR MAGA OR KAG OR WakeUpAmerica OR VoteEarly OR Ivoted OR VoteBidenHarrisToSaveAmerica OR VoteDonaldTrumpToSaveAmerica'
QUERY = '"Amber Heard" OR #AmberHeardIsAnAbuser OR #JusticeForJohnnyDepp OR #AmberHeardIsALiar'
# QUERY = 'mammamia'
# SINCE = 1601510400
# UNTIL = 1604188800

SINCE = 1609459200
UNTIL = 1619395200
TWEEPER_DIR = 'tweeper/'
HYDRATOR_DIR = 'hydrator/'

TWEEPER_CONFIG = 'configs/tweeper/'
HYDRATOR_CONFIG = 'configs/hydrator/'

TWEEPER_LOG = 'tweeper_logs/'
HYDRATOR_LOG = 'hydrator_logs/'

PYTHON = 'python3'

TWEEPER_DATA = 'result/'
HYDRATOR_DATA = 'result/'

TWEEPER_PARALLEL = 24
HYDRATOR_PARALLEL = 24


def change_ip():
    while True:
        with Controller.from_port(port=---) as controller:
            controller.authenticate(password='---')
            controller.signal(Signal.NEWNYM)
        session = requests.session()
        session.proxies = {}
        session.proxies['http'] = '---://localhost:---'
        session.proxies['https'] = '---://localhost:---'
        r = session.get('http://httpbin.org/ip')
        print(r.text)
        time.sleep(30)


def running(pid):
    if pid is None:
        return False
    try:
        proc = psutil.Process(pid)
        if proc.status() == psutil.STATUS_ZOMBIE:
            return False
        os.kill(pid, 0)
    except (OSError, NoSuchProcess):
        return False
    else:
        return True

def main():
    if not os.path.exists(TWEEPER_DATA):
        os.makedirs(TWEEPER_DATA)
    if not os.path.exists(HYDRATOR_DATA):
        os.makedirs(HYDRATOR_DATA)
    if not os.path.exists(TWEEPER_CONFIG):
        os.makedirs(TWEEPER_CONFIG)
    if not os.path.exists(HYDRATOR_CONFIG):
        os.makedirs(HYDRATOR_CONFIG)
    if not os.path.exists(TWEEPER_LOG):
        os.makedirs(TWEEPER_LOG)
    if not os.path.exists(HYDRATOR_LOG):
        os.makedirs(HYDRATOR_LOG)

    if os.path.exists('pids'):
        with open('pids', 'rb') as f:
            pids = pickle.load(f)
    else:
        pids = {
            'tweeper': None,
            'hydrator': None
        }

    if pids['tweeper'] is not None:
        if running(pids['tweeper']):
            os.kill(pids['tweeper'], signal.SIGTERM)
            pids['tweeper'] = None
    if pids['hydrator'] is not None:
        if running(pids['hydrator']):
            os.kill(pids['hydrator'], signal.SIGTERM)
            pids['hydrator'] = None
    with open('pids', 'wb') as f:
        pickle.dump(pids, f)

    thread = threading.Thread(target=change_ip, args=())
    thread.daemon = True
    thread.start()

    counter = 0

    while True:
        HYDRATOR_PARALLEL = 48
        with open('pids', 'rb') as f:
            pids = pickle.load(f)
        if not running(pids['tweeper']):
            launched = False
            logs = sorted(os.listdir('{0}'.format(TWEEPER_LOG)))
            for log in logs:
                with FileReadBackwards('{0}{1}'.format(TWEEPER_LOG, log), encoding='utf-8') as frb:
                    try:
                        line = frb.readline()
                        message = ndjson.loads(line)[0]['message']
                    except (json.decoder.JSONDecodeError, IndexError):
                        message = 'ERROR'
                    if message != 'DONE':
                        since, until = log.split('_')[1:]
                        since = int(since)
                        until = int(until)
                        config = {
                            'name': '{0}{1}_{2}'.format(TWEEPER_DATA, since, until),
                            'query': QUERY,
                            'since': since,
                            'until': until,
                            'interval': 1,
                            'parallel': TWEEPER_PARALLEL
                        }
                        with open('{0}config_{1}_{2}.json'.format(TWEEPER_CONFIG, since, until), 'w') as f:
                            json.dump(config, f, ensure_ascii=False)
                        command = '{0} {1}main.py config -f {2}config_{3}_{4}.json'.format(PYTHON, TWEEPER_DIR,
                                                                                           TWEEPER_CONFIG, since, until)
                        args = shlex.split(command)
                        tweeper_process = subprocess.Popen(args, stdin=None, stdout=open(
                            '{0}log_{1}_{2}'.format(TWEEPER_LOG, since, until), 'a'), stderr=open(
                            '{0}log_{1}_{2}'.format(TWEEPER_LOG, since, until), 'a'))
                        pids['tweeper'] = tweeper_process.pid
                        with open('pids', 'wb') as f:
                            pickle.dump(pids, f)
                        launched = True
                        HYDRATOR_PARALLEL = 24
                        break
            if not launched:
                since = int(logs[-1].split('_')[2]) if len(logs) > 0 else SINCE
                # until = calendar.timegm(time.gmtime())
                # DAY BY DAY
                until = since + 60 * 60 * 24
                if until <= UNTIL:
                    config = {
                        'name': '{0}{1}_{2}'.format(TWEEPER_DATA, since, until),
                        'query': QUERY,
                        'since': since,
                        'until': until,
                        'interval': 1,
                        'parallel': TWEEPER_PARALLEL
                    }
                    with open('{0}config_{1}_{2}.json'.format(TWEEPER_CONFIG, since, until), 'w') as f:
                        json.dump(config, f, ensure_ascii=False)
                    command = '{0} {1}main.py config -f {2}config_{3}_{4}.json'.format(PYTHON, TWEEPER_DIR, TWEEPER_CONFIG, since, until)
                    args = shlex.split(command)
                    tweeper_process = subprocess.Popen(args, stdin=None, stdout=open('{0}log_{1}_{2}'.format(TWEEPER_LOG, since, until), 'a'), stderr=open('{0}log_{1}_{2}'.format(TWEEPER_LOG, since, until), 'a'))
                    pids['tweeper'] = tweeper_process.pid
                    with open('pids', 'wb') as f:
                        pickle.dump(pids, f)
                    launched = True
                    HYDRATOR_PARALLEL = 24
        # else:
        #     HYDRATOR_PARALLEL = 24
        # time.sleep(5)
        # folders = sorted(os.listdir('{0}'.format(HYDRATOR_DATA)))
        # hydrated_conversations = []
        # for folder in folders:
        #     if os.path.exists('{0}{1}/conversations/'.format(HYDRATOR_DATA, folder)):
        #         conversations = os.listdir('{0}{1}/conversations'.format(HYDRATOR_DATA, folder))
        #         for conversation in conversations:
        #             hydrated_conversations.append(conversation.split('_')[1].split('.')[0])
        # if not running(pids['hydrator']):
        #     launched = False
        #     for folder in folders:
        #         if not os.path.exists('{0}{1}/conversations/'.format(HYDRATOR_DATA, folder)):
        #             # tweets_files = sorted(os.listdir('{0}{1}/tweets'.format(HYDRATOR_DATA, folder)))
        #             tweets_files = sorted(t for t in os.listdir('{0}{1}/tweets'.format(HYDRATOR_DATA, folder)) if t.endswith('.gz'))
        #             incomplete_tweets_files = sorted(t for t in os.listdir('{0}{1}/tweets'.format(HYDRATOR_DATA, folder)) if t.endswith('.ndjson'))
        #             if len(tweets_files) > 0 and len(incomplete_tweets_files) == 0:
        #                 conversations = []
        #                 for tweet_file in tweets_files:
        #                     with gzip.open('{0}{1}/tweets/{2}'.format(HYDRATOR_DATA, folder, tweet_file), 'rt') as f:
        #                         # tweets = ndjson.reader(f)
        #                         for f_tweet in f:
        #                             tweet = json.loads(f_tweet)
        #                             # if tweet['id_str'] not in hydrated_conversations and ( tweet['in_reply_to_status_id_str'] is not None or tweet['reply_count'] > 0 ):
        #                             if tweet['conversation_id_str'] not in hydrated_conversations:
        #                                 conversations.append(tweet['conversation_id_str'])
        #                                 hydrated_conversations.append(tweet['conversation_id_str'])
        #                 since, until = folder.split('_')
        #                 config = {
        #                     'name': '{0}{1}_{2}'.format(HYDRATOR_DATA, since, until),
        #                     'conversations': conversations,
        #                     'parallel': HYDRATOR_PARALLEL
        #                 }
        #                 with open('{0}config_{1}_{2}.json'.format(HYDRATOR_CONFIG, since, until), 'w') as f:
        #                     json.dump(config, f, ensure_ascii=False)
        #                 command = '{0} {1}main.py config -f {2}config_{3}_{4}.json'.format(PYTHON, HYDRATOR_DIR,
        #                                                                                    HYDRATOR_CONFIG, since, until)
        #                 args = shlex.split(command)
        #                 hydrator_process = subprocess.Popen(args, stdin=None, stdout=open(
        #                     '{0}log_{1}_{2}'.format(HYDRATOR_LOG, since, until), 'a'), stderr=open(
        #                     '{0}log_{1}_{2}'.format(HYDRATOR_LOG, since, until), 'a'))
        #                 pids['hydrator'] = hydrator_process.pid
        #                 with open('pids', 'wb') as f:
        #                     pickle.dump(pids, f)
        #                 launched = True
        #                 break






                        
            # if not launched and len(folders) > 0:
            #     folder = folders[counter]
            #     if counter == 0:
            #         hydrated_conversations = []
            #     counter = (counter + 1) % len(folders)
            #     # tweets_files = sorted(os.listdir('{0}{1}/tweets'.format(HYDRATOR_DATA, folder)))
            #     tweets_files = sorted(
            #         t for t in os.listdir('{0}{1}/tweets'.format(HYDRATOR_DATA, folder)) if t.endswith('.gz'))
            #     incomplete_tweets_files = sorted(t for t in os.listdir('{0}{1}/tweets'.format(HYDRATOR_DATA, folder)) if t.endswith('.ndjson'))
            #     if len(tweets_files) > 0 and len(incomplete_tweets_files) == 0:
            #         conversations = []
            #         for tweet_file in tweets_files:
            #             with gzip.open('{0}{1}/tweets/{2}'.format(HYDRATOR_DATA, folder, tweet_file), 'rt') as f:
            #                 # tweets = ndjson.reader(f)
            #                 for f_tweet in f:
            #                     tweet = json.loads(f_tweet)
            #                     # if tweet['conversation_id_str'] not in hydrated_conversations and (tweet['in_reply_to_status_id_str'] is not None or tweet['reply_count'] > 0):
            #                     if tweet['conversation_id_str'] not in hydrated_conversations:
            #                         conversations.append(tweet['conversation_id_str'])
            #                         hydrated_conversations.append(tweet['conversation_id_str'])
            #         since, until = folder.split('_')
            #         config = {
            #             'name': '{0}{1}_{2}'.format(HYDRATOR_DATA, since, until),
            #             'conversations': conversations,
            #             'parallel': HYDRATOR_PARALLEL
            #         }
            #         with open('{0}config_{1}_{2}.json'.format(HYDRATOR_CONFIG, since, until), 'w') as f:
            #             json.dump(config, f, ensure_ascii=False)
            #         command = '{0} {1}main.py config -f {2}config_{3}_{4}.json'.format(PYTHON, HYDRATOR_DIR,
            #                                                                            HYDRATOR_CONFIG, since, until)
            #         args = shlex.split(command)
            #         hydrator_process = subprocess.Popen(args, stdin=None, stdout=open(
            #             '{0}log_{1}_{2}'.format(HYDRATOR_LOG, since, until), 'a'), stderr=open(
            #             '{0}log_{1}_{2}'.format(HYDRATOR_LOG, since, until), 'a'))
            #         pids['hydrator'] = hydrator_process.pid
            #         with open('pids', 'wb') as f:
            #             pickle.dump(pids, f)
            #         launched = True

if __name__ == '__main__':
    main()