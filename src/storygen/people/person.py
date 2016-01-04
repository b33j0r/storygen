#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

from storygen.utility.probability import prng


class Person:

    FEMALE = 1
    MALE = 2

    def __init__(self, name, gender, birthdate, culture, father=None, mother=None):
        if not name:
            raise ValueError("Person does not have a name")
        if not gender:
            raise ValueError("Person does not have a gender")
        if not birthdate:
            raise ValueError("Person does not have a birthdate")
        if not culture:
            raise RuntimeError("Person does not have a culture")
        if bool(father) != bool(mother):
            # The seed population (Adam and Eve) can't have parents
            # by definition, but everyone else must
            raise RuntimeError(
                "Person has a {} but not a {}".format(
                    "father" if father else "mother",
                    "mother" if father else "father"
                )
            )
        self.name = name
        self.gender = gender
        self.pregnant = False
        self.birthdate = birthdate
        self.culture = culture
        self.father = father
        self.mother = mother
        self.alive = True

    def __str__(self):
        return "{} {}".format("Ms." if self.gender == self.FEMALE else "Mr.", self.name)


class OffspringGenerator:

    def __init__(self, name_generator):
        self.name_generator = name_generator

    def __call__(self, birthdate, father, mother):
        cultural_parent = father  # if prng.random_sample() > 0.2 else mother
        culture = cultural_parent.culture
        last_name = cultural_parent.name.last
        name = self.name_generator(culture=culture, last=last_name)
        gender = Person.MALE if prng.random_sample() > 0.4 else Person.FEMALE
        return Person(name, gender, birthdate, culture, father, mother)


def main():
    pass


if __name__ == "__main__":
    main()
