from Core.BusTable import  BusTable
from Core.Bus import Bus
import re
import random
import util

bus_table = BusTable()


def get_bus(start, end, date="2018-10-07"):
    start_rexExp = re.compile('.*{}.*'.format(start), re.IGNORECASE)
    end_rexExp = re.compile('.*{}.*'.format(end), re.IGNORECASE)
    _list = [i for i in bus_table.find_bus(start_rexExp, end_rexExp, date)]
    _list = sorted(_list, key=util.cmp_min_to_sec)
    return _list


def get_buses():
    _list = [i for i in bus_table.get_all()]
    _list = sorted(_list, key=util.cmp_min_to_sec)
    return _list


def get_passenger():
    user_list = [{'姓名': '文毅鸿', '身份证号码': '440582199810342930'}]
    pass


def assert_not_none(argv: list):
    for i in argv:
        assert i is not None


if __name__ == '__main__':

    bus_list = []
    des_list = ["北京", "上海", "广州", "深圳", "东莞", "华工大学城校区", "华工五山校区"]
    for i in range(10):
        j_idx = random.randrange(0, int(len(des_list)/2))
        i_idx = random.randrange(int(len(des_list)/2), len(des_list))
        h_1 = random.randrange(0, 24)
        h_2 = random.randrange(h_1, 24)
        min_1 = random.randrange(0, 60)
        min_2 = random.randrange(0, 60)
        _t1 = str(h_1) + ":" + str(min_1)
        _t2 = str(h_2) + ":" + str(min_2)
        _bus = Bus(BusId=str(random.randint(10000, 20000)), Destination=des_list[i_idx], Price=random.randint(0, 100), Departure=des_list[j_idx],
                   dTime=_t1, aTime=_t2)
        try:
            # bus_table.delete_bus('{}')
            bus_table.insert_bus(_bus)
        except OSError:
            print("insert error")
