from numpy import random


def sample(distribution):
    """return a random key from the distribution, where the probability is
    proportional to the size of the value, relative to the sum of all
    values.

    :param distribution: a dictionary of which the values are numerals
    :returns: a random element from the keys of the distribution
    """
    total = sum(distribution.values())
    r = random.random() * total
    current = 0
    for key, value in distribution.items():
        current += value
        if current > r:
            return key


def normal_as_range(normal, add=0):
    mu, sdev = normal
    return range(round(mu - (sdev + add)), round(mu + (sdev + add)))


def normal(normal):
    mu, sdev = normal
    return random.normal(mu, sdev)
