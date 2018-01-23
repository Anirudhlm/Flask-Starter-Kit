#!/usr/bin python
from pymongo import MongoClient

from config import config_default as config
mongo_conf = config.MONGO

class MongoClientProvider():
    """ A class that provides an instance of a mongo client, initialized with
        the host, port, username and password.
    """

    def __init__(self):
        self.host = mongo_conf['host']
        self.port = mongo_conf['port']
        self.username = mongo_conf['username']
        self.password = mongo_conf['password']
        self.database = mongo_conf['database']
        self.client = MongoClient(self.host, self.port, connect=False)
        self.client[self.database].authenticate(
            self.username, self.password, mechanism='SCRAM-SHA-1'
        )
        self.client = self.client[self.database]

    def get_client(self):
        """ Returns the instance of the client. """
        return self.client
