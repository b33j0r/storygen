#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import random
from bisect import bisect
from collections import OrderedDict
from pprint import pprint


class PhonemePosition:
    START = 1
    END = -1
    INTERIOR = 2
    ANY = 0


def weighted_dict_to_cummulative_distribution(choice_dct):
    keys, weights = zip(*choice_dct.items())
    total = float(sum(weights))
    probs = [v/total for v in weights]
    cdf = [probs[0]]
    for i in range(1, len(probs)):
        cdf.append(cdf[-1] + probs[i])
    return keys, cdf


def gen_name(weighted_transitions):
    transition_probs = {
        k: weighted_dict_to_cummulative_distribution(d)
        for k, d in weighted_transitions.items()
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
        b = bisect(cdf, x)
        p = possible_phonemes[b]
        if p is None:
            break
        phonemes.append(p)
        state = p

    return "".join(phonemes)


def gen_names(weighted_transitions, n=10, min_length=4):
    names = set()
    for i in range(n*n):
        name = gen_name(weighted_transitions)
        if len(name) < min_length:
            continue
        names.add(name)
        if len(names) >= n:
            break
    return names


def gen_language(phonemes, brevity_factor=10):
    phonemes = set(phonemes)
    initial_phonemes = set(random.sample(phonemes, len(phonemes)//4))
    ending_phonemes = set(random.sample(phonemes - initial_phonemes, len(phonemes)//4))
    other_phonemes = phonemes - initial_phonemes - ending_phonemes
    weighted_transitions = {
        None: {
            p: random.randint(3, 10) for p in initial_phonemes
        }
    }
    for phoneme in other_phonemes.union(initial_phonemes):
        weighted_transitions[phoneme] = {
            p: random.randint(3, 10) for p in other_phonemes.union(ending_phonemes)
        }
        weighted_transitions[phoneme][None] = brevity_factor
    for phoneme in ending_phonemes:
        weighted_transitions[phoneme] = {
            None: 1
        }
    return weighted_transitions


def main():
    phonemes = {
        "bra", "kah", "to", "ro", "for", "mo", "ter", "je", "jo", "mel",
        "din", "ger", "tog", "tag", "nar", "bar", "la",
        "sha", "ial", "bia", "fra", "dar", "mis", "fang", "ke", "ike", "pyke",
        "el", "pia", "del", "er", "es", "qi", "nin"
    }
    first_name_language = gen_language(phonemes, brevity_factor=1000)
    last_name_language = gen_language(phonemes)
    # pprint(first_name_language)

    first_names = gen_names(first_name_language, n=100, min_length=4)
    # first_names = sorted(first_names)
    last_names = list(gen_names(last_name_language, n=20, min_length=4))*5
    last_names = sorted(last_names)
    for first_name, last_name in zip(first_names, last_names):
        print("{} {}".format(first_name.title(), last_name.title()))


if __name__ == "__main__":
    main()
