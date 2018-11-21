from Core import Bus
from collections import OrderedDict


class TicketInterface(OrderedDict):
    def __init__(self, bus: Bus, purchase_record):
        for k, v in bus.items():
            self[k] = v
        for k, v in purchase_record.items():
            self[k] = v
