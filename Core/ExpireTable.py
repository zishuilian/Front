from Core.getDatabase import getDatabase

class ExpireTable:
    def __init__(self):
        pass

    def insertRecord(self, record):
        client, cursor = getDatabase('expire_collections')
        cursor.insert_one(record)
        client.close()

    def showRecord(self, username):
        client, cursor = getDatabase('expire_collections')
        _list = cursor.find({'username': username})
        client.close()
        return _list