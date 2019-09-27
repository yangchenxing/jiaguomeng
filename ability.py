#coding: utf-8
from common import Category, Status


class Target(object):
    def __init__(self, *targets):
        self.targets = set(targets)
        self.all = Category.All in targets

    def match(self, building):
        return self.targets and (self.all or building.info.category in self.targets or building.info.name in self.targets)

    def validate(self, buildings):
        for target in self.targets:
            if target not in Category.values and target not in buildings:
                raise Exception(f'invalid ability target: {target}')


Target.All = Target(Category.All)
Target.House = Target(Category.House)
Target.Business = Target(Category.Business)
Target.Industry = Target(Category.Industry)
Target.Empty = Target()


class Ability(object):
    def __init__(self, target, value, status=Status.Any):
        self.target = target
        self.status = status
        self.value = value

    def trigger(self, building, online):
        if self.target.match(building):
            if self.status == Status.Any or self.status == Status.OnlineOnly and online or self.status == Status.OfflineOnly and not online:
                yield self.value

    def validate(self, buildings):
        self.target.validate(buildings)


Ability.Empty = Ability(Target.Empty, 0.0)


class AbilitySet(object):
    def __init__(self, *abilities):
        self.abilities = abilities

    def trigger(self, building, online):
        for ability in self.abilities:
            for value in ability.trigger(building, online):
                yield value

    def validate(self, buildings):
        for ability in self.abilities:
            ability.validate(buildings)


AbilitySet.Empty = AbilitySet()
