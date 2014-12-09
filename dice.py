#!/usr/bin/env python3
# (c) Chiel Kooijman 2014
import random
import sys
import re


def __roll_die(sides):
    """Roll a die."""
    return random.randint(1, sides)


def __roll_component(part, add=True):
    total = 0
    exp = 0.  # Expected value
    max = 0
    min = 0
    components = ""  # Values of individual rolls and constants
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
            if add:
                exp += (dice + 1) / 2
                max += dice
                min += 1
                roll = __roll_die(dice)
                total += roll
                components += str(roll) + "/" + str(dice) + " + "
            else:
                exp -= (dice + 1) / 2
                max -= dice
                min -= 1
                roll = __roll_die(dice)
                total -= roll
                components += str(roll) + "/" + str(dice) + " - "
    # Constants
    else:
        try:
            const = int(part)
        except:
            print("Can not parse component: \"{}\"".format(part),
                  file=sys.stderr)
            sys.exit(1)
        if add:
            total += const
            exp += const
            max += const
            min += const
            components += part + " + "
        else:
            total -= const
            exp -= const
            max -= const
            min -= const
            components += part + " - "
    return {'total': total, 'exp': exp, 'min': min, 'max': max,
            'str': components}


def __roll(expression):
    total = 0
    exp = 0.  # Expected value
    max = 0
    min = 0
    components = ""  # Values of individual rolls and constants

    add = re.findall("(?!-)[\dd]+", "".join(expression))
    sub = [x[1:] for x in re.findall("(?:-)[\dd]+", "".join(expression))]
    for part in add:
        result = __roll_component(part)
        total += result["total"]
        exp += result["exp"]
        min += result["min"]
        max += result["max"]
        components += result["str"]
    for part in sub:
        result = __roll_component(part)
        total -= result["total"]
        exp -= result["exp"]
        min -= result["min"]
        max -= result["max"]
        components += result["str"]
    return {'total': total, 'exp': exp, 'min': min, 'max': max,
            'str': components}


def roll(expression, get="total"):
    """Roll dice and add constants. Gives the total by default, but can also
    give expectancy, minimum, maximum or a string representing all rolls.
    """
    return __roll(expression)[get]
