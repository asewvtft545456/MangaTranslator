import tweepy
import requests
import os
import json
from Configer import Settings
import ast

setting = Settings()
consumer_key = setting.consumer_key
consumer_secret = setting.consumer_secret
access_token = setting.access_token
access_token_secret = setting.access_token_secret
bearer_token = ""
if ast.literal_eval(setting.bearer_token) == list:
    bearer_token = "%".join(ast.literal_eval(setting.bearer_token))
else:
    bearer_token = setting.bearer_token.strip("[]")

auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
    )

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret,
    bearer_token=bearer_token
)
api = tweepy.API(auth)

def getImageUrl(link):
    try:
        imageURL = []
        id = link.split('/')[-1]
        status = api.get_status(str(id))._json
        for url in status['extended_entities']['media']:
            imageURL.append(url['media_url'])
    except:
        print("Error")
        pass
    return imageURL


def download(urls):
    files = []
    directory = Settings()
    try:
        for url in urls:
            name = directory.downLoad+'\\'+ url.split('/')[-1]
            data = requests.get(url).content
            with open(name, 'wb') as file:
                file.write(data)
            files.append(name)
    except:
        print("Error")
        pass
    return files
