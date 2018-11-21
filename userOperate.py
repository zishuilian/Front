from flask import render_template
from Core.BusTable import  BusTable
from Core.Bus import Bus
from Core import userAction
from Interface import PassengerInterface
import re
import random

bus_table = BusTable()


def register(username: str, password: str):
    return userAction.userCreateAccount(username, password, 0)


def get_bus(start, end, date="2018-10-07"):
    start_rexExp = re.compile('.*{}.*'.format(start), re.IGNORECASE)
    end_rexExp = re.compile('.*{}.*'.format(end), re.IGNORECASE)
    _list = [i for i in bus_table.find_bus(start_rexExp, end_rexExp, date)]
    pass


def get_buses():
    return bus_table.get_all()


def get_one_bus(Departure, Destination, BusId, BusDate):

    return bus_table.get_one_bus(Departure, Destination, BusDate, BusId)


def openBuyTicket(bus, username:str, link):
    person = userAction.userShowCard(username)
    _list = []
    for i in person:
        _list.append(PassengerInterface.PassengerInterface(i))
    return render_template('User/buyTicket.html', user=username, bus=bus, passengers=_list, link=link)


def buyTicket(username, card, departure, destination, date, BusId):
    if userAction.userBuyTicket(username, card, departure, destination, date, BusId):
        undo = userAction.checkBookList(username)
        done = userAction.checkExpireTicket(username)
        return undo, done
    return False


def returnTicket(username, card, departure, destination, date, BusId, link):
    userAction.userDeleteTicket(username, card, departure, destination, date, BusId)
    undo = userAction.checkBookList(username)
    done = userAction.checkExpireTicket(username)
    return render_template('User/ticketHistory.html', done=done, undo=undo, link=link)


def showUserCard(user):
    return userAction.userShowCard(user)


def addPassenger(user: str, card: str, name: str, phone: str, link):
    assert type(user) is str
    if userAction.userAddCard(user, card, name, phone):
        passengers = showUserCard(user)
        return passengers
    print('error {}'.format('add passenger error'))



def deletePassenger(user,card,link):
    userAction.userDeleteCard(user, card)
    return render_template('User/passengerInfo.html', link=link)


def changePassenger(user,card, name,phone, link):
    userAction.userDeleteCard(user,card)
    userAction.userAddCard(user, card, name, phone)
    return render_template('User/passengerInfo.html', link=link)


if __name__ == '__main__':
    username = 'a'
    card = '123'
    destination = '华工大学城校区'
    departure = '广州'
    date = '2019-1-07'
    BusId = 706
    print(userAction.userBuyTicket(username, card, departure, destination, date, BusId))
    # userAction.userCreateAccount('usertext', '123', 0)
    # userAction.userCreateAccount('admintext', '123', 2)
    #_bus = get_one_bus('深圳', '上海', '314', '2018-10-07')
    #print(_bus)

    # bus_list = []
    # des_list = ["北京", "上海", "广州", "深圳", "东莞", "华工大学城校区", "华工五山校区"]
    # for i in range(10):
    #     i_idx = random.randrange(0, int(len(des_list)/2))
    #     j_idx = random.randrange(int(len(des_list)/2), len(des_list))
    #
    #     _bus = Bus(BusId=random.randint(0, 10000), Destination=des_list[i_idx], Price=random.randint(0, 100), Departure=des_list[j_idx])
    #     try:
    #         bus_table.insert_bus(_bus)
    #     except OSError:
    #         print("insert error")
