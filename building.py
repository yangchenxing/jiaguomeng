# coding: utf-8
from collections import namedtuple
from enum import Enum
from itertools import chain
from functools import reduce, partial
from math import factorial
from operator import mul


from ability import Ability, AbilitySet, Target
from common import Category, Status, IncomeUp, merge_income_ups

_income_base = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11,
                14, 17, 21, 27, 33, 42, 53, 66, 83, 104,
                130]


class Quality(Enum):
    Normal = '普通'
    Rare = '稀有'
    Epic = '史诗'


Info = namedtuple(
    'Info', ('name', 'category', 'quality', 'coefficient', 'ability'))

infos = [
    Info('木屋', Category.House, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('木材厂'), 1.0))),
    Info('平房', Category.House, Quality.Normal, 1.1,
         AbilitySet(Ability(Target.House, 0.2))),
    Info('居民楼', Category.House, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('便利店'), 1.0))),
    Info('钢结构房', Category.House, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('钢铁厂'), 1.0))),
    Info('小型公寓', Category.House, Quality.Normal, 1.18, AbilitySet.Empty),
    Info('人才公寓', Category.House, Quality.Rare, 1.4,
         AbilitySet(Ability(Target.All, 0.2, Status.OnlineOnly), Ability(Target.Industry, 0.15))),
    Info('花园洋房', Category.House, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('商贸中心'), 1.0))),
    Info('中式小楼', Category.House, Quality.Rare, 1.4,
         AbilitySet(Ability(Target.All, 0.2, Status.OnlineOnly), Ability(Target.House, 0.15))),
    Info('空中别墅', Category.House, Quality.Epic, 1.0,
         AbilitySet(Ability(Target('民食斋'), 1.0), Ability(Target.All, 0.2, Status.OnlineOnly))),
    Info('复兴公馆', Category.House, Quality.Epic, 1.0,
         AbilitySet(Ability(Target.All, 0.1, Status.OfflineOnly))),

    Info('便利店', Category.Business, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('居民楼'), 1.0))),
    Info('五金店', Category.Business, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('零件厂'), 1.0))),
    Info('服装店', Category.Business, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('纺织厂'), 1.0))),
    Info('菜市场', Category.Business, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('食品厂'), 1.0))),
    Info('学校', Category.Business, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('图书城'), 1.0))),
    Info('图书城', Category.Business, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('学校'), 1.0), Ability(Target('造纸厂'), 1.0))),
    Info('商贸中心', Category.Business, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('花园洋房'), 1.0))),
    Info('加油站', Category.Business, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('人民石油'), 0.5), Ability(Target.All, 0.1, Status.OfflineOnly))),
    Info('民食斋', Category.Business, Quality.Epic, 1.52,
         AbilitySet(Ability(Target('空中别墅'), 1.0), Ability(Target.All, 0.2, Status.OnlineOnly))),
    Info('媒体之声', Category.Business, Quality.Epic, 1.615,
         AbilitySet(Ability(Target.All, 0.1, Status.OfflineOnly), Ability(Target.All, 0.5))),

    Info('木材厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('木屋'), 1.0))),
    Info('食品厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('菜市场'), 1.0))),
    Info('造纸厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('图书城'), 1.0))),
    Info('水厂', Category.Industry, Quality.Normal, 1.26,
         AbilitySet(Ability(Target.All, 0.1, Status.OfflineOnly))),
    Info('电厂', Category.Industry, Quality.Normal, 1.18,
         AbilitySet(Ability(Target.All, 0.2, Status.OnlineOnly))),
    Info('钢铁厂', Category.Industry, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('钢结构房'), 1.0), Ability(Target.Industry, 0.15))),
    Info('纺织厂', Category.Industry, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('服装店'), 1.0), Ability(Target.Business, 0.15))),
    Info('零件厂', Category.Industry, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('五金店'), 1.0), Ability(Target('企鹅机械'), 0.5))),
    Info('企鹅机械', Category.Industry, Quality.Epic, 1.33,
         AbilitySet(Ability(Target('零件厂'), 1.0), Ability(Target.All, 0.1))),
    Info('人民石油', Category.Industry, Quality.Epic, 1.0,
         AbilitySet(Ability(Target('加油站'), 1.0), Ability(Target.All, 0.1, Status.OfflineOnly))),
]

infos = {info.name: info for info in infos}

# check ability
for info in infos.values():
    info.ability.validate(infos)

IncomeInfo = namedtuple('IncomeInfo', ('base', 'up', 'up_ratio', 'reasons'))


class Building(object):
    def __init__(self, name, star, level):
        self.info = infos[name]
        self.star = star
        self.level = level if level <= 200 else 200
        self.income = self._calculate_base_income()

    def set_level(self, level):
        self.level = level
        self.income = self._calculate_base_income()

    def set_global_income_up(self, photos, policies, task):
        self.global_reasons = {
            True: [
                merge_income_ups(photos.trigger(self, True), '照片'),
                merge_income_ups(policies.trigger(self, True), '政策'),
            ],
            False:  [
                merge_income_ups(photos.trigger(self, False), '照片'),
                merge_income_ups(policies.trigger(self, False), '政策'),
            ],
        }
        task_online = list(task.trigger(self, True))
        task_offline = list(task.trigger(self, False))
        if task_online:
            self.global_reasons[True].append(
                merge_income_ups(task_online, '任务'))
        if task_offline:
            self.global_reasons[False].append(
                merge_income_ups(task_offline, '任务'))
        self.global_ups = {
            True: reduce(mul, ((1+up.value) for up in self.global_reasons[True]), 1)-1,
            False: reduce(mul, ((1+up.value) for up in self.global_reasons[False]), 1)-1,
        }

    def calculate_building_ups(self, buildings):
        self.building_ups = {
            True: dict(self.calculate_building_ups_with_status(True, buildings)),
            False: dict(self.calculate_building_ups_with_status(False, buildings)),
        }

    def calculate_building_ups_with_status(self, online, buildings):
        for cooperator in buildings:
            ups = list(IncomeUp(f'{cooperator.info.name}[{"*"*cooperator.star}]',
                                value * cooperator.star) for value in cooperator.info.ability.trigger(self, online))
            if ups:
                yield (cooperator.info.name, ups)

    def __str__(self):
        return self.info.name

    def __repr__(self):
        return self.info.name

    def _calculate_base_income(self):
        n = (self.level - 1) // 10
        return (sum(_income_base[: n]) * 10 +
                _income_base[n] * (self.level - n * 10)) * factorial(self.star) * self.info.coefficient

    def calculate_income(self, online, buildings):
        # 建筑加成
        # building_reasons = list(self.trigger_ability(buildings, online))
        building_ups = self.building_ups[online]
        #print('building ups:', building_ups)
        building_reasons = list(chain(
            *(building_ups[building.info.name] for building in buildings if building.info.name in building_ups)))
        #print('building reasons:', building_reasons)
        building_up = sum(up.value for up in building_reasons)
        # 全局加成
        global_reasons = self.global_reasons[online]
        global_up = self.global_ups[online]
        total_up = (1+building_up) * (1+global_up) - 1
        base = self.income * (0.5 if not online else 1.0)
        return IncomeInfo(base, base * total_up, total_up, building_reasons + global_reasons)

    def trigger_ability(self, buildings, online):
        for cooperator in buildings:
            for value in cooperator.info.ability.trigger(self, online):
                yield IncomeUp(f'{cooperator.info.name}[{"*"*cooperator.star}]', value * cooperator.star)


for name in infos.keys():
    setattr(Building, name, partial(Building, name))
