# coding: utf-8
from collections import namedtuple

from ability import Ability, Target
from building import Category
from common import IncomeUp

Info = namedtuple('Info', ('name', 'ability'))

infos = [
    Info('反腐风暴', Ability(Target.All, 0.2)),
    Info('服务示范区', Ability(Target('便利店', '菜市场'), 1.5))
]

infos = {info.name: info for info in infos}


class Task(object):
    def __init__(self, name):
        self.info = infos[name]

    def trigger(self, building, online):
        for value in self.info.ability.trigger(building, online):
            yield IncomeUp(self.info.name, value)
