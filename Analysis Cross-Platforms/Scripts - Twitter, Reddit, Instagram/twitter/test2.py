import subprocess

token = None
while not token:
        # session = Session()

        # session.proxies = {}
        # session.proxies['http'] = '---://localhost:---'
        # session.proxies['https'] = '---://localhost:---'

        # session.headers.update({
        #     'User-Agent': generate_user_agent(device_type='desktop'),
        #     'x-csrf-token': _get_csrf_token(),
        # })
        # retries = Retry(total=60, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
        # session.mount('https://', HTTPAdapter(max_retries=retries))
        # request = session.prepare_request(Request('GET', token_url))
        # response = session.send(request, timeout=12)
    token = subprocess.run(['python3', '/scripts/test.py'], stdout=subprocess.PIPE)
    token = token.stdout.decode('utf-8').rstrip('\n')
    if token == 'NULL':
        token = None
        logger.warning({'session': session_id, 'message': 'x-guest-token not found, waiting 10 seconds...'})
        time.sleep(10)            
print(token)
