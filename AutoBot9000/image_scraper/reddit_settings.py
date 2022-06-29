import os
import json

class Settings(object):
    basename = 'config.json'

    def __init__(self, directory=None):
        self.directory = self._get_directory(directory)
        self.data = self._init_data()

    def _init_data(self):

        self.load()
        return self.data

    def _get_directory(self, dirname):

        if dirname is None:
            return os.curdir
        else:
            return dirname

# add subreddit,