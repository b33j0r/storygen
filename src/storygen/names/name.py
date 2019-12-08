#! /usr/bin/env python


class Name:

    def __init__(self, culture, first=None, last=None):
        self.culture = culture
        if not culture:
            raise RuntimeError("Name does not have a culture!")
        if not culture.language:
            raise RuntimeError("Name does not have a culture with a language!")
        self.last = last or culture.language.word(validator=culture.last_name_validator)
        for n in range(100):
            self.first = first or culture.language.word(validator=culture.first_name_validator)
            if self.first != self.last:
                break

    def __str__(self):
        return "{} {}".format(str(self.first).title(), str(self.last).title())
