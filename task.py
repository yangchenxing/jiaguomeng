# coding: utf-8
from collections import namedtuple

from ability import Ability, Target, AbilitySet
from building import Category
from common import IncomeUp

Info = namedtuple('Info', ('name', 'ability'))

infos = [
    Info('反腐风暴', Ability(Target.All, 0.2)),
    Info('服务示范区', Ability(Target('便利店', '菜市场'), 1.5)),
    Info('绿色工厂', AbilitySet(
        Ability(Target('食品厂'), 1.0), Ability(Target('造纸厂'), 1.0), Ability(Target('电厂'), 1.5))),
    Info('保税商圈', AbilitySet(
        Ability(Target.Business, 0.3), Ability(Target('商贸中心'), 1.0, Ability(Target('便利店'), 1.5)))),
    Info('工业综合体', AbilitySet(
        Ability(Target.Industry, 0.3), Ability(Target('企鹅机械'), 1.0), Ability(Target('木材厂'), 1.0)))
]

infos = {info.name: info for info in infos}


class Task(object):
    def __init__(self, name):
        self.info = infos[name]

    def __repr__(self):
        return f'Task_{self.info.name}'

    def trigger(self, building, online):
        for value in self.info.ability.trigger(building, online):
            yield IncomeUp(self.info.name, value)


for name in infos.keys():
    setattr(Task, name, Task(name))
