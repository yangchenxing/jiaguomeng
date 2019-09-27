#coding: utf-8
from collections import namedtuple
from building import Category

Info = namedtuple('Info', ('name', 'region', 'online',
                           'offline', 'category', 'value'))

infos = [
    Info('中共一大会址', '上海', False, True, Category.All, 0.1),
    Info('豫园', '上海', False, True, Category.All, 0.1),
    Info('东方明珠电视塔', '上海', True, True, Category.All, 0.1),
    Info('浦东新区、自贸区', '上海', True, True, Category.Industry, 0.3),
    Info('中国国际进口博览会', '上海', False, False, Category.All, 0.0),
    Info('上海美术电影制片厂', '上海', True, True, Category.Business, 0.3),
    Info('石库门', '上海', True, True, Category.House, 0.3),

    Info('太湖', '江苏', True, False, Category.All, 0.1),
    Info('昆曲', '江苏', True, False, Category.All, 0.1),
    Info('大闸蟹', '江苏', True, False, Category.All, 0.0),
    Info('南京长江大桥', '江苏', True, True, Category.All, 0.1),
    Info('花果山', '江苏', False, True, Category.All, 0.1),
    Info('华西村', '江苏', True, True, Category.House, 0.3),
    Info('雨花台', '江苏', False, True, Category.All, 0.1),

    Info('西湖', '浙江', True, True, Category.All, 0.1),
    Info('世界互联网大会', '浙江', True, True, Category.Business, 0.3),
    Info('义乌小商品', '浙江', True, True, Category.Business, 0.3),
    Info('普陀山', '浙江', False, True, Category.All, 0.1),
    Info('宁波舟山港', '浙江', True, True, Category.Industry, 0.3),
    Info('绿水青山就是金山银山理念', '浙江', True, True, Category.All, 0.1),
]

infos = {info.name: info for info in infos}


IncomeUp = namedtuple('IncomeUp', ('reason', 'value'))


class Photo(object):
    def __init__(self, name):
        self.info = infos[name]

    def calculate_income_up(self, target, online):
        if target.info.category == self.info.category or self.info.category == Category.All:
            if online and self.info.online or not online and self.info.offline:
                return IncomeUp(self.info.name, self.info.value)
        return None
