BASE_URL = 'https://twitter.com/i/api/2/timeline/conversation/{0}.json'

class Query:
    def __init__(self, conversation = ''):
        self.conversation = conversation
        self.base_url = BASE_URL.format(conversation)
        self.cursor = None

    def set_parameter(self, conversation):
        self.conversation = conversation
        self.base_url = BASE_URL.format(conversation)

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
            'referrer': 'tweet',
            'count': '20',
            'include_ext_has_birdwatch_notes': 'false',
            'ext': 'mediaStats,highlightedLabel',
        }
        if self.cursor:
            params['cursor'] = self.cursor
        # query = '&'.join('%s=%s' % (k, v) for k, v in params.items())
        return params
