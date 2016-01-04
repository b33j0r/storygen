#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)


class Phoneme:
    """
    """

    def __init__(self, p):
        self.p = p

    def __str__(self):
        return self.p

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.p)

    def __len__(self):
        return len(self.p)

    def __lt__(self, other):
        return str(self) < str(other)


ALPHA = Phoneme('^')
OMEGA = Phoneme('$')


def load_phonemes():
    import codecs
    from storygen.utility.shared import project_path
    with codecs.open(project_path("data", "phonemes.txt"), 'r', 'utf-8') as f:
        return [Phoneme(l.strip()) for l in f if l.strip()]


def main():
    phonemes = load_phonemes()
    for ph in phonemes:
        print(ph)


if __name__ == "__main__":
    main()
