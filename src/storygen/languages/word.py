#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

from storygen.names.phoneme import ALPHA, OMEGA
from storygen.utility.probability import prng


class Word:

    def __init__(self, phonemes):
        self.phonemes = phonemes
        self._str = "".join(str(p) for p in self.phonemes)
        self._hash = hash(self._str)

    def __str__(self):
        return self._str

    def __len__(self):
        return len(str(self))

    def __lt__(self, other):
        return str(self) < str(other)

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return self._hash


class WordGenerator:

    def __init__(self):
        pass

    def __call__(self, language):
        from bisect import bisect
        w = [ALPHA]
        while w[-1] is not OMEGA:
            choices, cdf = language.phoneme_cdf[w[-1]]
            x = prng.random_sample()
            i = bisect(cdf, x)
            w.append(choices[i])
        phonemes = w[1:-1]
        return Word(phonemes)


class WordValidator:

    def __init__(self, min_length=4, max_length=6, max_vowels=2, max_consonants=2, allow_repetition=False):
        import re
        self.min_length = min_length
        self.max_length = max_length
        self.max_vowels_re = re.compile(r"[aeiouy]{%d,}" % (max_vowels+1))
        self.max_consonants_re = re.compile(r"[^aeiouy]{%d,}" % (max_consonants+1))
        self.allow_repetition = allow_repetition

    def partial_validation(self, word):
        w = str(word)
        if len(w) > self.max_length:
            return False

    def __call__(self, word):
        w = str(word)
        if len(w) < self.min_length:
            return False
        if self.max_vowels_re.search(w):
            return False
        if self.max_consonants_re.search(w):
            return False
        if not self.allow_repetition:
            for i in range(1, len(word.phonemes)):
                if word.phonemes[i-1] == word.phonemes[i]:
                    return False
        return True
