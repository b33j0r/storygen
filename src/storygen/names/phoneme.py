#! /usr/bin/env python
from storygen.utility.paths import FilePaths


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


def load_phonemes(name="phonemes.txt"):
    with (FilePaths.data_dir / name).open() as f:
        return [Phoneme(line.strip()) for line in f if line.strip()]


def main():
    phonemes = load_phonemes()
    for ph in phonemes:
        print(ph)


if __name__ == "__main__":
    main()
