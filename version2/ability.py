# coding: utf-8
from functools import reduce

from common import Category


class GeneralAbility(float):
    def trigger(self, online, building, times=1.0):
        return self * times


class OnlineAbility(float):
    def trigger(self, online, building, times=1.0):
        return self * times if online else None


class OfflineAbility(float):
    def trigger(self, online, building, times=1.0):
        return None if online else self * times


class HouseAbility(float):
    def trigger(self, online, building, times=1.0):
        return self * times if building.category == Category.住宅 else None


class BusinessAbility(float):
    def trigger(self, online, building, times=1.0):
        return self * times if building.category == Category.商业 else None


class IndustryAbility(float):
    def trigger(self, online, building, times=1.0):
        return self * times if building.category == Category.工业 else None


class BuildingAbility(str):
    def __call__(self, value):
        return BuildingAbilityInstance((self, value))


class BuildingAbilityInstance(tuple):
    def trigger(self, online, building, times=1.0):
        return self[1] * times if building.name == self[0] else None


class Ability(object):
    所有 = GeneralAbility
    在线 = OnlineAbility
    离线 = OfflineAbility
    住宅 = HouseAbility
    商业 = BusinessAbility
    工业 = IndustryAbility

    木屋 = BuildingAbility('木屋')
    居民楼 = BuildingAbility('居民楼')
    钢结构房 = BuildingAbility('钢结构房')
    平房 = BuildingAbility('平房')
    小型公寓 = BuildingAbility('小型公寓')
    人才公寓 = BuildingAbility('人才公寓')
    花园洋房 = BuildingAbility('花园洋房')
    中式小楼 = BuildingAbility('中式小楼')
    空中别墅 = BuildingAbility('空中别墅')
    复兴公馆 = BuildingAbility('复兴公馆')
    便利店 = BuildingAbility('便利店')
    五金店 = BuildingAbility('五金店')
    服装店 = BuildingAbility('服装店')
    菜市场 = BuildingAbility('菜市场')
    学校 = BuildingAbility('学校')
    图书城 = BuildingAbility('图书城')
    商贸中心 = BuildingAbility('商贸中心')
    加油站 = BuildingAbility('加油站')
    民食斋 = BuildingAbility('民食斋')
    媒体之声 = BuildingAbility('媒体之声')
    木材厂 = BuildingAbility('木材厂')
    食品厂 = BuildingAbility('食品厂')
    造纸厂 = BuildingAbility('造纸厂')
    水厂 = BuildingAbility('水厂')
    电厂 = BuildingAbility('电厂')
    钢铁厂 = BuildingAbility('钢铁厂')
    纺织厂 = BuildingAbility('纺织厂')
    零件厂 = BuildingAbility('零件厂')
    企鹅机械 = BuildingAbility('企鹅机械')
    人民石油 = BuildingAbility('人民石油')


class AbilitySet(list):
    def trigger(self, online, building, times=1):
        values = (ability.trigger(online, building) for ability in self)
        values = (value for value in values if value)
        return sum(values) * times
