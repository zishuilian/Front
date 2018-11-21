from Core.getDatabase import getDatabase

class DeleteTable:
    def __init__(self):
        pass

    def insertRecord(self, username, card, departure, destination, date, BusId, price):
        client, cursor = getDatabase('delete_collections')
        cursor.insert_one({'username': username, 'card': card, 'departure': departure, 'destination': destination, 'date': date, 'BusId': BusId, 'price': price})
        client.close()

    def searchRecord(self, condition):
        client, cursor = getDatabase('delete_collections')
        _list = cursor.find(condition)
        client.close()
        return _list
