def recompose_tweets(response):
    timeline = response['timeline']['instructions'][0]['addEntries']['entries']
    tweets = response['globalObjects']['tweets']
    users = response['globalObjects']['users']

    recomposed_tweets = []
    for entry in timeline:
        if 'item' in entry['content'] and entry['entryId'].startswith('sq-I-t-'):
            if 'tweet' in entry['content']['item']['content']:
                t = entry['content']['item']['content']['tweet']
            elif 'tombstone' in entry['content']['item']['content']:
                t = entry['content']['item']['content']['tombstone']['tweet']
            if 'promotedMetadata' in t:
                continue

            tweet_id = t['id']
            tweet = tweets[tweet_id]
            tweet['user'] = users[tweet['user_id_str']]

            if 'retweeted_status_id' in tweet:
                tweet['retweeted_status'] = tweets[tweet['retweeted_status_id_str']]
                tweet['retweeted_status']['user'] = users[tweet['retweeted_status']['user_id_str']]

            if 'quoted_status_id' in tweet:
                tweet['quoted_status'] = tweets[tweet['quoted_status_id_str']]
                tweet['quoted_status']['user'] = users[tweet['quoted_status']['user_id_str']]

            recomposed_tweets.append(tweet)
    return recomposed_tweets
