import argparse
from tweeper import Tweeper
import logging
import json
import os
FOLDER = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='Input type', dest='type')
commandline_parser = subparsers.add_parser('cli', help='Parameters by command line')

commandline_parser.add_argument('-q', '--query', type=str,
                                help='Query for the search')
commandline_parser.add_argument('--since', type=int, default=None,
                                help='Lower temporal bound (for example 2018-12-13 or 1544659200')
commandline_parser.add_argument('--until', type=int, default=None,
                                help='Upper temporal bound (for example 2018-12-13 or 1544659200)')
# commandline_parser.add_argument('--lang', type=int, default=None,
#                                 help='Scraper tweets in a specific language')
# commandline_parser.add_argument('--retweets', action='store_true',
#                                 help='Include retweets ()')
# commandline_parser.add_argument('--replies', action='store_true',
#                                 help='Include replies')
# commandline_parser.add_argument('--media', action='store_true',
#                                 help='Scrape only tweets containing images or videos')
# commandline_parser.add_argument('--images', action='store_true',
#                                 help='Scrape only tweets containing images')
# commandline_parser.add_argument('--videos', action='store_true',
#                                 help='Scrape only tweets containing videos')
# commandline_parser.add_argument('--links', action='store_true',
#                                 help='Scrape only tweets containing links')
# commandline_parser.add_argument('--verified', action='store_true',
#                                 help='Scrape only tweets from verified users')
# commandline_parser.add_argument('--limit', type=int, default=-1,
#                                 help='Max number of tweets to scrape')
# commandline_parser.add_argument('-i', '--interval', type=int, default=24,
#                                 help='hours interval for scraping (default 24h)')
# commandline_parser.add_argument('--parallel', action='store_true',
#                                 help='for parallel scraping')
# commandline_parser.add_argument('-o', '--output', type=str, default='tweets.json',
#                                 help='JSON file to store the tweets')

file_parser = subparsers.add_parser('config', help='Parameters by config file')
file_parser.add_argument('-f', '--file', type=str, help='Name of the config file')
args = parser.parse_args()


def main():
    if args.type == 'cli':
        config = vars(args)
    else:
        config = json.load(open(args.file))

    twpr = Tweeper(config)
    twpr.get_tweets()

if __name__ == "__main__":
    main()
