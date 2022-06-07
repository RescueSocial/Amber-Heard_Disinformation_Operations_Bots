BASE_URL = 'https://api.twitter.com/2/search/adaptive.json'

class Query:
    def __init__(self, config):
        self.query = config['query']
        self.since = config['since']
        self.until = config['until']

        self.base_url = BASE_URL
        self.cursor = None

    def set_parameter(self, query):
        self.query = query['q']
        self.since = query['since']
        self.until = query['until']
        self.cursor = query['cursor']


    def generate_params(self):
        params = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'skip_status': '1',
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': 'true',
            'include_quote_count': 'true',
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_entities': 'true',
            'include_user_entities': 'true',
            'include_ext_media_color': 'true',
            'include_ext_media_availability': 'true',
            'send_error_codes': 'true',
            'simple_quoted_tweet': 'true',
            'tweet_search_mode': 'live',
            'count': '20',
            'query_source': 'typed_query',
            'pc': '1',
            'spelling_corrections': '1',
            'ext': 'mediaStats,highlightedLabel',
        }

        q = self.query
        if self.since:
            q += ' since:{0}'.format(self.since)
        if self.until:
            q += ' until:{0}'.format(self.until)
        params['q'] = q
        params['cursor'] = '' if not self.cursor else self.cursor
        # query = '&'.join('%s=%s' % (k, v) for k, v in params.items())
        return params
