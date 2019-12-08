#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import math
from bisect import bisect
from collections import OrderedDict

import numpy as np
import scipy.stats

from storygen.names.phoneme import ALPHA, OMEGA


prng = np.random.RandomState()


def spike(x, offset, variance):
    y = scipy.stats.norm.pdf(x, offset, math.sqrt(variance))
    y = y - min(y)
    y = y/max(x)
    return y


class DistributionFunction:

    def __init__(self, delta=0.1, offset=0.1, variance=0.01, n=2000):
        self.delta = delta
        self.variance = variance
        self.offset = offset
        self.x = np.linspace(0, 1, n)
        self.y = (
            spike(self.x, self.offset, self.variance) #+ spike(self.x, 1, 0.05)*3
        )
        self.y = self.y/max(self.y)

    def plot(self):
        import matplotlib
        matplotlib.use('TKAgg')
        import matplotlib.pyplot as plt
        plt.plot(self.x, self.y)
        plt.show()

    def sample(self, x=None):
        if x is None:
            x = prng.random_sample()
        i = bisect(self.x, x)
        y = self.y[i]
        if y < self.delta:
            return 0
        return y


class MarkovChain(object):

    def __init__(self, state_mapping, start=ALPHA, end=OMEGA):
        self.state_mapping = state_mapping
        self.start = start
        self.end = end

    def __call__(self):
        result = [self.start]
        while result[-1] is not self.end:
            choices, cdf = self.state_mapping[result[-1]]
            x = prng.random_sample()
            i = bisect(cdf, x)
            result.append(choices[i])
        return result[1:-1]

    def keys(self):
        return self.state_mapping.keys()

    @classmethod
    def from_weights(cls, weights):
        d = OrderedDict()
        for k, choice_dct in weights.items():
            keys, weights = zip(*choice_dct.items())
            total = float(sum(weights))
            probs = [v/total for v in weights]
            cdf = [probs[0]]
            for i in range(1, len(probs)):
                cdf.append(cdf[-1] + probs[i])
            d[k] = keys, cdf
        return cls(d)


def main():
    df = DistributionFunction()
    df.plot()


if __name__ == "__main__":
    main()
