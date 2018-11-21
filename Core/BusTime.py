
class BusTime(dict):
    def __init__(self, year=1970, month=1, day=1, h=1, m=1):
        self['year'] = year
        self['month'] = month
        self['day'] = day
        self['h'] = h  # which hour
        self['m'] = m  # which minute

    @property
    def year(self):
        return self.year

    @year.setter
    def year(self, year):
        self['year'] = year

    @property
    def month(self):
        return self['month']

    @month.setter
    def month(self, month):
        self['month'] = month

    @property
    def day(self):
        return self['day']

    @day.setter
    def day(self, day):
        self['day'] = day

    @property
    def h(self):
        return self['h']

    @h.setter
    def h(self, h):
        self['h'] = h

    @property
    def m(self):
        return self['m']

    @m.setter
    def m(self, m):
        self['m'] = m

    pass


