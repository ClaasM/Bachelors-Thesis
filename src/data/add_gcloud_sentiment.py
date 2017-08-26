import csv
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

"""
This script reads all hydrated tweets and sends them to the gcloud sentiment analysis API.
The results are written to a file.
It makes sense to run the analysis once and save the result since the API is not free.
"""

# Set the path to the credentials downloaded from the google api console
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../google.access.json'

with open('../../data/interim/sanders_hydrated.csv') as csv_file:
    iterator = csv.reader(csv_file, delimiter=',')
    # Perform analysis on all tweets and write to file
    client = language.LanguageServiceClient()
    with open('../../data/interim/sanders_gcloud.csv', 'w', newline='') as out_file:
        # Quote everything, just like the in_file
        csv_writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_ALL)
        for tweet in iterator:
            text = tweet[2]
            # Create the document from the tweet
            document = types.Document(
                content=text,
                # PLAIN_TEXT or HTML
                type=enums.Document.Type.PLAIN_TEXT)
            # Analyze the sentiment
            try:
                annotations = client.analyze_sentiment(document=document)
                # Write the results to the out file
                csv_writer.writerow(tweet + [annotations.document_sentiment.score,
                                             annotations.document_sentiment.magnitude])
            except:
                # Write the tweet and an indicator that it didn't work
                # This is mainly the case if a tweet is in a language the API doesn't support
                csv_writer.writerow(tweet + ["N/A", "N/A"])

        out_file.close()
