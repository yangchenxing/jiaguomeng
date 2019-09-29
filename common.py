#coding: utf-8
from collections import namedtuple
from enum import Enum


class Category(Enum):
    House = '住宅'
    Business = '商业'
    Industry = '工业'
    All = '所有'


Category.values = set((Category.House, Category.Business,
                       Category.Industry, Category.All))


class Status(Enum):
    Any = 0
    OnlineOnly = 1
    OfflineOnly = 2


IncomeUp = namedtuple('IncomeUp', ('reason', 'value'))


def merge_income_ups(income_ups, reason):
    return IncomeUp(reason, sum(x.value for x in income_ups))
