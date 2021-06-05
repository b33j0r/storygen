#! /usr/bin/env python
import bisect
import json
import logging
import random
from dataclasses import dataclass
from typing import Callable

from storygen.log import get_logger

logger = get_logger("storygen.app")


def weighted_dict_to_cummulative_distribution(choice_dct):
    keys, weights = zip(*choice_dct.items())
    total = float(sum(weights))
    probs = [v/total for v in weights]
    cdf = [probs[0]]
    for i in range(1, len(probs)):
        cdf.append(cdf[-1] + probs[i])
    return keys, cdf


@dataclass
class LanguageSpec:
    phonemes: list[str]
    min_name_length: int = 4
    brevity_factor: int = random.randint(10, 80)


class Language:
    def __init__(self, spec: LanguageSpec):
        self.spec = spec

        phonemes = set(spec.phonemes)

        self.initial_phonemes = set(random.sample(tuple(phonemes), len(phonemes) // 4))
        self.ending_phonemes = set(random.sample(tuple(phonemes - self.initial_phonemes), len(phonemes) // 4))
        self.other_phonemes = phonemes - self.initial_phonemes - self.ending_phonemes

        # Calculate weighted transitions for phonemes chosen as prefixes
        self.weighted_transitions = {
            None: {
                p: random.randint(3, 10) for p in self.initial_phonemes
            }
        }

        # Calculate weighted transitions for phonemes not chosen as prefixes nor suffixes
        for phoneme in self.other_phonemes.union(self.initial_phonemes):
            self.weighted_transitions[phoneme] = {
                p: random.randint(3, 10) for p in self.other_phonemes.union(self.ending_phonemes)
            }
            self.weighted_transitions[phoneme][None] = spec.brevity_factor

        # Calculate weighted transitions for phonemes chosen as suffixes
        for phoneme in self.ending_phonemes:
            self.weighted_transitions[phoneme] = {None: 1000}

    def gen_name(self):
        transition_probs = {
            k: weighted_dict_to_cummulative_distribution(d)
            for k, d in self.weighted_transitions.items()
        }

        phonemes = []
        state = None
        for i in range(5):
            try:
                possible_phonemes, cdf = transition_probs[state]
            except KeyError:
                if not phonemes:
                    continue
                break
            x = random.random()
            b = bisect.bisect(cdf, x)
            p = possible_phonemes[b]
            if p is None:
                break
            phonemes.append(p)
            state = p

        return "".join(phonemes)

    def gen_names(self, n=10):
        names = set()
        for i in range(n ** 3):
            name = self.gen_name()
            if len(name) < self.spec.min_name_length:
                continue
            names.add(name)
            if len(names) >= n:
                break
        return names


class NameFormats:

    @classmethod
    def default(cls, first, last):
        return cls.first_space_last(first, last)

    @classmethod
    def first_space_last(cls, first, last):
        return f"{first} {last}"

    @classmethod
    def last_comma_first(cls, first, last):
        return f"{last}, {first}"


NameFormatter = Callable[[str, str], str]


def gen_full_names(language, num_last_names=3, num_first_names=5):
    for last_name in language.gen_names(n=num_last_names):
        for first_name in language.gen_names(n=num_first_names):
            yield last_name, first_name


def main(
    full_name_format: NameFormatter = NameFormats.default,
    num_last_names: int = 30,
    num_first_names: int = 10,
):
    from storygen.log import init_logging

    init_logging()

    phonemes = (
        "bra", "kah", "to", "ro", "for", "mo", "ter", "je", "jo", "mel",
        "din", "ger", "tog", "tag", "nar", "bar", "la",
        "sha", "ial", "bia", "fra", "dar", "mis", "fang",
        "ke", "ike", "ye", "ya", "yek", "el", "pia", "del", "er", "es",
        "qi", "nin",
    )
    phonemes = sorted(set(phonemes))

    spec = LanguageSpec(phonemes=phonemes)
    logger.debug("language spec: %s", spec)

    language = Language(spec)

    names = gen_full_names(
        language,
        num_last_names=num_last_names,
        num_first_names=num_first_names,
    )

    for i, (last_name, first_name) in enumerate(names):
        full_name = full_name_format(first_name, last_name)
        logger.info(f"{i+1:04d}    {full_name.title()}")


if __name__ == "__main__":
    main()
