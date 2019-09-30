# coding: utf-8
from itertools import combinations, product, chain

from progressbar import progressbar

from building import Building
from ability import Ability, AbilitySet
from common import Category


all_buildings = [
    Building.木屋(3),
    Building.居民楼(4),
    Building.钢结构房(3),
    Building.平房(3),
    Building.小型公寓(3),
    Building.人才公寓(2),
    Building.花园洋房(1),
    Building.中式小楼(1),
    # Building.空中别墅(0),
    # Building.复兴公馆(0),
    Building.便利店(4),
    Building.五金店(3),
    Building.服装店(4),
    Building.菜市场(4),
    Building.学校(3),
    Building.图书城(2),
    Building.商贸中心(1),
    Building.加油站(1),
    Building.民食斋(2),
    Building.媒体之声(1),
    Building.木材厂(4),
    Building.食品厂(3),
    Building.造纸厂(4),
    Building.水厂(3),
    Building.电厂(3),
    Building.钢铁厂(3),
    Building.纺织厂(2),
    Building.零件厂(2),
    Building.企鹅机械(1),
    Building.人民石油(1),
]


global_abilities = {
    '照片': AbilitySet([
        Ability.所有(1.2),
        Ability.在线(1.2),
        Ability.离线(1.4),
        Ability.住宅(2.4),
        Ability.商业(2.4),
        Ability.工业(2.1),
    ]),
    '政策': AbilitySet([
        Ability.所有(0.55),  # 家国之光
        Ability.所有(1.00),  # 一带一路建设[5]
        Ability.商业(3.00),  # 自由贸易区建设[5]
        Ability.住宅(3.00),  # 区域协同发展[5]
        Ability.所有(2.00),  # 全面深化改革[5]
        Ability.在线(1.50),  # 全面依法治国[4]
        Ability.离线(2.00),  # 科教兴国[5]
        Ability.工业(6.00),  # 创新驱动[5]
        Ability.工业(0.00),  # 制造强国[0]
        Ability.所有(0.40),  # 减税降费[1]
        Ability.商业(1.20),  # 普惠金融[1]
    ]),
    '任务': AbilitySet([
        Ability.食品厂(1.0),
        Ability.菜市场(1.0),
    ])
}

# 预计算
for building in all_buildings:
    building.prepare(all_buildings, global_abilities)

# 拆分建筑
house_buildings = [
    building for building in all_buildings if building.category == Category.住宅]
business_buildings = [
    building for building in all_buildings if building.category == Category.商业]
industry_buildings = [
    building for building in all_buildings if building.category == Category.工业]

# 分类内组合
house_combinations = list(combinations(house_buildings, 3))
business_combinations = list(combinations(business_buildings, 3))
industry_combinations = list(combinations(industry_buildings, 3))

# 类间组合
all_combinations = list(
    product(house_combinations, business_combinations, industry_combinations))

best_total_ratio = None
# 遍历类间组合，寻找离线最大值
for house, business, industry in progressbar(all_combinations):
    buildings = list(chain(house, business, industry))
    ratios = [building.trigger(False, buildings) for building in buildings]
    total_ratios = sum(ratio[0] for ratio in ratios)
    if best_total_ratio is None:
        best_total_ratio = (total_ratios, buildings, ratios)
        continue
    if best_total_ratio[0] < total_ratios:
        best_total_ratio = (total_ratios, buildings, ratios)

best_total_ratio, buildings, ratios = best_total_ratio
print(f'最佳总倍率: {best_total_ratio:>5.2f}x')
for building, ratio_info in zip(buildings, ratios):
    ratio, details = ratio_info
    print(f'\t{building!r}: {ratio:>5.2f}x')
    for reason, value in details:
        print(f'\t\t{reason:<20}: {value:>5.2f}x')
