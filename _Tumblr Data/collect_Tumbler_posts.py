from tumblpy import Tumblpy
import pandas as pd
import os
from os import listdir


t= Tumblpy(
    '**************************************************',
    '**************************************************',
    '**************************************************',
    '**************************************************'
)

def get_posts(blog_url, limit_pages=40, start_offset = 1):
        """
        Gets a list of posts from a particular blog
        :param blog_url: a string, the blogname you want to look up posts
                         for. eg: codingjester.tumblr.com
        :param post_type:  the type of posts you want returned, e.g. video. If omitted returns all post types.
        :param limit: an int, the number of likes you want returned
        :param offset: an int, the blog you want to start at, for pagination.
        :returns: A dict created from the JSON response
        """
        offset = start_offset
        all_posts = pd.DataFrame()
        for i in range(limit_pages):
            posts_all_data = t.posts(blog_url, kwargs={'limit': '50', 'offset': offset})
            print(offset, ', Remain pages =', limit_pages-i)
            offset += 50
            posts = pd.DataFrame(posts_all_data['posts'])
            all_posts = all_posts.append(posts)
        blog_name = blog_url.split('//')[1].split('.')[0]
        all_posts.to_csv('Tumblr_{}_posts_from{}to{}.csv'.format(blog_name, start_offset, offset-1), index=None)
        return print('Done')

get_posts(blog_url='<blog_url>', limit_pages=1, start_offset=1)