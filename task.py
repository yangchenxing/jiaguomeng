# coding: utf-8
from collections import namedtuple
from building import Category

Info = namedtuple('Info', ('name', 'targets', 'category', 'value'))

infos = [
    Info('反腐风暴', (), Category.All, 0.2),
]

infos = {info.name: info for info in infos}

IncomeUp = namedtuple('IncomeUp', ('reason', 'value'))


class Task(object):
    def __init__(self, name):
        self.info = infos[name]

    def calculate_income_up(self, target):
        if self.info.targets and target.info.name not in self.info.targets:
            return None
        if self.info.category != target.info.category and self.info.category != Category.All:
            return None
        return IncomeUp(self.info.name, self.info.value)
