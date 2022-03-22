import os
import requests
from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from copy import deepcopy
from multiprocessing import set_start_method
from multiprocessing import get_context
import logging.handlers
from pythonjsonlogger import jsonlogger
from itertools import (takewhile, repeat)
import re
import urllib3
import time
import ndjson
import json
import gzip
import shutil
from query import Query
from tweets import recompose_tweets
from user_agent import generate_user_agent
from requests.exceptions import ChunkedEncodingError
from urllib3.exceptions import ReadTimeoutError, ProtocolError
from http.client import IncompleteRead
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger('Hydrator')
formatter = jsonlogger.JsonFormatter('%(asctime)%(levelname)%(session)%(message)%(name)')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False


class Hydrator:
    def __init__(self, config):
        set_start_method('spawn')
        self.config = config
        self.session_id = 0

    def get_tweets(self):
        logger.info('{0} processes'.format(self.config['parallel']))
        # pool = Pool()

        with get_context("spawn").Pool(self.config['parallel']) as pool:
            if not os.path.exists(self.config['name']):
                os.makedirs(self.config['name'])
            if not os.path.exists('{0}/conversations'.format(self.config['name'])):
                os.makedirs('{0}/conversations'.format(self.config['name']))
            if not os.path.exists('{0}/cache'.format(self.config['name'])):
                os.makedirs('{0}/cache'.format(self.config['name']))

            res = []
            session = Session()

            session.proxies = {}
            session.proxies['http'] = 'socks5h://localhost:9050'
            session.proxies['https'] = 'socks5h://localhost:9050'

            session = _update_headers(session, -1)
            retries = Retry(total=60, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
            session.mount('https://', HTTPAdapter(max_retries=retries))
            for conversation in self.config['conversations']:
                query = Query(conversation)
                query_copy = deepcopy(query)
                logger.info(
                    {'session': self.session_id, 'message': 'Started tweets scraping for conversation {0}'.format(
                        conversation)})
                res.append(
                    pool.apply_async(_consume_query, args=[query_copy, session, self.session_id, self.config['name']]))
                self.session_id += 1
            pool.close()
            pool.join()
            logger.info('DONE')
            for r in res:
                r.get()


def _update_headers(session, session_id):
    session.headers.update({
        'Connection': 'keep-alive',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16c'
                         'HjhLTvJu4FA33AGWWjCpTnA',
        'x-guest-token': _fetch_token(session_id),
        'x-twitter-active-user': 'yes',
        'User-Agent': generate_user_agent(device_type='desktop'),
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://twitter.com/',
        'Accept-Language': 'en-US;q=0.8,en;q=0.7',
    })
    return session


def _get_csrf_token():
    prefix = b'CODEX'
    remainder = 32 // 2 - len(prefix)
    rem_bytes = os.urandom(remainder)
    return (prefix + rem_bytes).hex()


def _fetch_token(session_id, retries=60):
    token = None
    token_url = 'https://twitter.com/'
    while not token:
        session = Session()

        session.proxies = {}
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'

        session.headers.update({
            'User-Agent': generate_user_agent(device_type='desktop'),
            'x-csrf-token': _get_csrf_token(),
        })
        retries = Retry(total=60, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        request = session.prepare_request(Request('GET', token_url))
        try:
            response = session.send(request, timeout=12)
        except (
        requests.exceptions.RetryError, requests.exceptions.ConnectionError, ReadTimeoutError, ChunkedEncodingError, ProtocolError, IncompleteRead,
        socket.timeout):
            time.sleep(10)
            continue
        if match := re.search(r'"gt=(\d+);', response.text):
            token = match.group(1)
        elif 'gt' in response.cookies:
            token = response.cookies['gt']
        else:
            logger.warning({'session': session_id, 'message': 'x-guest-token not found, waiting 5 seconds...'})
            time.sleep(5)
    return token


def _search_query(query, session, session_id, retries=60):
    if retries == 0:
        logger.error({'session': session_id, 'message': 'MAX retries for conversation {0}'.format(query.conversation)})
        return [], None, []
    params = query.generate_params()
    request = session.prepare_request(Request('GET', query.base_url, params=params, cookies={}))
    try:
        response = session.send(request, timeout=12)
    except (requests.exceptions.RetryError, requests.exceptions.ConnectionError, ReadTimeoutError, ChunkedEncodingError, ProtocolError, IncompleteRead,
            socket.timeout):
        logger.error({'session': session_id, 'message': 'Connection error'})
        session = _update_headers(session, session_id)
        time.sleep(10)
        return _search_query(query, session, session_id, retries - 1)
    try:
        response_json = response.json()
    except (ValueError, AttributeError):
        logger.error({'session': session_id, 'message': 'Value or attribute error for resp.json, stopping'})
        session = _update_headers(session, session_id)
        time.sleep(10)
        return _search_query(query, session, session_id, retries - 1)

    if 'errors' in response_json:
        if response_json['errors'][0]['code'] == 34:
            logger.error({'session': session_id, 'message': 'Error code 34, page not found'})
            return [], None, []

    if 'timeline' not in response_json:
        logger.warning({'session': session_id, 'message': '"timeline" not in response'})
        time.sleep(10)
        session = _update_headers(session, session_id)
        return _search_query(query, session, session_id, retries - 1)

    if len(response_json['timeline']['instructions']) == 0:
        logger.warning({'session': session_id, 'message': '"instructions" length is 0'})
        time.sleep(10)
        session = _update_headers(session, session_id)
        return _search_query(query, session, session_id, retries - 1)

    if 'addEntries' not in response_json['timeline']['instructions'][0]:
        logger.error({'session': session_id, 'message': '"addEntries" not in response'})
        # time.sleep(10)
        # session = _update_headers(session, session_id)
        return [], None, []

    if 'errors' in response_json:
        logger.warning({'session': session_id, 'message': '"errors" in response'})
        time.sleep(10)
        session = _update_headers(session, session_id)
        return _search_query(query, session, session_id, retries - 1)

    if response_json['globalObjects']['tweets'] == {} and not response_json['timeline']['instructions'][0]['addEntries']['entries'] == []:
        logger.warning({'session': session_id, 'message': '"tweets" and "entries" empty '})
        time.sleep(10)
        session = _update_headers(session, session_id)
        return _search_query(query, session, session_id, retries - 1)

    if response_json['globalObjects']['tweets'] == {}:
        return [], None, []
    tweets, cursor, mores = recompose_tweets(response_json)
    next_query = deepcopy(query)
    next_query.cursor = cursor
    return tweets, next_query, mores


def _consume_query(query, session, session_id, session_name):
    saw = []
    go_on = True
    if os.path.exists('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation)):
        with open('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation),
                  encoding='utf-8') as f:
            tweets_objs = ndjson.reader(f)
        for tweet in tweets_objs:
            saw.append(tweet['id_str'])
    if os.path.exists('{0}/conversations/conversation_{1}.ndjson.gz'.format(session_name, query.conversation)):
        with gzip.open('{0}/conversations/conversation_{1}.ndjson.gz'.format(session_name, query.conversation),
                       encoding='utf-8', mode='rt') as f:
            # tweets_objs = ndjson.reader(f)
            for f_tweet in f:
                tweet = json.loads(f_tweet)
                saw.append(tweet['id_str'])
            # for tweet in tweets_objs:
            #     saw.append(tweet['id_str'])
    tweets_file = open('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation), 'a+',
                       encoding='utf-8')
    tweets_writer = ndjson.writer(tweets_file, ensure_ascii=False)
    show_mores = []

    roots = [query.conversation]
    tmp_tweets, next_query, mores = _search_query(query, session, session_id)
    if next_query is None:
        go_on = False
    show_mores += mores

    if go_on:
        for t in tmp_tweets:
            if t['id_str'] not in saw:
                saw.append(t['id_str'])
                tweets_writer.writerow(t)
                tweets_file.flush()
        while next_query.cursor != '':
            tmp_tweets, next_query, mores = _search_query(next_query, session, session_id)
            if next_query is None:
                break
            for t in tmp_tweets:
                if t['id_str'] not in saw:
                    saw.append(t['id_str'])
                    tweets_writer.writerow(t)
                    tweets_file.flush()
            show_mores += mores
            show_mores = list(set(show_mores) - set(roots))

        while len(show_mores) > 0:
            if next_query is None:
                next_query = Query()
            next_query.set_parameter(show_mores[0])
            roots.append(next_query.conversation)
            show_mores.pop(0)
            tmp_tweets, next_query, mores = _search_query(next_query, session, session_id)
            if next_query is None:
                break
            show_mores += mores
            show_mores = list(dict.fromkeys(show_mores))
            show_mores = list(set(show_mores) - set(roots))
            for t in tmp_tweets:
                if t['id_str'] not in saw:
                    saw.append(t['id_str'])
                    tweets_writer.writerow(t)
                    tweets_file.flush()
            while next_query.cursor != '':
                tmp_tweets, next_query, mores = _search_query(next_query, session, session_id)
                if next_query is None:
                    break
                show_mores += mores
                show_mores = list(dict.fromkeys(show_mores))
                show_mores = list(set(show_mores) - set(roots))
                for t in tmp_tweets:
                    if t['id_str'] not in saw:
                        saw.append(t['id_str'])
                        tweets_writer.writerow(t)
                        tweets_file.flush()
    n_tweets = _raw_count('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation))
    logger.info({'session': session_id, 'message': '{0} tweets found for conversation {1}'.format(
        n_tweets,
        query.conversation)})
    if n_tweets <= 1:
        os.remove('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation))
    else:
        if os.path.exists('{0}/conversations/conversation_{1}.ndjson.gz'.format(session_name, query.conversation)):
            with gzip.open('{0}/conversations/conversation_{1}.ndjson.gz'.format(session_name, query.conversation),
                           encoding='utf-8', mode='rt') as f:
                # tweets_objs = ndjson.reader(f)

                for f_tweet in f:
                    tweet = json.loads(f_tweet)
                    tweets_writer.writerow(tweet)
            os.remove('{0}/conversations/conversation_{1}.ndjson.gz'.format(session_name, query.conversation))
        tweets_file.close()
        with open('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation), 'rb') as f_in:
            with gzip.open('{0}/conversations/conversation_{1}.ndjson.gz'.format(session_name, query.conversation),
                           'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove('{0}/conversations/conversation_{1}.ndjson'.format(session_name, query.conversation))


def _raw_count(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024 * 1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen)
