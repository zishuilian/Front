from collections import OrderedDict
import util


class PassengerInterface(OrderedDict):
    def __init__(self, person):
        for k, v in person.items():
            self[k] = v
        if 'card' in self.keys():
            self['sex'] = util.get_sex_from_id(self['card'])
            self['birthday'] = util.get_birthday_from_id(self['card'])
            pass



