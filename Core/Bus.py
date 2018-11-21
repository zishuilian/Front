from .Date import Date
from datetime import date

class Bus(dict):
    def __init__(self, BusDate = "2019-01-07", BusId = '123', dTime = "16:55", aTime = "17:50", Departure = "aaa", Destination = "bbb", left_num = 50, Price = 100):
        BusId = str(BusId)
        self['BusDate'] = BusDate
        self['BusId'] = BusId
        self['dTime'] = dTime
        self['aTime'] = aTime
        self['Departure'] = Departure
        self['Destination'] = Destination
        self['left_num'] = left_num
        self['Price'] = Price

    def set_price(self, p):
        self.Price = p

    def set_time(self, BusDate, t1, t2):
        # if int(BusDate.year + BusDate.month + BusDate.day + t1) < int(self.BusDate.year + self.BusDate.month + self.BusDate.day + self.Time):
        #     return False
        # else:
        self.BusDate = BusDate
        self.dTime = t1
        self.aTime = t2

    def sell_ticket(self):
        if self.left_num > 0:
            self.left_num -= 1
            return True
        else:
            return False

    def cancel_ticket(self):
        self.left_num += 1