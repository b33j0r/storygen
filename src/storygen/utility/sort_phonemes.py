#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import codecs

from storygen.utility.shared import project_path


def main():
    ph_file_path = project_path("data", "phonemes.txt")
    with codecs.open(ph_file_path, 'r', 'utf-8') as f:
        phonemes = [l.strip() for l in f if l.strip()]
    original = phonemes
    phonemes = set(phonemes)
    if len(original) != len(phonemes):
        print("Removed {} duplicates".format(len(original) - len(phonemes)))
    phonemes = sorted(phonemes)
    with codecs.open(ph_file_path, 'w', 'utf-8') as f:
        for ph in phonemes:
            f.write(ph + "\n")


if __name__ == "__main__":
    main()
