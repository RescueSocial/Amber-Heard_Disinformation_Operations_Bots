import os
from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from datetime import datetime
from copy import deepcopy
from multiprocessing.pool import Pool
from multiprocessing import set_start_method
from multiprocessing import get_context
import logging.handlers
from pythonjsonlogger import jsonlogger
from file_read_backwards import FileReadBackwards
from itertools import (takewhile, repeat)
import re
import urllib3
import calendar
import time
import ndjson
import gzip
import shutil
from query import Query
from tweets import recompose_tweets
from user_agent import generate_user_agent

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger('Tweeper')
formatter = jsonlogger.JsonFormatter('%(asctime)%(levelname)%(session)%(message)%(name)')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False


class Tweeper:
    def __init__(self, config):
        set_start_method('spawn')
        self.config = config
        self.session_id = 0

    def get_tweets(self):
        logger.info('{0} processes'.format(self.config['parallel']))
        # pool = Pool(self.config['parallel'])
        with get_context("spawn").Pool(self.config['parallel']) as pool:
            if not os.path.exists(self.config['name']):
                os.makedirs(self.config['name'])
            if not os.path.exists('{0}/tweets'.format(self.config['name'])):
                os.makedirs('{0}/tweets'.format(self.config['name']))
            if not os.path.exists('{0}/cache'.format(self.config['name'])):
                os.makedirs('{0}/cache'.format(self.config['name']))

            query = Query(config=self.config)
            res = []
            session = Session()

            session.proxies = {}
            session.proxies['http'] = '---://localhost:---'
            session.proxies['https'] = '---://localhost:---'

            session = _update_headers(session, -1)
            retries = Retry(total=60, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
            session.mount('https://', HTTPAdapter(max_retries=retries))
            since = query.since if query.since else 0

            cache = sorted(c for c in os.listdir('{0}/cache'.format(self.config['name'])) if
                           os.path.getsize('{0}/cache/{1}'.format(self.config['name'], c)) > 0)
            for c in cache:
                with FileReadBackwards('{0}/cache/{1}'.format(self.config['name'], c), encoding='utf-8') as frb:
                    recover_query = ndjson.loads(frb.readline())[0]['query']
                logger.info({'session': self.session_id, 'message': 'Recovering tweets from {0} to {1}'.format(
                    datetime.utcfromtimestamp(recover_query['since']).strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.utcfromtimestamp(recover_query['until']).strftime('%Y-%m-%d %H:%M:%S')
                )})
                query.set_parameter(recover_query)
                query_copy = deepcopy(query)
                res.append(
                    pool.apply_async(_consume_query, args=[query_copy, session, self.session_id, self.config['name']]))
                self.session_id += 1

            query.since = since

            old_tweets = sorted(t for t in os.listdir('{0}/tweets'.format(self.config['name'])) if
                                os.path.getsize('{0}/tweets/{1}'.format(self.config['name'], t)) > 0 and t.endswith('.ndjson'))
            if len(old_tweets) > 0:
                query.since, query.until = (int(i) for i in old_tweets[0].replace('.ndjson', '').split('_') if
                                            i.isnumeric())
                if query.since == since:
                    tweets = 0
                    tweets_files = os.listdir('{0}/tweets'.format(self.config['name']))
                    for file in tweets_files:
                        tweets += _raw_count('{0}/tweets/{1}'.format(self.config['name'], file))
                    logger.info('{0} tweets found in total'.format(tweets))
                    logger.info('DONE')
                    for r in res:
                        r.get()
                    return
                else:
                    query.until = query.since
                    query.since = since
            while True:
                sliced_until, sliced_since = _slice_interval(query, session, self.config['interval'])
                if not sliced_until and not sliced_since:
                    pool.close()
                    pool.join()
                    tweets = 0
                    tweets_files = os.listdir('{0}/tweets'.format(self.config['name']))
                    for file in tweets_files:
                        tweets += _raw_count('{0}/tweets/{1}'.format(self.config['name'], file))

                    logger.info('{0} tweets found in total'.format(tweets))
                    logger.info('DONE')
                    for r in res:
                        r.get()
                    break
                logger.info({'session': self.session_id, 'message': 'Found tweets from {0} to {1}'.format(
                    datetime.utcfromtimestamp(sliced_since).strftime('%Y-%m-%d %H:%M:%S'),
                    datetime.utcfromtimestamp(sliced_until).strftime('%Y-%m-%d %H:%M:%S')
                )})
                query.until = sliced_until
                query.since = sliced_since
                if query.since <= since:
                    query.since = since
                    query_copy = deepcopy(query)
                    res.append(
                        pool.apply_async(_consume_query, args=[query_copy, session, self.session_id, self.config['name']]))
                    self.session_id = self.session_id + 1
                    pool.close()
                    pool.join()

                    tweets = 0
                    tweets_files = os.listdir('{0}/tweets'.format(self.config['name']))
                    for file in tweets_files:
                        tweets += _raw_count('{0}/tweets/{1}'.format(self.config['name'], file))

                    logger.info('{0} tweets found in total'.format(tweets))
                    logger.info('DONE')
                    for r in res:
                        r.get()
                    return
                else:
                    query_copy = deepcopy(query)
                    res.append(
                        pool.apply_async(_consume_query, args=[query_copy, session, self.session_id, self.config['name']]))
                    self.session_id += 1
                if query.since != since:
                    query.since = since
                    query.until = sliced_since


def _update_headers(session, session_id):
    session.headers.update({
        'Connection': 'keep-alive',
        'authorization': 'Bearer ---------------------------------------------------------------------------'
                         '-----------------',
        'x-guest-token': _fetch_token(session_id),
        'x-twitter-active-user': 'yes',
        'User-Agent': generate_user_agent(device_type='desktop'),
        'Accept': '*/*',
        'Origin': 'https://twitter.com',
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


def _fetch_token(session_id):
    token = None
    token_url = 'https://twitter.com/'
    while not token:
        session = Session()

        session.proxies = {}
        session.proxies['http'] = '---://localhost:---'
        session.proxies['https'] = '---://localhost:---'

        session.headers.update({
            'User-Agent': generate_user_agent(device_type='desktop'),
            'x-csrf-token': _get_csrf_token(),
        })
        retries = Retry(total=60, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))
        request = session.prepare_request(Request('GET', token_url))
        response = session.send(request, timeout=12)
        if match := re.search(r'"gt=(\d+);', response.text):
            token = match.group(1)
        elif 'gt' in response.cookies:
            token = response.cookies['gt']
        else:
            logger.warning({'session': session_id, 'message': 'x-guest-token not found, waiting 10 seconds...'})
            time.sleep(10)
    return token


def _search_query(query, session, session_id, retries=30):
    if retries == 0:
        logger.error('MAX retires for query {0} -> since:{1} - until{0}'.format(query.query, query.since, query.until))
        return [], None
    params = query.generate_params()
    request = session.prepare_request(Request('GET', query.base_url, params=params, cookies={}))
    response = session.send(request, timeout=12)
    try:
        response_json = response.json()
    except (ValueError, AttributeError):
        logger.error('Value or attribute error for resp.json, stopping')
        return
    if 'errors' in response_json and retries > 0 or (response_json['globalObjects']['tweets'] == {}
                                                     and not response_json['timeline']['instructions']
                                                     [0]['addEntries']['entries'] == []):
        session = _update_headers(session, session_id)
        return _search_query(query, session, session_id, retries - 1)

    tweets = recompose_tweets(response_json)
    next_query = deepcopy(query)
    next_query.cursor = re.findall('"(scroll:.+?)",', response.text)[0]
    return tweets, next_query


def _slice_interval(query, session, interval):
    tweets = _search_query(query, session, -1)[0]
    if len(tweets) > 0:
        target = tweets[0]
        until = int(
            calendar.timegm(datetime.strptime(target['created_at'], '%a %b %d %H:%M:%S +0000 %Y').timetuple())) + 1
        since = until - 3600 * interval
        return until, since
    else:
        return None, None


def _consume_query(query, session, session_id, session_name):
    tweets_file = open('{0}/tweets/tweets_{1}_{2}.ndjson'.format(session_name, query.since, query.until), 'a+',
                       encoding='utf-8')
    tweets_writer = ndjson.writer(tweets_file, ensure_ascii=False)

    cache_file = open('{0}/cache/{1}_{2}'.format(session_name, query.since, query.until), 'a+',
                      encoding='utf-8')
    cache_writer = ndjson.writer(cache_file, ensure_ascii=False)

    old_cursor = query.cursor
    tmp_tweets, next_query = _search_query(query, session, session_id)
    cache_writer.writerow({'session': session_id, 'status': 'in_progress', 'query': {'cursor': next_query.cursor,
                           'since': next_query.since, 'until': next_query.until, 'q': next_query.query}})
    cache_file.flush()
    retries = 20
    while True:
        if len(tmp_tweets) == 0 and retries == 0:
            break
        if len(tmp_tweets) == 0:
            time.sleep(5)
            retries -= 1
            next_query.cursor = old_cursor
            tmp_tweets, next_query = _search_query(next_query, session, session_id)
        else:
            for t in tmp_tweets:
                tweets_writer.writerow(t)
                tweets_file.flush()
            cache_writer.writerow({'session': session_id, 'status': 'in_progress',
                                   'query': {'cursor': next_query.cursor, 'since': next_query.since,
                                             'until': next_query.until,
                                             'q': next_query.query}})
            cache_file.flush()
            old_cursor = next_query.cursor
            tmp_tweets, next_query = _search_query(next_query, session, session_id)
            retries = 20
    cache_file.close()
    os.remove('{0}/cache/{1}_{2}'.format(session_name, query.since, query.until))
    logger.info({'session': session_id, 'message': '{0} tweets found from {1} to {2}'.format(
        _raw_count('{0}/tweets/tweets_{1}_{2}.ndjson'.format(session_name, query.since, query.until)),
        datetime.utcfromtimestamp(query.since).strftime('%Y-%m-%d %H:%M:%S'),
        datetime.utcfromtimestamp(query.until).strftime('%Y-%m-%d %H:%M:%S'))})
    tweets_file.close()

    with open('{0}/tweets/tweets_{1}_{2}.ndjson'.format(session_name, query.since, query.until), 'rb') as f_in:
        with gzip.open('{0}/tweets/tweets_{1}_{2}.ndjson.gz'.format(session_name, query.since, query.until), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove('{0}/tweets/tweets_{1}_{2}.ndjson'.format(session_name, query.since, query.until))

def _raw_count(filename):
    f = open(filename, 'rb')
    bufgen = takewhile(lambda x: x, (f.raw.read(1024*1024) for _ in repeat(None)))
    return sum(buf.count(b'\n') for buf in bufgen)
