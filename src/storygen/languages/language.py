#! /usr/bin/env python
import logging
from collections import OrderedDict

from storygen.languages.word import WordValidator, WordGenerator
from storygen.names.phoneme import ALPHA, OMEGA
from storygen.utility.probability import DistributionFunction, MarkovChain

__all__ = ['Language', 'LanguageGenerator']


logger = logging.getLogger(__name__)


class Language:
    """
    Consists of a set of phonemes, and a probabilistic model of how they occur.
    """

    def __init__(self, markov_chain, **kwargs):
        self.word_generator = kwargs.get('word_generator') or WordGenerator()
        self.phonemes = set(k for k in markov_chain.keys() if k is not ALPHA)
        self.markov_chain = markov_chain

    def word(self, validator=None, max_tries=1000):
        for n in range(max_tries):
            word = self.word_generator(self)
            if validator and not validator(word):
                continue
            return word
        else:
            raise RuntimeError("Failed to generate a word!")


class LanguageGenerator:
    """
    """
    def __init__(self, phonemes, sequence_dist_fn=None, phoneme_dist_fn=None):
        self.phonemes = phonemes
        self.phoneme_dist_fn = phoneme_dist_fn or DistributionFunction(delta=0.5, offset=0.5, variance=0.01)
        self.sequence_dist_fn = sequence_dist_fn or DistributionFunction(offset=0.1, variance=0.025)

    def __call__(self):
        phonemes = set(self.phonemes)
        for phoneme in list(phonemes):
            x = self.phoneme_dist_fn.sample()
            if not x:
                phonemes.remove(phoneme)
        if len(phonemes) < 10:
            # return self()
            phonemes = set(self.phonemes)

        # To be able to reproduce results using saved PRNG, the mapping must be ordered
        phoneme_weights = OrderedDict()
        for p in sorted(phonemes.union({ALPHA})):
            phoneme_weights[p] = OrderedDict()
            while sum(phoneme_weights[p].values()) < 0.3:
                for p2 in sorted(phonemes.union({OMEGA})):
                    if p is ALPHA and p2 is OMEGA:
                        continue
                    phoneme_weights[p][p2] = self.sequence_dist_fn.sample()
                    if p2 is OMEGA:
                        phoneme_weights[p][p2] += 0.1

        markov_chain = MarkovChain.from_weights(phoneme_weights)

        return Language(markov_chain)


def main():
    from storygen.names.phoneme import load_phonemes
    language_gen = LanguageGenerator(load_phonemes())
    main_language_words(language_gen)
    print("")
    main_language_words(language_gen)
    # language_gen.phoneme_dist_fn.plot()


def main_language_words(language_gen):
    language = language_gen()
    print("Language phonemes: {}".format(", ".join(sorted(str(p) for p in language.phonemes))))
    first_name = WordValidator(min_length=4, max_length=7, max_vowels=2, max_consonants=2)
    last_name = WordValidator(min_length=6, max_length=11, max_vowels=2, max_consonants=2)
    words = [(language.word(validator=first_name), language.word(validator=last_name)) for n in range(50)]
    for first, last in sorted(words, key=(lambda w: w[1])):
        first, last = str(first), str(last)
        print("{last}, {first}".format(first=first.title(), last=last.title()))
    return language


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
