def recompose_tweets(response):
    if len(response['timeline']['instructions']) == 0:
        return [], '', []
    show_more = False
    try:
        timeline = response['timeline']['instructions'][0]['addEntries']['entries']
    except KeyError:
        try:
            timeline = response['timeline']['instructions'][0]['addToModule']['moduleItems']
            show_more = True
        except KeyError:
            return [], '', []
    tweets = response['globalObjects']['tweets']
    users = response['globalObjects']['users']

    recomposed_tweets = []
    bottom_cursor = ''
    mores = []
    for entry in timeline:
        if show_more:
            if entry['entryId'].startswith('tweet-') and 'tweet' in entry['item']['content']:
                tweet_id = entry['item']['content']['tweet']['id']
                if tweet_id not in tweets:
                    continue
                tweet = tweets[tweet_id]
                tweet['user'] = users[tweet['user_id_str']]

                if 'retweeted_status_id' in tweet:
                    tweet['retweeted_status'] = tweets[tweet['retweeted_status_id_str']]
                    tweet['retweeted_status']['user'] = users[tweet['retweeted_status']['user_id_str']]

                if 'quoted_status_id' in tweet:
                    tweet['quoted_status'] = tweets[tweet['quoted_status_id_str']]
                    tweet['quoted_status']['user'] = users[tweet['quoted_status']['user_id_str']]

                recomposed_tweets.append(tweet)
                if tweet['reply_count'] > 0:
                    mores.append(tweet_id)
            # elif entry['entryId'].endswith('-show_more_cursor'):
            #     mores.append(entry['item']['content']['timelineCursor']['value'])
        else:
            if entry['entryId'].startswith('conversationThread-'):
                for sub_entry in entry['content']['timelineModule']['items']:
                    if sub_entry['entryId'].startswith('tweet-') and 'tweet' in sub_entry['item']['content']:

                        tweet_id = sub_entry['item']['content']['tweet']['id']
                        if tweet_id not in tweets:
                            continue
                        tweet = tweets[tweet_id]
                        tweet['user'] = users[tweet['user_id_str']]

                        if 'retweeted_status_id' in tweet:
                            tweet['retweeted_status'] = tweets[tweet['retweeted_status_id_str']]
                            tweet['retweeted_status']['user'] = users[tweet['retweeted_status']['user_id_str']]

                        if 'quoted_status_id' in tweet:
                            tweet['quoted_status'] = tweets[tweet['quoted_status_id_str']]
                            tweet['quoted_status']['user'] = users[tweet['quoted_status']['user_id_str']]

                        recomposed_tweets.append(tweet)
                        if tweet['reply_count'] > 0:
                            mores.append(tweet_id)
                    # elif sub_entry['entryId'].endswith('-show_more_cursor'):
                    #     mores.append(sub_entry['item']['content']['timelineCursor']['value'])
            elif 'item' in entry['content'] and entry['entryId'].startswith('tweet-'):
                if 'promotedMetadata' in entry['content']['item']['content']['tweet']:
                    continue

                tweet_id = entry['content']['item']['content']['tweet']['id']
                if tweet_id not in tweets:
                    continue
                tweet = tweets[tweet_id]
                tweet['user'] = users[tweet['user_id_str']]

                if 'retweeted_status_id' in tweet:
                    tweet['retweeted_status'] = tweets[tweet['retweeted_status_id_str']]
                    tweet['retweeted_status']['user'] = users[tweet['retweeted_status']['user_id_str']]

                if 'quoted_status_id' in tweet:
                    tweet['quoted_status'] = tweets[tweet['quoted_status_id_str']]
                    tweet['quoted_status']['user'] = users[tweet['quoted_status']['user_id_str']]

                recomposed_tweets.append(tweet)
                if tweet['reply_count'] > 0:
                    mores.append(tweet_id)

            elif entry['entryId'].startswith('cursor-bottom-') or entry['entryId'].startswith('cursor-showMoreThreads'):
                bottom_cursor = entry['content']['operation']['cursor']['value']
    return recomposed_tweets, bottom_cursor, mores
