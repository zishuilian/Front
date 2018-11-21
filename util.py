import math


def cmp_min_to_sec(x, key_str='dTime'):  # 计算13：45 的真实分钟。方便进行排序.
    assert type(key_str) == str
    _pos_1 = x[key_str].find(':')
    return int(x[key_str][:_pos_1])*60 + int(x[key_str][_pos_1+1:])


def cmp_year_day_mon_to_sec(x, key_str='BusDate'):
    '''
    :param x: str like '2019-01-07'
    :return: secs
    '''
    assert type(key_str) == str
    _pos_1 = x[key_str].find('-')
    _pos_2 = x[key_str].find('-', _pos_1+1)
    if _pos_2 - _pos_1 > 1:
        year = int(x[key_str][:_pos_1])
        month = int(x[key_str][_pos_1+1:_pos_2])
        day = int(x[key_str][_pos_2+1:])
        return (year*365 + month*30 + day)*24*60*60


def cmp_year_and_min_to_sec(x, key_str_date='BusDate', key_str_min='dTime'):
    return cmp_year_day_mon_to_sec(x, key_str_date) + cmp_min_to_sec(x, key_str_min)


def get_sex_from_id(card: int):
    '''
    :param card: ID of the passenger
    :return: the sex str
    '''
    card = int(card)
    _num = math.floor((card % 100) / 10) % 2
    if _num == 1:
        return '男'
    return '女'


def get_birthday_from_id(card: str):
    '''
    :param card: ID of the passenger
    :return: the birthday str
    '''
    id_list = list(card)
    if len(id_list) == 18:
        year = ''.join(id_list[6:10])
        month = ''.join(id_list[10:12])
        day = ''.join(id_list[12:14])
        return '{}-{}-{}'.format(year, month, day)
    return '------'




