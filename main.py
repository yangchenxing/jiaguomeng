# coding: utf-8
from functools import reduce
from collections import namedtuple
from itertools import combinations, product, chain
from progressbar import progressbar

from building import Building, Category
from photo import Photo, PhotoSet
from policy import PolicySet, Policy, Light
from task import Task

units = ['', 'K', 'M', 'B', 'T']

policies = PolicySet(
    Policy.一带一路建设(5),
    Policy.自由贸易区建设(5),
    Policy.区域协调发展(4),
    Policy.全面深化改革(5),
    Policy.全面依法治国(2),
    Policy.科教兴国(5),
    Policy.创新驱动(4),
    Light(0.4)
)

photos = PhotoSet(
    Photo.中共一大会址,
    Photo.豫园,
    Photo.东方明珠电视塔,
    Photo.外滩,
    Photo.浦东新区自贸区,
    Photo.上海美术电影制片厂,
    Photo.石库门,
    Photo.本帮菜,
    Photo.太湖,
    Photo.昆曲,
    Photo.大闸蟹,
    Photo.南京长江大桥,
    Photo.花果山,
    Photo.华西村,
    Photo.淮扬菜,
    Photo.宜兴紫砂壶,
    Photo.雨花台,
    Photo.西湖,
    Photo.越剧,
    Photo.世界互联网大会,
    Photo.义乌小商品,
    Photo.普陀山,
    Photo.嘉兴南湖红船,
    Photo.宁波舟山港,
    Photo.绿水青山就是金山银山理念
)

all_buildings = [
    Building.钢结构房(3, 200),
    Building.平房(3, 150),
    Building.居民楼(3, 175),
    Building.人才公寓(2, 50),
    Building.木屋(3, 200),
    Building.中式小楼(1, 100),
    Building.小型公寓(2, 150),

    Building.便利店(3, 200),
    Building.学校(3, 200),
    Building.菜市场(4, 400),
    Building.服装店(3, 275),
    Building.民食斋(2, 148),
    Building.图书城(2, 175),
    Building.五金店(2, 150),
    Building.媒体之声(1, 100),

    Building.造纸厂(4, 350),
    Building.钢铁厂(2, 350),
    Building.木材厂(3, 175),
    Building.企鹅机械(1, 150),
    Building.纺织厂(2, 175),
    Building.食品厂(2, 75),
    Building.零件厂(2, 250),
    Building.电厂(3, 100),
    Building.水厂(2, 125),
    Building.人民石油(1, 1),
]

task = Task.工业综合体

CombinationIncome = namedtuple(
    'CombinationIncome', ('online', 'offline', 'buildings', 'online_detail', 'offline_detail'))


def calculate_income(buildings):
    online_incomes = [(building.info.name, building.calculate_income(
        True, buildings)) for building in buildings]
    offline_incomes = [(building.info.name, building.calculate_income(
        False, buildings)) for building in buildings]
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


#target_level = None
target_level = 200


def format_reasons(reasons):
    return ', '.join(map(lambda x: f'{x.reason}+{x.value}', reasons))


if __name__ == '__main__':
    for building in all_buildings:
        building.calculate_building_ups(all_buildings)
    if target_level is not None:
        for building in all_buildings:
            building.set_level(target_level)
    for building in all_buildings:
        building.set_global_income_up(photos, policies, task)
    best_online = None
    best_offline = None
    house, business, industry = split_buildings(all_buildings)
    house_combinations = list(combinations(house, 3))
    business_combinations = list(combinations(business, 3))
    industry_combinations = list(combinations(industry, 3))
    for buildings in progressbar(list(product(house_combinations, business_combinations, industry_combinations))):
        buildings = list(chain(*buildings))
        income = calculate_income(buildings)
        if best_online is None:
            best_online = income
            best_offline = income
            continue
        if best_online.online < income.online or best_online.online == income.online and best_online.offline < income.offline:
            best_online = income
        if best_offline.offline < income.offline or best_offline.offline == income.offline and best_offline.online < income.online:
            best_offline = income
        break
    print(
        f'best online income {format_income(best_online.online)}, with offline income {format_income(best_online.offline)}')
    print(f'\t{", ".join(x[0] for x in best_online.online_detail)}')
    for name, info in best_online.online_detail:
        print(
            f'\t{name}: {format_income(info.base)} +{format_income(info.up)} (+{info.up_ratio*100:0.2f}%)')
        for reason in info.reasons:
            print(f'\t\t{reason.reason:<16}: +{reason.value*100:.2f}%')
    print()
    print(
        f'best offline income {format_income(best_offline.offline)}, with online income {format_income(best_offline.online)}')
    print(f'\t{", ".join(x[0] for x in best_offline.offline_detail)}')
    for name, info in best_offline.offline_detail:
        print(
            f'\t{name}: {format_income(info.base)} +{format_income(info.up)} (+{info.up_ratio*100:0.2f}%)')
        for reason in info.reasons:
            print(f'\t\t{reason.reason:<16}: +{reason.value*100:.2f}%')
