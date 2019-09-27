# coding: utf-8
from collections import namedtuple
from enum import Enum
from itertools import chain
from functools import reduce, partial


from ability import Ability, AbilitySet, Target
from common import Category, Status

_income_base = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11,
                14, 17, 21, 27, 33, 42, 53, 66, 83, 104]


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
    Info('小型公寓', Category.House, Quality.Normal, 1.0, AbilitySet.Empty),
    Info('人才公寓', Category.House, Quality.Rare, 1.4,
         AbilitySet(Ability(Target.All, 0.2, Status.OnlineOnly), Ability(Target.Industry, 0.15))),
    Info('花园洋房', Category.House, Quality.Rare, 1.0,
         AbilitySet(Ability(Target('商贸中心'), 1.0))),
    Info('中式小楼', Category.House, Quality.Rare, 1.0,
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
    Info('媒体之声', Category.Business, Quality.Epic, 1.0,
         AbilitySet(Ability(Target.All, 0.1, Status.OfflineOnly), Ability(Target.All, 0.5))),

    Info('木材厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('木屋'), 1.0))),
    Info('食品厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('菜市场'), 1.0))),
    Info('造纸厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target('图书城'), 1.0))),
    Info('水厂', Category.Industry, Quality.Normal, 1.0,
         AbilitySet(Ability(Target.All, 0.1, Status.OfflineOnly))),
    Info('电厂', Category.Industry, Quality.Normal, 1.0,
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

IncomeUp = namedtuple('IncomeUp', ('reason', 'value'))

IncomeInfo = namedtuple('IncomeInfo', ('base', 'up', 'up_ratio', 'reasons'))


class Building(object):
    def __init__(self, name, star, level):
        self.info = infos[name]
        self.star = star
        self.level = level
        self.income = self._calculate_base_income()

    def set_level(self, level):
        self.level = level
        self.income = self._calculate_base_income()

    def __str__(self):
        return self.info.name

    def __repr__(self):
        return self.info.name

    def _calculate_base_income(self):
        n = (self.level - 1) // 10
        return (sum(_income_base[: n]) * 10 +
                _income_base[n] * (self.level - n * 10)) * self.star * self.info.coefficient

    def calculate_income(self, online, buildings, photos, policies, task):
        # 建筑加成
        building_reasons = list(self.trigger_ability(buildings, online))
        building_up = sum(up.value for up in building_reasons)
        # 照片加成
        photo_reasons = list(photos.trigger(self, online))
        photo_up = sum(up.value for up in photo_reasons)
        # 政策加成
        policy_reasons = list(policies.trigger(self, online))
        policy_up = sum(up.value for up in policy_reasons)
        # 任务加成
        task_reasons = list(task.trigger(self, online))
        task_up = sum(up.value for up in task_reasons)
        total_up = (1+building_up) * (1+photo_up) * \
            (1+policy_up) * (1+task_up) - 1
        base = self.income * (0.5 if not online else 1.0)
        return IncomeInfo(base, base * total_up, total_up, list(chain(building_reasons, photo_reasons, policy_reasons, task_reasons)))

    def trigger_ability(self, buildings, online):
        for cooperator in buildings:
            for value in cooperator.info.ability.trigger(self, online):
                yield IncomeUp(f'{cooperator.info.name}[{"⭑"*cooperator.star}]', value * cooperator.star)
