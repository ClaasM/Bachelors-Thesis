import tweepy
import csv
import itertools

# TODO remove this before pushing to github
consumer_key = "EJa95UqoYaD6Zme6BkeYLNgtS"
consumer_secret = "r1hvUD1s721K99HbRcFW9Pgr5JGovKsHt56CXSM2kdS5P3qXJX"
access_token = "1421459618-TMezTymHrnC8VdgVtyvauPiKrJpGmDcAgvYO0ZC"
access_token_secret = "zCwVoYbD8TSmDC3KJBTCGfuByIkA1YiNBVAs2oCRTvUG7"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

with open('../../data/interim/corpus.csv') as in_file:
    csv_reader = csv.reader(in_file, delimiter=',')
    with open('../../data/external/sanders.csv', 'w', newline='') as out_file:
        csv_writer = csv.writer(out_file, delimiter=',')
        # Go through the tweets in chunks of 100, since the lookup api can return 100 tweets at once.
        while True:
            chunk = tuple(itertools.islice(csv_reader, 100))
            if chunk:
                # Get the tweets from the API
                tweets = api.statuses_lookup([row[2] for row in chunk])
                # We don't even need to handle any rate limiting,
                # since the sanders dataset can be downloaded in one go
                for index, tweet in enumerate(tweets):
                    # write the original row plus the text
                    # add more details from the tweet as needed
                    # Strings should be escaped, since the csvWriter doesn't do that
                    csv_writer.writerow(chunk[index] + [repr(tweet.text)])
            else:
                # We're done, all chunks downloaded
                break
        out_file.close()
    in_file.close()
