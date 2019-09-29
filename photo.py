# coding: utf-8
from collections import namedtuple
from functools import partial

from ability import Ability, Target
from building import Category
from common import Status, IncomeUp

Info = namedtuple('Info', ('name', 'region', 'ability'))

infos = [
    Info('中共一大会址', '上海', Ability(Target.All, 0.1, Status.OfflineOnly)),
    Info('豫园', '上海', Ability(Target.All, 0.1, Status.OfflineOnly)),
    Info('东方明珠电视塔', '上海', Ability(Target.All, 0.1)),
    Info('世博会中国馆', '上海', Ability(Target.All, 0.1, Status.OnlineOnly)),
    Info('外滩', '上海', Ability(Target.Business, 0.3)),
    Info('浦东新区自贸区', '上海', Ability(Target.Industry, 0.3)),
    Info('中国国际进口博览会', '上海', Ability.Empty),
    Info('上海美术电影制片厂', '上海', Ability(Target.Business, 0.3)),
    Info('石库门', '上海', Ability(Target.House, 0.3)),
    Info('本帮菜', '上海', Ability(Target.House, 0.3)),

    Info('太湖', '江苏', Ability(Target.All, 0.1, Status.OnlineOnly)),
    Info('昆曲', '江苏', Ability(Target.All, 0.1, Status.OnlineOnly)),
    Info('江南园林', '江苏', Ability(Target.All, 0.1, Status.OfflineOnly)),
    Info('大闸蟹', '江苏', Ability.Empty),
    Info('南京长江大桥', '江苏', Ability(Target.All, 0.1)),
    Info('花果山', '江苏', Ability(Target.All, 0.1, Status.OfflineOnly)),
    Info('华西村', '江苏', Ability(Target.House, 0.3)),
    Info('淮扬菜', '江苏', Ability(Target.House, 0.3)),
    Info('宜兴紫砂壶', '江苏', Ability(Target.Business, 0.3)),
    Info('雨花台', '江苏', Ability(Target.All, 0.1, Status.OfflineOnly)),

    Info('西湖', '浙江', Ability(Target.All, 0.1)),
    Info('越剧', '浙江', Ability(Target.All, 0.1, Status.OnlineOnly)),
    Info('世界互联网大会', '浙江', Ability(Target.Business, 0.3)),
    Info('义乌小商品', '浙江', Ability(Target.Business, 0.3)),
    Info('普陀山', '浙江', Ability(Target.All, 0.1, Status.OfflineOnly)),
    Info('嘉兴南湖红船', '浙江', Ability(Target.All, 0.1, Status.OfflineOnly)),
    Info('宁波舟山港', '浙江', Ability(Target.Industry, 0.3)),
    Info('浙菜', '浙江', Ability(Target.House, 0.3)),
    Info('绿水青山就是金山银山理念', '浙江', Ability(Target.All, 0.1)),
]

infos = {info.name: info for info in infos}


class Photo(object):
    def __init__(self, name):
        self.info = infos[name]

    def trigger(self, building, online):
        for value in self.info.ability.trigger(building, online):
            yield IncomeUp(self.info.name, value)


class PhotoSet(object):
    def __init__(self, *photos):
        self.photos = photos

    def trigger(self, building, online):
        for photo in self.photos:
            for value in photo.trigger(building, online):
                yield value


for name in infos.keys():
    setattr(Photo, name, Photo(name))
