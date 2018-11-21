from Core.getDatabase import getDatabase

# Bus表，存放所有bus的信息
class BusTable():
    def __init__(self):
        pass

    def insert_bus(self, b):
        # client, cursor = getDatabase('bus_collections')  # or cursor = db.test_collections auto create the collection
        # cursor.ensure_index('', unique=True)
        client, cursor = getDatabase('bus_collections')
        condition = {'BusDate': b['BusDate'], 'BusId': b['BusId'], 'Departure': b['Departure'], 'Destination': b['Destination']}
        if cursor.find_one(condition) == None:
            cursor.insert_one(b)
            client.close()
            return True
        else:
            client.close()
            return False

    def addOneSeat(self, departure, destination, date, BusId):
        client, cursor = getDatabase('bus_collections')
        b = cursor.find_one({'Destination': destination, 'Departure': departure, 'BusDate': date, 'BusId': BusId})
        t = b['left_num']
        t = t + 1
        cursor.update({'Destination': destination, 'Departure': departure, 'BusDate': date, 'BusId': BusId}, {'$set': {'left_num': t}})
        client.close()

    def delete_bus(self, Bus):
        client, cursor = getDatabase('bus_collections')
        condition = {'Departure': Bus['Departure'], 'Destination' : Bus['Destination'], 'BusDate': Bus['BusDate'], 'BusId': Bus['BusId']}
        if cursor.find(condition) == None:
            client.close()
            return False
        else:
            cursor.delete_one(condition)
            client.close()
            return True

    def update_bus(self, OBus, NBus):
        client, cursor = getDatabase('bus_collections')
        Ocondition = {'Departure': OBus['Departure'], 'Destination': OBus['Destination'], 'BusDate': OBus['BusDate'], 'BusId': OBus['BusId']}

        cursor.update(Ocondition, NBus)
        client.close()

    # 根据出发地、目的地和日期来找车
    def find_bus(self, departure, destination, date):
        client, cursor = getDatabase('bus_collections')
        _list = cursor.find({'Departure': departure, 'Destination': destination, 'BusDate': date}).sort('Busdate')
        client.close()
        return _list

    def get_one_bus(self, departure, destination, date, BusId):
        client, cursor = getDatabase('bus_collections')
        condition = {'Departure': departure, 'Destination': destination, 'BusDate': date, 'BusId': BusId}
        bus = cursor.find_one(condition)
        client.close()
        return bus

    def buy(self, departure, destination, date, BusId):
        client, cursor = getDatabase('bus_collections')
        condition = {'BusDate': date, 'BusId': BusId, 'Departure': departure,
                     'Destination': destination}
        # print(cursor.find({}))
        b = cursor.find_one(condition)

        if b != None and b['left_num'] > 0:
            b['left_num'] = b['left_num'] - 1
            cursor.update(condition, b)
            client.close()
            return True, b['Price']
        return False, 0

    def get_all(self):
        client, cursor = getDatabase('bus_collections')
        _list = cursor.find({}).sort('BusDate')
        client.close()
        return _list

