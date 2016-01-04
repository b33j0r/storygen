#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import math

from storygen.events.timestamp import TimeDelta
from storygen.names.name import Name
from storygen.people.person import Person, OffspringGenerator
from storygen.utility.probability import prng


class Event:

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __call__(self, world):
        """
        :param world:
        :type world: storygen.world.world.World
        :return:
        """
        raise NotImplementedError()

    def __str__(self):
        return "<Unspecified Event>"

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __eq__(self, other):
        return self.timestamp == other.timestamp


class BirthEvent(Event):

    def __init__(self, person):
        super(BirthEvent, self).__init__(person.birthdate)
        self.person = person

    def __call__(self, world):
        lifespan = prng.random_integers(20, 80)*365
        lifespan = TimeDelta(days=lifespan)
        lifespan = TimeDelta(days=lifespan.days)
        try:
            death_timestamp = self.timestamp + lifespan
        except OverflowError:
            world.log("Lame... {} would have been born, but the universe was due to end", self.person)
            return
        world.people.add(self.person)
        if self.person.gender == self.person.FEMALE:
            world.women.add(self.person)
        else:
            world.men.add(self.person)
        world.schedule(
            DeathEvent(
                death_timestamp,
                self.person
            )
        )
        if self.person.gender == self.person.FEMALE:
            for i in range(prng.random_integers(1, 6)):
                world.schedule(
                    FertilityEvent(
                        world.clock + TimeDelta(days=prng.random_integers(15, 45)*365),
                        self.person
                    )
                )
        if not self.person.father:
            world.log("{} was immaculately generated", self.person, timestamp=self.timestamp)
        else:
            world.log(
                "It's a {}! {} was born to {} and {} (population: {})",
                "boy" if self.person.gender == Person.MALE else "girl",
                self.person, self.person.mother, self.person.father,
                len(world.people),
                timestamp=self.timestamp
            )
            self.person.mother.pregnant = False

    def __str__(self):
        return "{} was born".format(self.person)


class FertilityEvent(Event):

    default_offspring_generator = OffspringGenerator(Name)

    def __init__(self, timestamp, person):
        super(FertilityEvent, self).__init__(timestamp)
        self.person = person
        self.offspring_generator = self.default_offspring_generator
        assert isinstance(self.offspring_generator, OffspringGenerator)

    def __call__(self, world):
        if not self.person.alive:
            # world.log("Wah waah... {} would have gotten pregnant, but passed away before her time.".format(self.person))
            return
        if self.person.pregnant:
            # world.log("Look at dem genes... {} would have gotten pregnant again, but already is!".format(self.person))
            return
        # fathers = list(filter(lambda p: p.gender == p.MALE, world.people))
        fathers = list(world.men)
        if not fathers:
            # world.log("{} was looking for a man, but there were none to be found", self.person)
            return
        father_index = prng.random_integers(0, len(fathers)-1)
        father = fathers[father_index]
        # world.log("{} is expecting a baby with {}!", self.person, father, timestamp=self.timestamp)
        child = self.default_offspring_generator(world.clock + TimeDelta(days=30*9), father, self.person)
        birth = BirthEvent(child)
        self.person.pregnant = True
        world.schedule(birth)


class DeathEvent(Event):

    def __init__(self, timestamp, person):
        super(DeathEvent, self).__init__(timestamp)
        self.person = person

    def __call__(self, world):
        if not self.person in world.people:
            return
        world.people.remove(self.person)
        try:
            world.men.remove(self.person)
        except KeyError:
            pass
        try:
            world.women.remove(self.person)
        except KeyError:
            pass
        self.person.alive = False
        world.log(
            "{} has died at the age of {}",
            self.person,
            math.floor((self.timestamp - self.person.birthdate).days/365),
            timestamp=self.timestamp
        )

    def __str__(self):
        return "{} has died".format(self.person)


class PlagueEvent(Event):

    def __init__(self, timestamp, mortality_rate=0.5, communication_factor=1):
        super(PlagueEvent, self).__init__(timestamp)
        self.mortality_rate = communication_factor

    def __call__(self, world):
        world.events = []
        for person in world.people:
            world.schedule(
                DeathEvent(world.clock + TimeDelta(days=1), person)
            )
        world.log("PLAGUE has struck!")


def main():
    pass


if __name__ == "__main__":
    pass
