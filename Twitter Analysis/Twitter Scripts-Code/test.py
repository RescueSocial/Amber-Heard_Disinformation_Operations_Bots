import os
from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import re
import time
from user_agent import generate_user_agent



def _get_csrf_token():
    prefix = b'CODEX'
    remainder = 32 // 2 - len(prefix)
    rem_bytes = os.urandom(remainder)
    return (prefix + rem_bytes).hex()



def main():
    token = None
    token_url = 'https://twitter.com/'
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
        print('NULL')
        return
    print(token)

if __name__ == '__main__':
    main()