import tweepy
import requests
import os
import json
from Configer import Settings
import ast

class Twitter:
    def __init__(self):     
        self.setting = Settings()
        self.setting.getUpdateInfo()
        consumer_key = self.setting.consumer_key
        consumer_secret = self.setting.consumer_secret
        access_token = self.setting.access_token
        access_token_secret = self.setting.access_token_secret
        bearer_token = ""
        if ast.literal_eval(self.setting.bearer_token) == list:
            bearer_token = "%".join(ast.literal_eval(self.setting.bearer_token))
        else:
            bearer_token = self.setting.bearer_token.strip("[]")

        auth = tweepy.OAuth1UserHandler(
            consumer_key=consumer_key, consumer_secret=consumer_secret,
            access_token=access_token, access_token_secret=access_token_secret
            )

        self.api = tweepy.API(auth)

    def getImageUrl(self, link):
        self.setting.getUpdateInfo()
        try:
            imageURL = []
            id = link.split('/')[-1]
            status = self.api.get_status(str(id))._json
            for url in status['extended_entities']['media']:
                imageURL.append(url['media_url'])
        except:
            print("Error")
            pass
        return imageURL


    def download(self, urls):
        files = []
        directory = self.setting.downLoad
        try:
            for url in urls:
                name = directory+'\\'+ url.split('/')[-1]
                data = requests.get(url).content
                with open(name, 'wb') as file:
                    file.write(data)
                files.append(name)
        except:
            print("Error")
            pass
        return files
