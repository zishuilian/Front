from Core.BusTable import BusTable
from Core.PurchaseTable import PurchaseTable
from Core.AccountTable import AccountTable
from Core.IdentityTable import IdentityTable
from Core.DeleteTable import DeleteTable
from Core.ExpireTable import ExpireTable
import time

from Interface import TicketInterface
# 定义了用户所能进行的所有动作

#根据用户给定的条件查找对应的巴士，返回巴士列表
def userSearchBus(departure, destination, date):
    BT = BusTable()
    return BT.find_bus(departure, destination, date)

# 为username用户使用card购买符合条件的票，返回成功或失败
def userBuyTicket(username, card, departure, destination, date, BusId):
    # assert type(BusId) == int
    BT = BusTable()
    PT = PurchaseTable()
    num = 0
    _list = PT.searchRecord({'username': username, 'card': card, 'departure': departure, 'destination': destination, 'date': date, 'BusId': BusId})
    # print(_list)
    for i in _list:
        num += 1
    if num != 0:
        print("db do not has the ticket {}".format(BusId))
        return False
    f, price = BT.buy(departure, destination, date, BusId)
    if f:
        PT.insertRecord(username, card, departure, destination, date, BusId, price)
        return True
    else:
        print('{} buy error'.format(username))
        return False

# 返回username名字的用户的等级，分成0，1，2三个等级
def userGetLevel(username):
    AT = AccountTable()
    return AT.getLevel(username)

# 登陆名为username的用户,验证password是否正确，返回0：不存在账号；1：密码错误；2：登陆成功
def userLogIn(username, password):
    AT = AccountTable()
    return AT.login(username, password)

# 创建名为username，密码为password的用户，返回成功或失败（已存在名为username的用户），level是用户等级
def userCreateAccount(username, password, level):
    AT = AccountTable()
    if AT.exist(username):
        return False
    else:
        AT.insert_account(username, password, level)
        return True

# 返回usernmae用户绑定的所有身份证
def userShowCard(username):
    IT = IdentityTable()
    return IT.find(username)

# 为username的用户添加一张卡card
def userAddCard(username, card, name, phone):
    IT = IdentityTable()
    try:
        print(username)
        print(card)
        print(name)
        print(phone)
        IT.insert(username, card, name, phone)
    except OSError:
        return False
    return True

# 为username的用户删除一张卡card
def userDeleteCard(username, card):
    IT = IdentityTable()
    return IT.delete(username, card)

# 为username的用户查询其购票记录，返回已经购票了的车辆的信息
# 可以指定为某个身份证查
# 注意返回的信息中，票价是原本购买时采用的票价
# 返回符合条件的巴士列表和数量（要么查username全部的，要么查某张卡的）
def checkBookList(username, card = "-1"):
    PT = PurchaseTable()
    BT = BusTable()
    condition = {}
    condition['username'] = username
    if card != "-1":
        condition['card'] = str(card)

    _list1 = PT.searchRecord(condition)
    _list2 = []
    total_num = 0
    for i in _list1:
        ticket = TicketInterface.TicketInterface(BT.get_one_bus(i['departure'], i['destination'], i['date'], i['BusId']), i)
        _list2.append(ticket)
        _list2[total_num]['Price'] = i['price']
        total_num = total_num + 1
    return _list2, total_num

# 同上，查询的是delete表（退票表）里面的信息
def checkDeleteList(username, card = -1):
    DT = DeleteTable()
    BT = BusTable()
    condition = {}
    condition['username'] = username
    if card != -1:
        condition['card'] = card

    _list1 = DT.searchRecord(condition)
    _list2 = []
    total_num = 0
    for i in _list1:
        _list2.append(BT.get_one_bus(i['departure'], i['destination'], i['date'], i['BusId']))
        _list2[total_num]['Price'] = i['price']
        total_num = total_num + 1
    return _list2, total_num

def userDeleteTicket(username, card, departure, destination, date, BusId):
    BT = BusTable()
    PT = PurchaseTable()
    DT = DeleteTable()
# <<<<<<< HEAD
    PT.deleteOneRecord(username, card, departure, destination, date, BusId)
    DT.insertRecord(username, card, departure, destination, date, BusId, 4396)
# =======
    condition = {'username': username, 'card': card, 'departure': departure, 'destination': destination, 'date': date, 'BusId': BusId}
    p = PT.searchRecord(condition);
    i = p[0]
    PT.deleteOneRecord(username, card, departure, destination, date, BusId)
    DT.insertRecord(username, card, departure, destination, date, BusId, i['price'])
# >>>>>>> 1dfb90fd307e946b179efd04504ebd442b8c498d
    BT.addOneSeat(departure, destination, date, BusId)

# 在用户登陆时，更新票务信息，将过了期的票转移到ExpireTable中
def updateTicketInfo(username):
    BT = BusTable()
    PT = PurchaseTable()
    ET = ExpireTable()
    _list = PT.searchRecord({'username': username}) #找某个用户的所有购买记录
    for i in _list:
        b = BT.get_one_bus(i['departure'], i['destination'], i['date'], i['BusId'])
        ticketTime = b['BusDate'] + b['dTime']
        currTime = time.strftime('%Y-%m-%d%H:%M', time.localtime(time.time()))
        if currTime > ticketTime:   #过期票，将记录从perchase表移入到expire表
            PT.deleteOneRecord(username, i['card'], i['departure'], i['destination'], i['date'], i['BusId'])
            ET.insertRecord(i)

# 查看已使用的票
def checkExpireTicket(username):
    ET = ExpireTable()
    return ET.showRecord(username)

if __name__ == '__main__':
    # print(userAddCard('a', 'a', '123', '123'))
    ET = ExpireTable()
    print(ET.showRecord('a'))
