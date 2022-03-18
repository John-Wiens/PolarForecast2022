import pymongo
import config
from datetime import datetime

client = pymongo.MongoClient(config.DB_URI)


def log_msg(msg, type = 'INFO', database = 'pf-database-2022'):
    event = {
        'DateTime' : datetime.now(),
        'Message': msg,
        'Type': type
    }
    print("DBLog", event)
    insert_one('Log', event, database=database)
    

def insert_one(col, item, database = 'pf-database-2022'):
    db = client[database]
    col = db[col]
    return col.insert_one(item)


def update_one(col, item, database = 'pf-database-2022'):
    db = client[database]
    col = db[col]
    return col.replace_one({'key': item['key']}, item, upsert=True)

def find_one(col, filter, database = 'pf-database-2022'):
    db = client[database]
    col = db[col]
    return col.find_one({'key':str(filter)})

def find(col, filter, database = 'pf-database-2022'):
    db = client[database]
    col = db[col]
    return col.find(filter)