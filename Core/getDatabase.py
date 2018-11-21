from pymongo import MongoClient
PORT = 27017

def getDatabase(dbname):
    client = MongoClient('localhost', PORT)
    db = client.station_database
    # print(db)
    cursor = db[dbname]
    # print(cursor)
    return client, cursor
