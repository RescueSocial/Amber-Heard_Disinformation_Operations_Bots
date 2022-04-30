import gzip
import ndjson
import glob
from elasticsearch import Elasticsearch

def main():
	es = Elasticsearch()
	i = 0
	folder = '/scripts/result/'
	days_files = glob.glob(folder + '*/')
	for day_files in days_files:
		tweets_files = glob.glob(day_files + 'tweets/*.gz')
		for tweets_file in tweets_files:
			# print(tweets_file)
			with gzip.open(tweets_file, 'r') as fin:
				data = ndjson.load(fin)
				for document in data:
					res = es.index(index='tweets', body=document)
					i += 1
					if i % 1000 == 0:
						print(i)

if __name__ == '__main__':
    main()

