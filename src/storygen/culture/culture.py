#! /usr/bin/env python
from storygen.languages.word import WordValidator


class Culture:

    default_first_name_validator = WordValidator(min_length=4, max_length=6, max_vowels=2, max_consonants=2)
    default_last_name_validator = WordValidator(min_length=4, max_length=14, max_vowels=2, max_consonants=5)

    def __init__(self, language):
        self.language = language
        self.first_name_validator = self.default_first_name_validator
        self.last_name_validator = self.default_last_name_validator
