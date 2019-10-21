# coding: utf-8
from collections import namedtuple, defaultdict
from decimal import Decimal
from functools import reduce

from ability import Ability, AbilitySet, GeneralStepAbility
from common import Category, Quality


star_ratios = tuple(map(Decimal, (0, 1, 2, 6, 24, 120)))


RatioUp = namedtuple('RatioUp', ('reason', 'value'))


class Building(object):
    def __init__(self, name, category, quality, base_ratio, abilities, stars=0):
        self.name = name
        self.category = category
        self.quality = quality
        self.base_ratio = Decimal(base_ratio)
        self.abilities = abilities
        self.stars = stars

    def star(self, stars):
        self.stars = stars
        return self

    def ability(self, abilities):
        self.abilities = abilities
        return self

    def __repr__(self):
        return f'{self.name}[{"*"*self.stars}]'

    def prepare(self, buildings, abilities):
        self.global_ratios = {
            True: sorted([RatioUp(name, ability.trigger(True, self)) for name, ability in abilities.items()]),
            False: sorted([RatioUp(name, ability.trigger(False, self)) for name, ability in abilities.items()]),
        }
        self.global_ratio = {
            True: Decimal(reduce(lambda x, y: x * (y.value + 1), self.global_ratios[True], 1)),
            False: Decimal(reduce(lambda x, y: x * (y.value + 1), self.global_ratios[False], 1)),
        }
        self.building_ratios = {
            True: {building.name: building.abilities.trigger(True, self, building.stars) for building in buildings if building.ability},
            False: {building.name: building.abilities.trigger(False, self, building.stars) for building in buildings if building.ability},
        }
        self.building_ratios = {
            True: {key: value for key, value in self.building_ratios[True].items() if value},
            False: {key: value for key, value in self.building_ratios[False].items() if value},
        }

    def trigger(self, online, buildings):
        building_ratios = self.building_ratios[online]
        building_ratios = [RatioUp(repr(building), building_ratios[building.name])
                           for building in buildings if building.name in building_ratios]
        building_ratio = Decimal(sum(up.value for up in building_ratios) + 1)
        details = [RatioUp('基础', self.base_ratio),
                   RatioUp('星级', star_ratios[self.stars])] + \
            building_ratios + \
            self.global_ratios[online]
        ratio = self.base_ratio * \
            building_ratio * \
            star_ratios[self.stars] * \
            self.global_ratio[online]
        return ratio, details


木屋 = Building('木屋', Category.住宅, Quality.普通, 1.0,
              Ability.木材厂(1.0))
居民楼 = Building('居民楼', Category.住宅, Quality.普通, 1.0,
               Ability.便利店(1.0))
钢结构房 = Building('钢结构房', Category.住宅, Quality.普通, 1.0,
                Ability.钢铁厂(1.0))
平房 = Building('平房', Category.住宅, Quality.普通, 1.1,
              Ability.住宅(0.2))
小型公寓 = Building('小型公寓', Category.住宅, Quality.普通, 1.18, AbilitySet())
人才公寓 = Building('人才公寓', Category.住宅, Quality.稀有, 1.4,
                AbilitySet([Ability.在线(0.2), Ability.工业(0.15)]))
花园洋房 = Building('花园洋房', Category.住宅, Quality.稀有, 1.02,
                Ability.商贸中心(1.0))
中式小楼 = Building('中式小楼', Category.住宅, Quality.稀有, 1.0,
                AbilitySet([Ability.在线(0.2), Ability.住宅(0.15)]))
空中别墅 = Building('空中别墅', Category.住宅, Quality.史诗, 1.0,
                AbilitySet([Ability.民食斋(1.0), Ability.在线(0.2)]))
复兴公馆 = Building('复兴公馆', Category.住宅, Quality.史诗, 1.0,
                Ability.离线(0.1))

便利店 = Building('便利店', Category.商业, Quality.普通, 1.0,
               Ability.居民楼(1.0))
五金店 = Building('五金店', Category.商业, Quality.普通, 1.0,
               Ability.零件厂(1.0))
服装店 = Building('服装店', Category.商业, Quality.普通, 1.0,
               Ability.纺织厂(1.0))
菜市场 = Building('菜市场', Category.商业, Quality.普通, 1.0,
               Ability.食品厂(1.0))
学校 = Building('学校', Category.商业, Quality.普通, 1.0,
              Ability.图书城(1.0))
图书城 = Building('图书城', Category.商业, Quality.稀有, 1.0,
               AbilitySet([Ability.学校(1.0), Ability.造纸厂(1.0)]))
商贸中心 = Building('商贸中心', Category.商业, Quality.稀有, 1.0,
                Ability.花园洋房(1.0))
加油站 = Building('加油站', Category.商业, Quality.稀有, 1.2,
               AbilitySet([Ability.人民石油(0.5), Ability.离线(0.1)]))
民食斋 = Building('民食斋', Category.商业, Quality.史诗, 1.52,
               AbilitySet([Ability.空中别墅(1.0), Ability.在线(0.2)]))
媒体之声 = Building('媒体之声', Category.商业, Quality.史诗, 1.615,
                AbilitySet([Ability.离线(0.1), Ability.所有(0.05)]))

木材厂 = Building('木材厂', Category.工业, Quality.普通, 1.0,
               Ability.木屋(1.0))
食品厂 = Building('食品厂', Category.工业, Quality.普通, 1.0,
               Ability.菜市场(1.0))
造纸厂 = Building('造纸厂', Category.工业, Quality.普通, 1.0,
               Ability.图书城(1.0))
水厂 = Building('水厂', Category.工业, Quality.普通, 1.26,
              GeneralStepAbility((False, 0.1, 0.05)))
电厂 = Building('电厂', Category.工业, Quality.普通, 1.18,
              Ability.在线(0.1))
钢铁厂 = Building('钢铁厂', Category.工业, Quality.稀有, 1.0,
               AbilitySet([Ability.钢结构房(1.0), Ability.工业(0.15)]))
纺织厂 = Building('纺织厂', Category.工业, Quality.稀有, 1.0,
               AbilitySet([Ability.服装店(1.0), Ability.商业(0.15)]))
零件厂 = Building('零件厂', Category.工业, Quality.稀有, 1.0,
               AbilitySet([Ability.五金店(1.0), Ability.企鹅机械(0.5)]))
企鹅机械 = Building('企鹅机械', Category.工业, Quality.史诗, 1.33,
                AbilitySet([Ability.零件厂(1.0), Ability.所有(0.1)]))
人民石油 = Building('人民石油', Category.工业, Quality.史诗, 1.0,
                AbilitySet([Ability.加油站(1.0), Ability.离线(0.1)]))
