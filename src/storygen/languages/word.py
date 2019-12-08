#! /usr/bin/env python
from storygen.utility.probability import MarkovChain


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

    def __init__(self, validator=None):
        self.validator = validator

    def __call__(self, language):
        phonemes = language.markov_chain()
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
        if len(word) > self.max_length:
            return False
        return True

    def __call__(self, word):
        if not self.partial_validation(word):
            return False
        if len(word) < self.min_length:
            return False
        w = str(word)
        if self.max_vowels_re.search(w):
            return False
        if self.max_consonants_re.search(w):
            return False
        if not self.allow_repetition:
            for i in range(1, len(word.phonemes)):
                if word.phonemes[i-1] == word.phonemes[i]:
                    return False
        return True
