'''
Python module that

1) Extracts Data From the MongoDB database
- Connect to the database
- Query the data

2) Transforms the data
- Perform sentiment analysis

3) Loads the data into a Postgres database
- Connect to the database
- Create table(s)
- INSERT INTO
'''

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd 

import time
import logging

from pymongo import MongoClient
from sqlalchemy import create_engine


# Connect to the MongoDB database
mongo_client = MongoClient(host='mymongo', port=27017)
mongodb = mongo_client.slack_pipeline
slack_collection = mongodb.slackspiced


# Connect to the Postgres database
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')


# Create table slack in the Postgres database
CREATE_QUERY = ''' CREATE TABLE IF NOT EXISTS slacks
                   (text TEXT,
                   sentiment_score NUMERIC);'''

engine.execute(CREATE_QUERY)


s = SentimentIntensityAnalyzer()

# Write functions for each step of the ETL process
def extract():
    '''Extracts tweets from the MongoDB database'''
    slacks = list(slack_collection.find())
    # slacks is a list of slack messages, where each item is a slack message. Each slack message is of the datatype dict or cursor
    return slacks


def transform(slacks):
    for slack in slacks:
        slack['sentiment_score'] = s.polarity_scores(slack['text'])['compound']
    return slacks


def load(slacks):
    '''
    Load transformed slack messages into the Postgres database

    Parameters:
    -----------
    slacks : List of slack messages that were extracted from the MongoDB database and transformed.
    '''

    insert_query = 'INSERT INTO slacks VALUES (%s, %s)'
    for slack in slacks:
        engine.execute(insert_query, (slack['text'], slack['sentiment_score']))



extracted_slacks = extract()
transformed_slacks = transform(extracted_slacks)
load(transformed_slacks)
