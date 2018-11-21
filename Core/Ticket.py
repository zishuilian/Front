from .Date import Date

class Ticket():
    def __init__(self, BusDate, BusId, SeatId, AccountId):
        self.BusDate = BusDate
        self.BusId = BusId
        self.SeatId = SeatId
        self.AccountId = AccountId

