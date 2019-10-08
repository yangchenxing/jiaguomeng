# coding: utf-8
from itertools import combinations, product, chain

from progressbar import progressbar

import building
from ability import Ability, AbilitySet
from common import Category


all_buildings = [
    building.木屋.star(5),
    building.居民楼.star(5),
    building.钢结构房.star(5),
    building.平房.star(5),
    building.小型公寓.star(5),
    building.人才公寓.star(4),
    building.花园洋房.star(4),
    building.中式小楼.star(3),
    building.空中别墅.star(2),
    building.复兴公馆.star(3),

    building.便利店.star(5),
    building.五金店.star(5),
    building.服装店.star(5),
    building.菜市场.star(5),
    building.学校.star(5),
    building.图书城.star(4),
    building.商贸中心.star(3),
    building.加油站.star(3),
    building.民食斋.star(3),
    building.媒体之声.star(2),

    building.木材厂.star(5),
    building.食品厂.star(5),
    building.造纸厂.star(5),
    building.水厂.star(5).ability(Ability.离线固定(0.3)),
    building.电厂.star(5).ability(Ability.在线固定(1.4)),
    building.钢铁厂.star(4),
    building.纺织厂.star(4),
    building.零件厂.star(4),
    building.企鹅机械.star(3),
    building.人民石油.star(2),
]


global_abilities = {
    '照片': AbilitySet([
        Ability.所有(1.7),
        Ability.在线(2.0),
        Ability.离线(1.8),
        Ability.住宅(3.0),
        Ability.商业(3.0),
        Ability.工业(3.6),
    ]),
    '政策': AbilitySet([
        Ability.所有(0.55),  # 家国之光
        Ability.所有(1.00),  # 一带一路建设[5]
        Ability.商业(3.00),  # 自由贸易区建设[5]
        Ability.住宅(3.00),  # 区域协同发展[5]
        Ability.所有(2.00),  # 全面深化改革[5]
        Ability.在线(2.00),  # 全面依法治国[5]
        Ability.离线(2.00),  # 科教兴国[5]
        Ability.工业(6.00),  # 创新驱动[5]
        Ability.工业(12.0),  # 制造强国[5]
        Ability.所有(4.00),  # 减税降费[5]
        Ability.商业(12.0),  # 普惠金融[5]
        Ability.住宅(24.0),  # 新型城镇化[5]
        Ability.在线(0.80),  # 乡村振兴[1]
        Ability.离线(8.00),  # 精准扶贫[5]
        Ability.所有(8.00),  # 新一代人工智能[5]
    ]),
    '任务': AbilitySet([
        Ability.水厂(1.0),
        Ability.电厂(2.0),
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
    # do filter

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
        if reason in ('基础', '星级'):
            print(f'\t\t{reason:<20}: {value:>6.2f}x')
        else:
            print(f'\t\t{reason:<20}: {value:>+6.2f}x')
