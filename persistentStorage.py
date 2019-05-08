from kademlia.storage import IStorage
import time
from itertools import takewhile
import operator
from collections import OrderedDict
from pymongo import MongoClient

class PersistentStorage (IStorage):
    def __init__(self, ttl=604800, mongourl='mongodb://localhost:27017', db='dht', collection='records'):
        '''
        By default, max age is a week.
        '''
        self.data = OrderedDict()
        self.ttl = ttl
        # Initialize MongoClient
        client = MongoClient(mongourl)
        db = client[db]
        self.storage = db[collection]
        self.warmup()

    def __setitem__(self, key, value):
        # Write to the Dictionary
        if key in self.data:
            del self.data[key]
        self.data[key] = (time.monotonic(), value)
        self.cull()
        # Write to Mongo
        self.storage.find_one_and_replace({'_id':key},
                                          {'_id':key, key.hex():value},
                                          upsert=True)

    # Put everything from Mongo to Dictionary
    def warmup(self):
        records = self.storage.find(projection={'_id': False})
        for record in records:
            for key in list(record):
                dictKey = bytes.fromhex(key)
                self.data[dictKey] = (time.monotonic(), record[key])
        self.cull()

    def cull(self):
        for _, _ in self.iter_older_than(self.ttl):
            self.data.popitem(last=False)

    def get(self, key, default=None):
        self.cull()
        if key in self.data:
            return self[key]
        return default

    def __getitem__(self, key):
        self.cull()
        return self.data[key][1]

    def __repr__(self):
        self.cull()
        return repr(self.data)

    def iter_older_than(self, seconds_old):
        min_birthday = time.monotonic() - seconds_old
        zipped = self._triple_iter()
        matches = takewhile(lambda r: min_birthday >= r[1], zipped)
        return list(map(operator.itemgetter(0, 2), matches))

    def _triple_iter(self):
        ikeys = self.data.keys()
        ibirthday = map(operator.itemgetter(0), self.data.values())
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ibirthday, ivalues)

    def __iter__(self):
        self.cull()
        ikeys = self.data.keys()
        ivalues = map(operator.itemgetter(1), self.data.values())
        return zip(ikeys, ivalues)
