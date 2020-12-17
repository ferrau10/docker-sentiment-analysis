import os
import logging
from sqlalchemy import create_engine
import time
from slack import RTMClient
from slack.errors import SlackApiError

oauth_token =  'xoxb-1263169162151-1568563158727-vh8bMN7zZkPdD1XVbFkXzVyE'
#oauth_token = "xoxb-1263169162151-1382329023637-RtdTCS32CCd7OrXOxIhO8AbE"

# Connect to the Postgres database
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')

POSITIVE_RANDOM_QUERY = '''SELECT * FROM slacks where sentiment_score > 0.99 ORDER BY RANDOM() LIMIT 1;'''
                
NEGATIVE_RANDOM_QUERY = '''SELECT * FROM slacks where sentiment_score < 0.01 ORDER BY RANDOM() LIMIT 1;'''


if len(engine.table_names()) == 0: 
    time.sleep(5)

with engine.connect() as connection:
    result_positive = connection.execute(POSITIVE_RANDOM_QUERY)
    for row in result_positive:
        text_positive = row['text']

    result_negative = connection.execute(NEGATIVE_RANDOM_QUERY)
    for row in result_negative:
        text_negative = row['text']



@RTMClient.run_on(event='message')
def answer_slack_messages(**payload):
    data = payload['data']
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    print('moody')

    if 'text' in data and 'Hello' in data.get('text', []) or 'yo' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']


        try:
            response = web_client.chat_postMessage(
                channel=channel_id,
                text=f"Hi <@{user}>!",
                thread_ts=thread_ts
            )

        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")


    if 'text' in data and 'positive' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        try:
            response_positive = web_client.chat_postMessage(
                channel=channel_id,
                text=text_positive,
                thread_ts=thread_ts
            )

        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")


    if 'text' in data and 'negative' in data.get('text', []):
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        try:
            response_negative = web_client.chat_postMessage(
                channel=channel_id,
                text=text_negative,
                thread_ts=thread_ts
            )

        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")



rtm_client = RTMClient(token=oauth_token)
rtm_client.start()



