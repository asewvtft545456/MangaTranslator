import configparser
import os
from FileHandling import FileHandler

class Settings:
    def __init__(self):
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
        config = configparser.SafeConfigParser()
        config.add_section("Paths")
        if file.find_directory("cropText"):
            config.set("Paths", "cropText", file.find_directory("cropText"))
        else:
            path = os.path.join(os.getcwd(),"cropText")
            os.mkdir(path)
            config.set("Paths", "cropText", path)
        if file.find_directory("Translated"):
            config.set("Paths", "Translated", file.find_directory("Translated"))
        else:
            pathT = os.path.join(os.getcwd(),"Translated")
            os.mkdir(pathT)
            config.set("Paths", "Translated", pathT)
        config.set("Paths", "Download", "")
        config.add_section("Twitter")
        config.set("Twitter", "Consumer key", "None")
        config.set("Twitter", "Consumer secret", "None")
        config.set("Twitter", "Access token", "None")
        config.set("Twitter", "Access token secret", "None")
        config.set("Twitter", "Bearer token", "None")


        with open("settings.ini", "w") as setting:
            config.write(setting)

    def getConfig(self):
        if not os.path.exists("settings.ini"):
            self.createConfig()

        config = configparser.ConfigParser()
        config.read("settings.ini")
        return config

    def updateSetting(self, section, setting, value):
        config = self.getConfig()
        config.set(section, setting, value)
        with open("settings.ini", "w") as updated:
            config.write(updated)
        

Settings()