from datetime import datetime
import instaloader
import pickle
import os

proxy = '-------------------------------------------'

os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

L = instaloader.Instaloader()

L.login("---------------", "--------------")

START = datetime(2021, 5, 28)
END = datetime(2021, 5, 30)
HASHTAG = "amberheard"
GraphQL_Hash = "9b498c08113f1e09617a1703c22b2f32"




post_iterator = instaloader.NodeIterator(
    L.context, GraphQL_Hash,
    lambda d: d['data']['hashtag']['edge_hashtag_to_media'],
    lambda n: instaloader.Post(L.context, n),
    {'tag_name': HASHTAG},
    f"https://www.instagram.com/explore/tags/{HASHTAG}/"
)

if os.path.isfile('{HASHTAG}.pkl'):
    with open(f'{HASHTAG}.pkl', 'rb') as resumefile:
        resumeint = pickle.load(resumefile)
        post_iterator.thaw(resumeint)

def gen(posts):
    for post in posts:
        print(post.date)
        yield post
        # print(post.date)
        # if post.date > start and post.date > end:
        #     pass
        # elif post.date >= start and post.date <= end:
        #     yield post
        # elif post.date <= start:
        #     break


iter = 0
posts = []

# for post in gen(posts=post_iterator):
#     posts.append(post)
#     if len(posts) == 100000:
#         with open('posts/' + str(iter) + '.obj', 'wb') as outp:  # Overwrites any existing file.
#             pickle.dump(posts, outp, pickle.HIGHEST_PROTOCOL)
#         posts = []
#         iter += 1

try:
    for post in post_iterator:
        print(post.date, flush=True)
        posts.append(post)
        if len(posts) == 100000:
            with open('posts/' + str(iter) + '.obj', 'wb') as outp:  # Overwrites any existing file.
                pickle.dump(posts, outp, pickle.HIGHEST_PROTOCOL)
            posts = []
            iter += 1
except:
    iteratorfreeze = post_iterator.freeze()
    with open(f'{HASHTAG}.pkl', 'wb') as resumefile:
        pickle.dump(iteratorfreeze, resumefile)