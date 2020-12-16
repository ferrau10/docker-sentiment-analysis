import slack
from slack import WebClient
from slack.errors import SlackApiError
import requests
import pandas as pd 
from pymongo import MongoClient
import json 

# Create a connection to MongoDB
mongo_client = MongoClient(host='mymongo', port=27017) # host = name of mongodb container, port = port of container
mongodb = mongo_client.slack_pipeline
slack_collection = mongodb.slack


oauth_token = "xoxb-1263169162151-1382566512052-kcahC5NqnSNzYAbhRCnvh0fF"
channel = 'C0184AAGVRD'
client = slack.WebClient(token=oauth_token)

def getMessages2(token, channelID, limit):
    '''
    Get all the messages from a slack channel  with including a limit

    Parameters
    ----------
    token: oauth token for the slack workplace
    channelID: ID of the channel that you want to collect data from
    limit: number of messages to collect. By default the limit would be 100 if this was not part of the function.
    '''
    
    messages = client.api_call(api_method="conversations.history",
                             params={"channel": channelID,
                                   "limit": limit, 
                                   "token": token},
                             http_verb="GET")
    return messages

def getReplies(token, channelID, ts):
    '''
    Get threaded replies from one collected message based on the ts

    Parameters
    ----------
    token: oauth token for the slack workplace
    channelID: ID of the channel that you want to collect data from
    ts: thread number of the message
    '''
    resp = client.api_call(api_method="conversations.replies",
                             params={"channel": channelID,
                                   "ts": ts, 
                                   "token": token},
                             http_verb="GET")
    return resp 

def getQuestions_and_threads(df):
    '''
    Get all threaded replies from one df 

    Parameters
    ----------
    df: a dataFrame that has a collection of messages from slack 
    '''
    threads = []
    for i in df.ts:
        thread = getReplies(oauth_token, channel , i)
        threads.append(thread['messages'])
    return threads 

#Data is already collected, and then the bot got deleted by admins, but I used this code: 
# messages2 = getMessages2(oauth_token, channel, 400)
# df = pd.DataFrame(messages2['messages'])
# data = getQuestions_and_threads(df)

#loading data from the json file I had created before to save the data
with open('data_hands_on_agile_general.json') as json_file:
    data = json.load(json_file)

#load data 
for i in range(len(data)):
    mongodb.slackspiced.insert(data[i])