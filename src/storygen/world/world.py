#! /usr/bin/env python
import heapq
import itertools

from storygen.events.event import PlagueEvent, BirthEvent
from storygen.events.timestamp import Time, TimeDelta
from storygen.names.name import Name


def heappopwhile(predicate, heap):
    while True:
        try:
            e = heapq.heappop(heap)
        except IndexError:
            break
        if predicate(e):
            yield e
        else:
            heapq.heappush(heap, e)
            break


class World:

    def __init__(self):
        self.clock = Time(5000, 1, 1)
        self.events = []
        self.people = set()
        self.men = set()
        self.women = set()

    def schedule(self, e):
        if e.timestamp < self.clock:
            raise RuntimeError("Cannot schedule an event in the past")
        heapq.heappush(self.events, e)

    def step(self, dt=None):
        dt = dt or TimeDelta(days=1)
        self.clock += dt
        # self.log("A new day")
        population = len(self.people)
        for e in heappopwhile((lambda e: e.timestamp <= self.clock), self.events):
            e(self)
        # if population != len(self.people):
        #     print("WORLD POPULATION: {}".format(len(self.people)))
        return bool(self.events)

    def steps(self, n, dt=None):
        for i in range(n):
            yield self.step(dt=dt)

    def step_infinite(self, dt=None):
        while True:
            yield self.step(dt=dt)

    def step_all(self, dt=None):
        for e in itertools.takewhile((lambda has_events: has_events), self.step_infinite(dt=dt)):
            yield e

    def log(self, message, *args, timestamp=None, **kwargs):
        timestamp = timestamp or self.clock
        msg = message.format(*args, **kwargs)
        print("[{clock:%Y-%m-%d}] {msg}".format(clock=timestamp, msg=msg))


def main():
    initial_population = 100

    from storygen.names.phoneme import load_phonemes
    from storygen.languages.language import LanguageGenerator
    from storygen.culture.culture import Culture
    from storygen.people.person import Person

    language_gen = LanguageGenerator(load_phonemes())
    language = language_gen()
    culture = Culture(language)
    print("Language phonemes: {}".format(", ".join(sorted(str(p) for p in language.phonemes))))
    names = [Name(culture) for n in range(initial_population)]

    world = World()

    for i, name in enumerate(names):
        birthdate = world.clock
        person = Person(name, Person.MALE if (i % 2) else Person.FEMALE, birthdate, culture)
        birth = BirthEvent(person)
        world.schedule(birth)

    # world.schedule(PlagueEvent(world.clock + TimeDelta(days=100000)))

    for _ in world.step_all():
        pass

    world.log("History has ended after {} years", world.clock.year-5000)


if __name__ == "__main__":
    main()
