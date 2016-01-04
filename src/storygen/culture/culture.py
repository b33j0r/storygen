#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

from storygen.languages.word import WordValidator


class Culture:

    default_first_name_validator = WordValidator(min_length=4, max_length=6, max_vowels=2, max_consonants=2)
    default_last_name_validator = WordValidator(min_length=4, max_length=10, max_vowels=2, max_consonants=5)

    def __init__(self, language):
        self.language = language
        self.first_name_validator = self.default_first_name_validator
        self.last_name_validator = self.default_last_name_validator
