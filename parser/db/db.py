from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker


class MethodsMongo:
    def __init__(self):
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client['test-database']['animal2']

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


class MethodsMySQL:
    def __init__(self):
        engine = create_engine("mysql://admin:admin@127.0.0.1:3306/test", echo=True)
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        self.session = Session()

    def insert(self, dict_insert, class_table):
        ins = class_table(**dict_insert)
        self.session.add(ins)

        try:
            self.session.commit()
            self.session.close()
        except IntegrityError:
            self.update(dict_insert, class_table)

    def update(self, dict_insert, class_table):
        self.session.rollback()
        self.session.execute(
            update(class_table)
            .where(class_table.ws_id == dict_insert.get('ws_id'))
            .values(**dict_insert)
        )
        self.session.commit()
        self.session.close()
