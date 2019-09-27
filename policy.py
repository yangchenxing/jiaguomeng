# coding: utf-8
from collections import namedtuple
from building import Category

Info = namedtuple('Info', ('name', 'category', 'online', 'offline', 'values'))


infos = [
    Info('一带一路建设', Category.All, True, True, [None, None, None, 0.75, 1.0]),
    Info('自由贸易区建设', Category.Business, True,
         True, [None, None, 1.5, None, None]),
    Info('区域协调发展', Category.House, True, True, [None, None, 1.5, None, None]),
]

infos = {info.name: info for info in infos}

IncomeUp = namedtuple('IncomeUp', ('reason', 'value'))


class Policy(object):
    def __init__(self, name, level):
        self.info = infos[name]
        self.level = level

    def calculate_income_up(self, target, online):
        if self.info.category == target.info.category or self.info.category == Category.All:
            if online and self.info.online or not online and self.info.offline:
                return IncomeUp(self.info.name, self.info.values[self.level - 1])
        return None


class Light(object):
    def __init__(self, value):
        self.value = value

    def calculate_income_up(self, target, online):
        return IncomeUp('家国之光', self.value)
