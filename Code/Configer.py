import configparser
import os
from FileHandling import FileHandler

class Settings:
    def __init__(self):
        self.config = configparser.ConfigParser()
        setting = self.getConfig()
        self.cropText = setting.get("Paths", "cropText")
        self.Translated = setting.get("Paths", "Translated")
        self.downLoad = setting.get("Paths", "Download")
        self.consumer_key = setting.get("Twitter", "Consumer key", raw=True)
        self.consumer_secret = setting.get("Twitter", "Consumer secret", raw=True)
        self.access_token = setting.get("Twitter", "Access token", raw=True)
        self.access_token_secret = setting.get("Twitter", "Access token secret", raw=True)
        self.bearer_token = setting.get("Twitter", "Bearer token", raw=True)
    
    def createConfig(self):
        file = FileHandler()
        self.config.add_section("Paths")
        if file.find_directory("cropText"):
            self.config.set("Paths", "cropText", file.find_directory("cropText"))
        else:
            path = os.path.join(os.getcwd(),"cropText")
            os.mkdir(path)
            self.config.set("Paths", "cropText", path)
        if file.find_directory("Translated"):
            self.config.set("Paths", "Translated", file.find_directory("Translated"))
        else:
            pathT = os.path.join(os.getcwd(),"Translated")
            os.mkdir(pathT)
            self.config.set("Paths", "Translated", pathT)
        self.config.set("Paths", "Download", "")
        self.config.add_section("Twitter")
        self.config.set("Twitter", "Consumer key", "None")
        self.config.set("Twitter", "Consumer secret", "None")
        self.config.set("Twitter", "Access token", "None")
        self.config.set("Twitter", "Access token secret", "None")
        self.config.set("Twitter", "Bearer token", "None")


        with open("settings.ini", "w") as setting:
            self.config.write(setting)

    def getConfig(self):
        if not os.path.exists("settings.ini"):
            self.createConfig()

        self.config = configparser.ConfigParser()
        self.config.read("settings.ini")
        return self.config

    def updateSetting(self, section, setting, value):
        self.config = self.getConfig()
        self.config.set(section, setting, value)
        with open("settings.ini", "w") as updated:
            self.config.write(updated)
    
    def getUpdateInfo(self):
        self.cropText = self.config.get("Paths", "cropText")
        self.Translated = self.config.get("Paths", "Translated")
        self.downLoad = self.config.get("Paths", "Download")
        self.consumer_key = self.config.get("Twitter", "Consumer key", raw=True)
        self.consumer_secret = self.config.get("Twitter", "Consumer secret", raw=True)
        self.access_token = self.config.get("Twitter", "Access token", raw=True)
        self.access_token_secret = self.config.get("Twitter", "Access token secret", raw=True)
        self.bearer_token = self.config.get("Twitter", "Bearer token", raw=True)