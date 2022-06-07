import praw
import time
import requests
from prawcore.exceptions import Forbidden, NotFound
from pprint import pprint
from datetime import datetime
from elasticsearch import Elasticsearch
import re

from textblob import TextBlob
# VADER can be accessed by the NLTK library.
import nltk
# Download the VADAR tool and access it through the NLTK library.
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# api = PushshiftAPI()
#
# gen = api.search_submissions(limit=100)
# results = list(gen)



reddit = praw.Reddit(
    client_id='--------',
    client_secret='-----------------',
    password='---------------',
    user_agent='testscript by u/fakebot3',
    username='-----------',
)

def text_blob_sentiment(review):
    analysis = TextBlob(review)
    if analysis.sentiment.polarity >= 0.0001:
        if analysis.sentiment.polarity > 0:
            return 'Positive'

    elif analysis.sentiment.polarity <= -0.0001:
        if analysis.sentiment.polarity <= 0:
            return 'Negative'
    else:
        return 'Neutral'

sia = SentimentIntensityAnalyzer()
def nltk_sentiment(review):
    vs = sia.polarity_scores(review)
    if not vs['neg'] > 0.05:
        if vs['pos'] - vs['neg'] > 0:
            return 'Positive'
        else:
            return 'Neutral'

    elif not vs['pos'] > 0.05:
        if vs['pos'] - vs['neg'] <= 0:
            return 'Negative'
        else:
            return 'Neutral'
    else:
        return 'Neutral'

def submissions_pushshift_praw(start=None, end=None, limit=100, extra_query=''):
    '''
    A simple function that returns a list of PRAW submission objects during a particular period from a defined sub.
    This function serves as a replacement for the now deprecated PRAW `submissions()` method.

    :param subreddit: A subreddit name to fetch submissions from.
    :param start: A Unix time integer. Posts fetched will be AFTER this time. (default: None)
    :param end: A Unix time integer. Posts fetched will be BEFORE this time. (default: None)
    :param limit: There needs to be a defined limit of results (default: 100), or Pushshift will return only 25.
    :param extra_query: A query string is optional. If an extra_query string is not supplied,
                        the function will just grab everything from the defined time period. (default: empty string)

    Submissions are yielded newest first.

    For more information on PRAW, see: https://github.com/praw-dev/praw
    For more information on Pushshift, see: https://github.com/pushshift/api
    '''
    matching_praw_submissions = []

    # Default time values if none are defined (credit to u/bboe's PRAW `submissions()` for this section)
    utc_offset = 28800
    now = int(time.time())
    start = max(int(start) + utc_offset if start else 0, 0)
    end = min(int(end) if end else now, now) + utc_offset
    search_link = 'https://api.pushshift.io/reddit/search/submission/?q={}&after={}&before={}&subreddit=&author=&aggs=&metadata=true&frequency=hour&advanced=false&sort=desc&domain=&sort_type=num_comments&size={}'
    # Format our search link properly.
    # search_link = ('https://api.pushshift.io/reddit/submission/search/'
    #                '?subreddit={}&after={}&before={}&sort_type=score&sort=asc&limit={}&q={}')
    # search_link = search_link.format(subreddit, start, end, limit, extra_query)
    search_link = search_link.format(extra_query, start, end, limit)

    # Get the data from Pushshift as JSON.
    success = False
    while not success:
        try:
            retrieved_data = requests.get(search_link)
            returned_submissions = retrieved_data.json()['data']
            success = True
        except:
            success = False

    # Iterate over the returned submissions to convert them to PRAW submission objects.
    for submission in returned_submissions:
        # Take the ID, fetch the PRAW submission object, and append to our list
        praw_submission = reddit.submission(id=submission['id'])

        matching_praw_submissions.append(praw_submission)

    # Return all PRAW submissions that were obtained.
    return matching_praw_submissions



# for submission in submissions_pushshift_praw('languagelearning', 1478532000, 1478542000):
#         print(submission.title)


# submission = reddit.submission(url='https://www.reddit.com/r/entertainment/comments/nxv4ly/fans_once_again_call_for_amber_heard_to_be_fired/')
# print(submission.id)
#
# print(submission.title)

es = Elasticsearch()


until = 1624752000


while True:
    since = until - (60 * 60 * 24)

    for submission in submissions_pushshift_praw(since, until, 100000, 'amber%20heard'):
        try:
            test = submission.title
        except (Forbidden, NotFound):
            continue

        try:
            author_name = submission.author.name
            author = {'name': author_name,
                'created_at': datetime.utcfromtimestamp(submission.author.created_utc).strftime('%a %b %d %H:%M:%S +0000 %Y'),
                'has_verified_email': submission.author.has_verified_email,
                'is_employee': submission.author.is_employee,
                'is_mod': submission.author.is_mod,
                'is_gold': submission.author.is_gold}
        except (Forbidden, NotFound,AttributeError):
            author_name = '-banned-'
            author = {'name': author_name,
                'created_at': None,
                'has_verified_email': None,
                'is_employee': None,
                'is_mod': None,
                'is_gold': None}
        if 'amber heard' not in submission.title.lower():
            continue
        print(datetime.utcfromtimestamp(submission.created_utc).strftime('%a %b %d %H:%M:%S +0000 %Y'))

        urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', submission.title)

        urls_objects = []
        for url in urls:
            urls_objects.append({'display_url': url})


        document = {
            'id': submission.id,
            'name': submission.name,
            'permalink': submission.permalink,
            'text': submission.title,
            'parent_id': '',
            'subreddit': submission.subreddit_name_prefixed,
            'author': author,
            'created_at': datetime.utcfromtimestamp(submission.created_utc).strftime('%a %b %d %H:%M:%S +0000 %Y'),
            'entities': {
                'urls': urls_objects
            },
            'sentiment_blob': text_blob_sentiment(submission.title),
            'sentiment_nltk': nltk_sentiment(submission.title)
        }
        res = es.index(index='reddit', body=document)


        success = False
        while not success:
            try:
                submission.comments.replace_more(limit=None)
                success = True
            except:
                success = False

        for comment in submission.comments.list():

            try:
                author_name = comment.author.name
                author = {'name': author_name,
                          'created_at': datetime.utcfromtimestamp(submission.author.created_utc).strftime(
                              '%a %b %d %H:%M:%S +0000 %Y'),
                          'has_verified_email': submission.author.has_verified_email,
                          'is_employee': submission.author.is_employee,
                          'is_mod': submission.author.is_mod,
                          'is_gold': submission.author.is_gold}
            except (Forbidden, NotFound, AttributeError):
                author_name = '-banned-'
                author = {'name': author_name,
                          'created_at': None,
                          'has_verified_email': None,
                          'is_employee': None,
                          'is_mod': None,
                          'is_gold': None}

            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', comment.body)

            urls_objects = []
            for url in urls:
                urls_objects.append({'display_url': url})

            document = {
                'id': comment.id,
                'name': comment.name,
                'permalink': comment.permalink,
                'text': comment.body,
                'parent_id': comment.parent_id,
                'subreddit': comment.subreddit_name_prefixed,
                'author': author,
                'created_at': datetime.utcfromtimestamp(comment.created_utc).strftime('%a %b %d %H:%M:%S +0000 %Y'),
                'entities': {
                        'urls': urls_objects
                    },
                'sentiment_blob': text_blob_sentiment(comment.body),
                'sentiment_nltk': nltk_sentiment(comment.body)
            }
            res = es.index(index='reddit', body=document)

    until = since

#nohup python3 /scripts/reddit/scraper.py > log2.out 2>&1 &