import pandas as pd
import os
import glob


def splitcsv(filename):
    count = 0
    for i,chunk in enumerate(pd.read_csv(filename, chunksize=50000)):
        count = count + 1
        chunk.to_csv('twitter_chunk{}.csv'.format(i), index=False)
        print(count)

def mergecsv(extension):
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # export to csv
    combined_csv.to_csv("combinedtwitter_csv.csv", index=False, encoding='utf-8-sig')

#filename = 'C:/Users/USER PC/PycharmProjects/twitter/part3_tweets_new_2021.csv'
#splitcsv(filename)

extension = 'csv'
mergecsv(extension)

