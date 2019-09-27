# coding: utf-8
from collections import namedtuple
from enum import Enum
from itertools import chain
from functools import reduce

_income_base = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11,
                14, 17, 21, 27, 33, 42, 53, 66, 83, 104]


class Quality(Enum):
    Normal = '普通'
    Rare = '稀有'
    Epic = '史诗'


class Category(Enum):
    House = '住宅'
    Business = '商业'
    Industry = '工业'
    All = '所有'


Ability = namedtuple('Ability', ('target', 'online', 'offline', 'value'))

Info = namedtuple(
    'Info', ('name', 'category', 'quality', 'coefficient', 'abilities'))

infos = [
    Info('木屋', Category.House, Quality.Normal,
         1.0, [Ability('木材厂', True, True, 1.0)]),
    Info('平房', Category.House, Quality.Normal,
         1.1, [Ability(Category.House, True, True, 0.2)]),
    Info('居民楼', Category.House, Quality.Normal,
         1.0, [Ability('便利店', True, True, 1.0)]),
    Info('钢结构房', Category.House, Quality.Normal,
         1.0, [Ability('钢铁厂', True, True, 1.0)]),
    Info('小型公寓', Category.House, Quality.Normal, 1.0, []),
    Info('人才公寓', Category.House, Quality.Rare, 1.4,
         [Ability(Category.All, True, False, 0.2), Ability(Category.Industry, True, True, 0.15)]),
    Info('花园洋房', Category.House, Quality.Rare, 1.0,
         [Ability('商贸中心', True, True, 1.0)]),
    Info('中式小楼', Category.House, Quality.Rare, 1.0,
         [Ability(Category.All, True, False, 0.2), Ability(Category.House, True, True, 0.15)]),
    Info('空中别墅', Category.House, Quality.Epic, 1.0, [
         Ability('民食斋', True, True, 1.0), Ability(Category.All, True, False, 0.2)]),
    Info('复兴公馆', Category.House, Quality.Epic, 1.0,
         [Ability(Category.All, False, True, 0.1)]),

    Info('便利店', Category.Business, Quality.Normal,
         1.0, [Ability('居民楼', True, True, 1.0)]),
    Info('五金店', Category.Business, Quality.Normal,
         1.0, [Ability('零件厂', True, True, 1.0)]),
    Info('服装店', Category.Business, Quality.Normal,
         1.0, [Ability('纺织厂', True, True, 1.0)]),
    Info('菜市场', Category.Business, Quality.Normal,
         1.0, [Ability('食品厂', True, True, 1.0)]),
    Info('学校', Category.Business, Quality.Normal,
         1.0, [Ability('图书城', True, True, 1.0)]),
    Info('图书城', Category.Business, Quality.Rare, 1.0,
         [Ability('学校', True, True, 1.0), Ability('造纸厂', True, True, 1.0)]),
    Info('商贸中心', Category.Business, Quality.Rare,
         1.0, [Ability('花园洋房', True, True, 1.0)]),
    Info('加油站', Category.Business, Quality.Rare, 1.0,
         [Ability('人民石油', True, True, 0.5), Ability(Category.All, False, True, 0.1)]),
    Info('民食斋', Category.Business, Quality.Epic, 1.52,
         [Ability('空中别墅', True, True, 1.0), Ability(Category.All, True, False, 0.2)]),
    Info('媒体之声', Category.Business, Quality.Epic, 1.0,
         [Ability(Category.All, False, True, 0.1), Ability(Category.All, True, True, 0.5)]),

    Info('木材厂', Category.Industry, Quality.Normal,
         1.0, [Ability('木屋', True, True, 1.0)]),
    Info('食品厂', Category.Industry, Quality.Normal,
         1.0, [Ability('菜市场', True, True, 1.0)]),
    Info('造纸厂', Category.Industry, Quality.Normal,
         1.0, [Ability('图书城', True, True, 1.0)]),
    Info('水厂', Category.Industry, Quality.Normal, 1.0,
         [Ability(Category.All, False, True, 0.1)]),
    Info('电厂', Category.Industry, Quality.Normal, 1.0,
         [Ability(Category.All, True, False, 0.2)]),
    Info('钢铁厂', Category.Industry, Quality.Rare, 1.0, [
         Ability('钢结构房', True, True, 1.0), Ability(Category.Industry, True, True, 0.15)]),
    Info('纺织厂', Category.Industry, Quality.Rare, 1.0, [Ability(
        '服装店', True, True, 1.0), Ability(Category.Business, True, True, 0.15)]),
    Info('零件厂', Category.Industry, Quality.Rare, 1.0, [
         Ability('五金店', True, True, 1.0), Ability('企鹅机械', True, True, 0.5)]),
    Info('企鹅机械', Category.Industry, Quality.Epic, 1.33, [
         Ability('零件厂', True, True, 1.0), Ability(Category.All, True, True, 0.1)]),
    Info('人民石油', Category.Industry, Quality.Epic, 1.0, [
         Ability('加油站', True, True, 1.0), Ability(Category.All, False, True, 0.1)]),
]

infos = {info.name: info for info in infos}


def check_infos():
    for name, info in infos.items():
        for ability in info.abilities:
            if ability.target in (Category.All, Category.House, Category.Business, Category.Industry):
                continue
            if ability.target not in infos:
                raise Exception(f'unkonwn ability target: {ability.target}')


check_infos()


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
        building_ups = list(filter(lambda x: x, (building.calculate_income_up(
            self, online) for building in buildings)))
        building_up = sum(up.value for up in building_ups)
        photo_ups = list(filter(lambda x: x, (photo.calculate_income_up(
            self, online) for photo in photos)))
        photo_up = sum(up.value for up in photo_ups)
        policy_ups = list(filter(lambda x: x, (policy.calculate_income_up(
            self, online) for policy in policies)))
        policy_up = sum(up.value for up in policy_ups)
        task_up = task.calculate_income_up(self)
        total_up = (1+building_up) * (1+photo_up) * \
            (1+policy_up) * (1+task_up.value) - 1
        base = self.income * (0.5 if not online else 1.0)
        return IncomeInfo(base, base * total_up, total_up, list(chain(building_ups, photo_ups, policy_ups, [task_up])))

    def calculate_income_up(self, target, online):
        for ability in self.info.abilities:
            if ability.online and online or ability.offline and not online:
                if ability.target == target.info.name or ability.target == target.info.category or ability.target == Category.All:
                    return IncomeUp(self.info.name, ability.value * self.star)
        return None
