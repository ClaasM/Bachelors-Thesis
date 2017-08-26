import tweepy
import csv
import itertools
import json

"""
This script is used to get the tweets from the Sanders dataset.
Existing scripts were too slow and didn't take full advantage of the API.
The dataset is not hydrated yet because that would violate twitters TOS.
"""

with open('../../twitter.access.json') as access_info_file:
    access_info = json.load(access_info_file)
    auth = tweepy.OAuthHandler(access_info['consumer_key'], access_info['consumer_secret'])
    auth.set_access_token(access_info['access_token'], access_info['access_token_secret'])
    api = tweepy.API(auth)
    with open('../../data/external/sanders.csv') as in_file:
        csv_reader = csv.reader(in_file, delimiter=',')
        with open('../../data/interim/sanders_hydrated.csv', 'w') as out_file:
            # Quote everything, just like the in_file
            csv_writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_ALL)
            # Go through the tweets in chunks of 100, since the lookup api can return 100 tweets at once.
            while True:
                chunk = tuple(itertools.islice(csv_reader, 100))
                if chunk:
                    # Get the tweets from the API
                    tweets = api.statuses_lookup([id for (topic, sentiment, id) in chunk])
                    # We don't even need to handle any rate limiting,
                    # since the sanders dataset can be downloaded in one go
                    for index, tweet in enumerate(tweets):
                        # write the original row plus the text
                        # add more details from the tweet as needed
                        # The csv file contains line breaks, but the python csv reader handles them correctly
                        csv_writer.writerow(chunk[index] + [tweet.text])
                else:
                    # We're done, all chunks downloaded
                    break
            out_file.close()
        in_file.close()
print("Done!")
