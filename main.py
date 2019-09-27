# coding: utf-8
from functools import reduce
from collections import namedtuple
from itertools import combinations, product, chain

from building import Building, Category
from photo import Photo, PhotoSet
from policy import PolicySet, Policy, Light
from task import Task

units = ['', 'K', 'M', 'B']

policies = PolicySet(
    Policy('一带一路建设', 5),
    Policy('自由贸易区建设', 4),
    Policy('区域协调发展', 3),
    Light(0.2)
)

photos = PhotoSet(
    Photo('中共一大会址'),
    Photo('豫园'),
    Photo('东方明珠电视塔'),
    Photo('浦东新区、自贸区'),
    Photo('上海美术电影制片厂'),
    Photo('石库门'),
    Photo('太湖'),
    Photo('昆曲'),
    Photo('大闸蟹'),
    Photo('南京长江大桥'),
    Photo('花果山'),
    Photo('华西村'),
    Photo('雨花台'),
    Photo('西湖'),
    Photo('世界互联网大会'),
    Photo('义乌小商品'),
    Photo('普陀山'),
    Photo('宁波舟山港'),
    Photo('绿水青山就是金山银山理念')
)

all_buildings = [
    Building('便利店', 2, 200),
    Building('钢结构房', 2, 200),
    Building('平房', 2, 150),
    Building('居民楼', 2, 175),
    Building('造纸厂', 2, 175),
    Building('钢铁厂', 2, 175),
    Building('学校', 2, 175),
    Building('菜市场', 2, 83),
    Building('木材厂', 2, 175),
    Building('木屋', 2, 200),
    Building('服装店', 2, 50),
    Building('企鹅机械', 1, 150),
    Building('民食斋', 1, 148),
    Building('图书城', 1, 175),
    Building('纺织厂', 1, 100),
    Building('五金店', 1, 80),
    Building('食品厂', 1, 75),
    Building('人才公寓', 1, 50),
    Building('零件厂', 1, 50),
]

task = Task('服务示范区')

CombinationIncome = namedtuple(
    'CombinationIncome', ('online', 'offline', 'buildings', 'online_detail', 'offline_detail'))


def calculate_income(buildings, photos, policies, task):
    online_incomes = [(building.info.name, building.calculate_income(
        True, buildings, photos, policies, task)) for building in buildings]
    offline_incomes = [(building.info.name, building.calculate_income(
        False, buildings, photos, policies, task)) for building in buildings]
    online_total = reduce(
        lambda x, y: x+y[1].base + y[1].up, online_incomes, 0)
    offline_total = reduce(
        lambda x, y: x+y[1].base + y[1].up, offline_incomes, 0)
    building_names = [building.info.name for building in buildings]
    return CombinationIncome(online_total, offline_total, building_names, online_incomes, offline_incomes)


def split_buildings(buildings):
    return list(filter(lambda x: x.info.category == Category.House, buildings)), \
        list(filter(lambda x: x.info.category == Category.Business, buildings)), \
        list(filter(lambda x: x.info.category == Category.Industry, buildings))


def format_income(value):
    unit = 0
    while value >= 1000:
        unit += 1
        value = value / 1000
    return f'{value:.2f}{units[unit]}'


target_level = None
# target_level = 175


def format_reasons(reasons):
    return ', '.join(map(lambda x: f'{x.reason}+{x.value}', reasons))


if __name__ == '__main__':
    if target_level is not None:
        for building in all_buildings:
            building.set_level(target_level)
    best_online = None
    best_offline = None
    house, business, industry = split_buildings(all_buildings)
    house_combinations = list(combinations(house, 3))
    business_combinations = list(combinations(business, 3))
    industry_combinations = list(combinations(industry, 3))
    for buildings in product(house_combinations, business_combinations, industry_combinations):
        buildings = list(chain(*buildings))
        income = calculate_income(buildings, photos, policies, task)
        if best_online is None:
            best_online = income
            best_offline = income
            continue
        if best_online.online < income.online or best_online.online == income.online and best_online.offline < income.offline:
            best_online = income
        if best_offline.offline < income.offline or best_offline.offline == income.offline and best_offline.online < income.online:
            best_offline = income
    print(
        f'best online income {format_income(best_online.online)}, with offline income {format_income(best_online.offline)}')
    for name, info in best_online.online_detail:
        print(
            f'\t{name}: {format_income(info.base)} +{format_income(info.up)} (+{info.up_ratio*100:0.2f}%)')
        for reason in info.reasons:
            print(f'\t\t{reason.reason}: +{reason.value}')
    print()
    print(
        f'best offline income {format_income(best_offline.offline)}, with online income {format_income(best_offline.online)}')
    for name, info in best_offline.offline_detail:
        print(
            f'\t{name}: {format_income(info.base)} +{format_income(info.up)} (+{info.up_ratio*100:0.2f}%)')
        for reason in info.reasons:
            print(f'\t\t{reason.reason}: +{reason.value}')
