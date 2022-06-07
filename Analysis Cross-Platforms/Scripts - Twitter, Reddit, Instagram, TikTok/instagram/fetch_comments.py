from datetime import datetime
import instaloader
import pickle
import os
import time
import sys
from instaloader.exceptions import TooManyRequestsException, BadResponseException, ConnectionException, QueryReturnedForbiddenException, QueryReturnedBadRequestException
from datetime import datetime
from requests import get
import traceback

pointer = 0


proxies1 = ['---------------------------------------------------------',
            '---------------------------------------------------------',
            '---------------------------------------------------------
            '---------------------------------------------------------',
            '---------------------------------------------------------',
           '---------------------------------------------------------']

proxies2 = ['---------------------------------------------------------',
            '---------------------------------------------------------',
            '---------------------------------------------------------',
            '---------------------------------------------------------',
            ]

proxies3 = ['---------------------------------------------------------',
            '---------------------------------------------------------'
            ]

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
]

credentials1 = [('-------------','-------------'), ('-------------','-------------'), ('-------------','-------------'), ('-------------','-------------'), ('-------------','-------------'), ('-------------','-------------')]
credentials2 = [('-------------','-------------'), ('-------------','-------------'), ('-------------','-------------'), ('--------------','-------------')]
credentials3 = [('-------------','-------------'), ('-------------','-------------')]

proxies = proxies1 + proxies2 + proxies3
credentials = credentials1 + credentials2 + credentials3

os.environ['http_proxy'] = proxies[pointer]
os.environ['HTTP_PROXY'] = proxies[pointer]
os.environ['https_proxy'] = proxies[pointer]
os.environ['HTTPS_PROXY'] = proxies[pointer]

# print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Logging in using account ' + credentials[pointer][0])


