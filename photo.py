# coding: utf-8
from collections import namedtuple
from functools import partial

from ability import Ability, Target
from building import Category
from common import Status, IncomeUp


class Photo(object):
    def __init__(self, abilities):
        self.abilities = abilities

    def trigger(self, building, online):
        for value in self.abilities.trigger(building, online):
            yield IncomeUp('照片', value)


# class PhotoSet(object):
#     def __init__(self, *photos):
#         self.photos = photos

#     def trigger(self, building, online):
#         for photo in self.photos:
#             for value in photo.trigger(building, online):
#                 yield value
