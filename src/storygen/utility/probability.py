#! /usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)

import pickle
import math
from bisect import bisect

import numpy as np
import matplotlib.mlab as mlab

from storygen.utility.shared import project_path


prng = np.random.RandomState()
# try:
#     with open(project_path('prng.dat'), 'rb') as f:
#         prng_state = pickle.load(f)
#     prng.set_state(prng_state)
#     print("Loaded saved PRNG")
# except IOError:
#     prng_state = prng.get_state()
#     with open(project_path('prng.dat'), 'wb') as f:
#         pickle.dump(prng_state, f)
#     print("Saved new PRNG")


def spike(x, offset, variance):
    y = mlab.normpdf(x, offset, math.sqrt(variance))
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


def main():
    df = DistributionFunction()
    df.plot()


if __name__ == "__main__":
    main()


def weighted_dict_to_cummulative_distribution(choice_dct):
    keys, weights = zip(*choice_dct.items())
    total = float(sum(weights))
    probs = [v/total for v in weights]
    cdf = [probs[0]]
    for i in range(1, len(probs)):
        cdf.append(cdf[-1] + probs[i])
    return keys, cdf