zero_success = False
while not zero_success:
    try:
        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Account ' + credentials[pointer][0] + ' in rate limit', flush=True)
        pointer = (pointer + 1) % len(proxies)
        if 'L' in locals():
            del L
        time.sleep(5)
        os.environ['http_proxy'] = proxies[pointer]
        os.environ['HTTP_PROXY'] = proxies[pointer]
        os.environ['https_proxy'] = proxies[pointer]
        os.environ['HTTPS_PROXY'] = proxies[pointer]

        ip = get('https://api.ipify.org').text

        L = instaloader.Instaloader(filename_pattern='{mediaid}', quiet=True, download_pictures=False,
                                    download_videos=False, download_video_thumbnails=False,
                                    user_agent=user_agent_list[0],
                                    download_comments=True)
        if os.path.exists(credentials[pointer][0]):
            print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Loading session for account ' +
                  credentials[pointer][0] + ' IP: ' + ip, flush=True)
            L.load_session_from_file(credentials[pointer][0], credentials[pointer][0])
        else:
            print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Logging in using account ' +
                  credentials[pointer][0] + ' IP: ' + ip, flush=True)
            L.login(credentials[pointer][0],credentials[pointer][1])
            L.save_session_to_file(credentials[pointer][0])
            print('[' + datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S") + '] ' + 'Session saved', flush=True)

        zero_success = True
    except ConnectionException as e:
        zero_success = False
        time.sleep(5)

# L = instaloader.Instaloader(filename_pattern='{mediaid}', quiet=True, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', download_comments=True)
#
# L.login(credentials[pointer][0], credentials[pointer][1])

with open('posts/' + str(0) + '.obj', 'rb') as inpt:  # Overwrites any existing file.
    posts = pickle.load(inpt)

for post in posts:
    if os.path.exists('data/' + str(post.mediaid) + '.txt'):
        print('Post ' + str(post.mediaid) + ' already gathered')
    else:
        success = False
        while not success:
            try:
                print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Gathering post ' + post.shortcode + ' (mediaid: ' + str(post.mediaid) + ')', flush=True)
                L.download_post(post, target='data')
                success = True
                sys.stdout.flush()
                time.sleep(2)
            except (TooManyRequestsException, ConnectionException, BadResponseException, QueryReturnedBadRequestException) as e:
                print(traceback.format_exc(), flush=True)
                second_success = False
                while not second_success:
                    try:
                        print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Account ' + credentials[pointer][0] + ' in rate limit', flush=True)
                        pointer = (pointer + 1) % len(proxies)
                        del L
                        time.sleep(5)
                        os.environ['http_proxy'] = proxies[pointer]
                        os.environ['HTTP_PROXY'] = proxies[pointer]
                        os.environ['https_proxy'] = proxies[pointer]
                        os.environ['HTTPS_PROXY'] = proxies[pointer]

                        ip = get('https://api.ipify.org').text

                        L = instaloader.Instaloader(filename_pattern='{mediaid}', quiet=True, download_pictures=False, download_videos=False, download_video_thumbnails=False,
                                                    user_agent=user_agent_list[0],
                                                    download_comments=True)
                        if os.path.exists(credentials[pointer][0]):
                            print('[' + datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S") + '] ' + 'Loading session for account ' +
                                  credentials[pointer][0] + ' IP: ' + ip, flush=True)
                            L.load_session_from_file(credentials[pointer][0], credentials[pointer][0])
                        else:
                            print('[' + datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S") + '] ' + 'Logging in using account ' +
                                  credentials[pointer][0] + ' IP: ' + ip, flush=True)
                            L.login(credentials[pointer][0], credentials[pointer][1])
                            L.save_session_to_file(credentials[pointer][0])
                            print('[' + datetime.now().strftime(
                                "%d/%m/%Y %H:%M:%S") + '] ' + 'Session saved', flush=True)
                        second_success = True
                    except ConnectionException as e:
                        print(traceback.format_exc(), flush=True)
                        second_success = False
                        time.sleep(5)
            except ConnectionException as e:
                print(traceback.format_exc(), flush=True)
                time.sleep(5)
                pass
            except (QueryReturnedForbiddenException) as e:
                print(traceback.format_exc(), flush=True)
                success = True
                print('[' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '] ' + 'Post ' + post.shortcode + ' skipped (mediaid: ' + str(post.mediaid) + ')' , flush=True)

# START = datetime(2021, 5, 28)
# END = datetime(2021, 5, 30)
# HASHTAG = "amberheard"
# GraphQL_Hash = "9b498c08113f1e09617a1703c22b2f32"
#
#
#
#
# post_iterator = instaloader.NodeIterator(
#     L.context, GraphQL_Hash,
#     lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
#     lambda n: instaloader.Post(L.context, n),
#     {'tag_name': HASHTAG},
#     f"https://www.instagram.com/explore/tags/{HASHTAG}/"
# )
#
# if os.path.isfile('{HASHTAG}.pkl'):
#     with open(f'{HASHTAG}.pkl', 'rb') as resumefile:
#         resumeint = pickle.load(resumefile)
#         post_iterator.thaw(resumeint)
#
# def gen(posts):
#     for post in posts:
#         print(post.date)
#         yield post
#         # print(post.date)
#         # if post.date > start and post.date > end:
#         #     pass
#         # elif post.date >= start and post.date <= end:
#         #     yield post
#         # elif post.date <= start:
#         #     break
#
#
# iter = 0
# posts = []
#
# # for post in gen(posts=post_iterator):
# #     posts.append(post)
# #     if len(posts) == 100000:
# #         with open('posts/' + str(iter) + '.obj', 'wb') as outp:  # Overwrites any existing file.
# #             pickle.dump(posts, outp, pickle.HIGHEST_PROTOCOL)
# #         posts = []
# #         iter += 1
#
# try:
#     for post in post_iterator:
#         print(post.date, flush=True)
#         posts.append(post)
#         if len(posts) == 100000:
#             with open('posts/' + str(iter) + '.obj', 'wb') as outp:  # Overwrites any existing file.
#                 pickle.dump(posts, outp, pickle.HIGHEST_PROTOCOL)
#             posts = []
#             iter += 1
# except:
#     iteratorfreeze = post_iterator.freeze()
#     with open(f'{HASHTAG}.pkl', 'wb') as resumefile:
#         pickle.dump(iteratorfreeze, resumefile)