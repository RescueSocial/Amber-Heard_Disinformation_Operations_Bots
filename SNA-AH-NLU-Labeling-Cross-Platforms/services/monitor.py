import requests
from datetime import datetime

SERVER_URL = "http://127.0.0.1:8000/"
def post_tweet(payload):
    try:
        headers = {'Authorization' : '(some auth code)', 'Accept' : 'text/plain', 'Content-Type' : 'application/json'}
        r = requests.post(SERVER_URL+'api/tweet', json=payload, headers=headers)
        print("request status code: ", r.status_code)
        print("method ", r.json()['method'])
        return r.json()
    except Exception as e:
        print(e)
        return {'method':'None'}

payload = {}
payload["what"] = 'I love Amber Heard becasue she is great women!'
payload["bot"] = 'twitterbot1'
payload["who"] = '@amberheardT'
payload["where"] = 'https://twitter.com'

post_tweet(payload)