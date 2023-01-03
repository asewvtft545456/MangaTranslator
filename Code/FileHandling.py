import os

class FileHandler:
    def __init__(self):
        pass

    def find_directory(self, folderName):
        for r,d,f in os.walk(os.getcwd()):
            for folder in d:
                if folder == folderName:
                    return os.path.join(r,folder)
    
    def deleteFiles(self, directory):
        for r,d,f in os.walk(directory):
            for file in f:
                os.remove(directory+"\\{}".format(file))
