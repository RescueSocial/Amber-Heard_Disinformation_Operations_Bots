import json
import argparse
import requests
import pandas as pd
import time
import os


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def query(headers, params, search_url):
    response = requests.request("GET", search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def query_loop(headers, query_params, pagination_token, search_url):
    query_params["next_token"] = pagination_token
    response = requests.request("GET", search_url, headers=headers, params=query_params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


bearer_token = "----------------------------------------------------------------------------------------------------------"

query_params = {
    # 'start_time': '2016-10-11T00:00:00Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    # 'end_time': '2016-11-09T00:00:00Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    # 'end_time': '2016-10-16T11:50:00.000Z',  # YOUR START DATE IN YYYY-MM-DDT00:00:00Z Format
    'tweet.fields': 'author_id,created_at,in_reply_to_user_id,lang,public_metrics,referenced_tweets,source,entities',
    'max_results': 100,  # This is the max results admited by API endpoint
    'expansions': 'author_id,referenced_tweets.id.author_id,referenced_tweets.id,in_reply_to_user_id',
    #    'media.fields': 'duration_ms,media_key,url,type,public_metrics',
    'user.fields': 'id,username,created_at,description,profile_image_url,public_metrics,location,url'
}

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-t', '--token', type=str, help='')
    args = parser.parse_args()

    bearer_token = args.token

    df = pd.read_csv('timeline.csv')
    tweet_ids = list(df['id'].values)

    for twt_id in tweet_ids:
        twt_id = str(twt_id)
        # twt_id = str(1121826290464641024)
        if os.path.exists('quotes/{0}.json'.format(twt_id)):
            print('{0} already done, skipping'.format(twt_id))
            continue
        print(twt_id)
        original_tweet = None
        objs = []
        headers = create_headers(bearer_token)
        search_url = "https://api.twitter.com/2/tweets/{0}/quote_tweets".format(twt_id)
        next_token = None

        if next_token is not None:
            query_params['pagination_token'] = next_token

        first = True
        data_rt = []

        while True:
            time.sleep(12.1)
            # try:
            json_response = query(headers, query_params, search_url)
            if 'data' not in json_response:
                print('Break')
                break
            if 'includes' not in json_response:
                print('Break')
                break
            if 'tweets' not in json_response['includes']:
                print('Break')
                break
            if original_tweet is None:
                for tweet in json_response['includes']['tweets']:
                    if tweet['id'] == twt_id:
                        original_tweet = tweet
                        print(original_tweet)
                        break
                for author in json_response['includes']['users']:
                    if author['id'] == '807003567605227520':
                        original_tweet['author'] = author
            for tweet in json_response['data']:
                tweet['quoted_tweet'] = original_tweet
                for author in json_response['includes']['users']:
                    if author['id'] == tweet['author_id']:
                        tweet['author'] = author
                objs.append(tweet)

            # df = pd.json_normalize(json_response['data'])
            # df = df.reindex(columns=['id', 'author_id', 'created_at', 'text', 'lang', 'public_metrics.retweet_count',
            #                          'public_metrics.reply_count', 'public_metrics.like_count',
            #                          'public_metrics.quote_count',
            #                          'in_reply_to_user_id', 'geo.place_id', 'geo.coordinates.type',
            #                          'geo.coordinates.coordinates'])
            # if os.path.exists('data/common_hashtags.csv'):
            #     df.to_csv('data/common_hashtags.csv', mode='a', encoding='utf-8', index=False, header=None)
            # else:
            #     df.to_csv('data/common_hashtags.csv', encoding='utf-8', index=False)
            #     first = False
            # data_rt.append(json_response)
        # except Exception as e:
        #     print(e)
        #     pass
            print(len(objs))
            if 'next_token' in json_response['meta']:
                next_token = json_response['meta']['next_token']
                query_params['pagination_token'] = next_token
            else:
                query_params['pagination_token'] = None
                with open('quotes/{0}.json'.format(twt_id), 'w') as outfile:
                    json.dump(objs, outfile)
                print()
                break

if __name__ == '__main__':
    main()
