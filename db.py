from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class MethodsMongo:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client['test-database']['animal']

    def insert(self, dict_insert, *args):
        try:
            self.db.insert_one(dict_insert)
        except DuplicateKeyError:
            self.update(dict_insert, *args)

    def update(self, dict_insert, *args):
        dict_insert.update(*args)
        self.db.update_one({'_id': dict_insert.get('_id')}, {'$set': dict_insert})

    def find(self, *args):
        return self.db.find_one(*args)

    def find_all(self, *args):
        return self.db.find(*args)
