#coding: utf-8
from enum import Enum


class Category(Enum):
    住宅 = 1
    商业 = 2
    工业 = 3


class Quality(Enum):
    普通 = 0
    稀有 = 1
    史诗 = 2
