from Core.getDatabase import getDatabase
from Core.BusTable import BusTable
from pymongo import MongoClient
# <<<<<<< HEAD
# import
# import Date
# =======
import Core.Date
# >>>>>>> 1dfb90fd307e946b179efd04504ebd442b8c498d

class PurchaseTable():

    def __init__(self):
        pass

    def insertRecord(self, username, card, departure, destination, date, BusId, price):
        client, cursor = getDatabase('purchase_collections')
        cursor.insert_one({'username': username, 'card': card, 'departure': departure, 'destination': destination, 'date': date, 'BusId': BusId, 'price': price})
        client.close()

    def deleteOneRecord(self, username, card, departure, destination, date, BusId):
        client, cursor = getDatabase('purchase_collections')
        cursor.delete_one({'username': username, 'card': card, 'departure': departure, 'destination': destination, 'date': date, 'BusId': BusId})
        client.close()

    def updateRecord(self, oldRecord, departure = 'undefined', destination = 'undefined', date = 'undefined',
                    BusId = -1):
        client, cursor = getDatabase('purchase_collections')
        if departure == 'undefined':
            Ndeparture = oldRecord['departure']
        else:
            Ndeparture = departure

        if destination == 'undefined':
            Ndestination = oldRecord['destination']
        else:
            Ndestination = destination

        if date == 'undefined':
            Ndate = oldRecord['date']
        else:
            Ndate = date

        if BusId == -1:
            NBusId = oldRecord['BusId']
        else:
            NBusId = BusId

        cursor.update(oldRecord, {'$set': {'departure': Ndeparture, 'destination': Ndestination, 'date': Ndate, 'BusId': NBusId}})
        client.close()
        return

    # admin使用
    def findRecordForOneBus(self, departure, destination, date, BusId):
        client, cursor = getDatabase('purchase_collections')
        _list = cursor.find({'departure': departure, 'destination': destination, 'date': date, 'BusId': BusId})
        client.close()
        return _list

    # admin使用，用于查找一定范围的数据
    def findRangeRecord(self, startDate, endDate, departure, destination):
        client, cursor = getDatabase('purchase_collections')
        condition = {}
        if startDate != "undefined":
            condition["date"] = {'$gte': startDate, '$lte': endDate}
        if departure != "undefined":
            condition["departure"] = departure
        if destination != "undefined":
            condition["destination"] = destination
        _list = cursor.find(condition).sort([('date', 1), ('BusId', 1), ('destination', 1)])

        _list2 = []
        data = {}
        date = '1'
        dest = '1'
        dep = '1'
        bid = '1'
        totalCustomer = 0
        totalRevenue = 0

        for i in _list:
            if i['date'] != date or i['destination'] != dest or i['departure'] != dep or i['BusId'] != bid:
                data['date'] = date
                data['destination'] = dest
                data['departure'] = dep
                data['BusId'] = bid
                data['totalCustomer'] = totalCustomer
                data['totalRevenue'] = totalRevenue
                _list2.append({'date': date, 'destination': dest, 'departure': dep, 'BusId': bid, 'totalCustomer': totalCustomer, 'totalRevenue': totalRevenue})
                date = i['date']
                dest = i['destination']
                dep = i['departure']
                bid = i['BusId']
                totalCustomer = 1
                totalRevenue = i['price']
            else:
                totalCustomer = totalCustomer + 1
                totalRevenue = totalRevenue + i['price']

        _list2.append({'date': date, 'destination': dest, 'departure': dep, 'BusId': bid, 'totalCustomer': totalCustomer,
             'totalRevenue': totalRevenue})

        for i in range(len(_list2)):
            if _list2[i]['date'] == '1':
                del _list2[i]
                break

        for i in _list2:
            print(i)

        totalCustomer = 0
        totalRevenue = 0
        for i in _list2:
            totalCustomer = totalCustomer + i['totalCustomer']
            totalRevenue = totalRevenue + i['totalRevenue']
        print(totalCustomer, totalRevenue)
        client.close()
        return totalCustomer, totalRevenue, _list2


    # 用户使用
    def searchRecord(self, condition):
        client, cursor = getDatabase('purchase_collections')
        _list = cursor.find(condition)
        client.close()
        return [i for i in _list]



    # print(PT.searchRecord(''))
