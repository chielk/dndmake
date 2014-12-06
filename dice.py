#!/usr/bin/env python3
# (c) Chiel Kooijman 2014
import random
import sys


def __roll_dice(sides):
    """Roll a die."""
    return random.randint(1, sides)


def __roll(expression):
    total = 0
    exp = 0.  # Expected value
    max = 0
    min = 0
    components = ""  # Values of individual rolls and constants

    for part in "".join(expression).split("+"):
        # Dice
        if "d" in part:
            num, dice = part.split("d")
            if not num:
                num = 1
            try:
                num = int(num)
                dice = int(dice)
            except:
                print("Can not parse component: \"{}\"".format(part),
                      file=sys.stderr)
                sys.exit(1)
            for _ in range(num):
                exp += (dice + 1) / 2
                max += dice
                min += 1
                roll = __roll_dice(dice)
                total += roll
                components += str(roll) + "/" + str(dice) + " + "
        # Constants
        else:
            try:
                const = int(part)
            except:
                print("Can not parse component: \"{}\"".format(part),
                      file=sys.stderr)
                sys.exit(1)
            total += const
            exp += const
            max += const
            min += const
            components += part + " + "
    return total, exp, min, max, components


def roll(expression):
    return __roll(expression)[0]
