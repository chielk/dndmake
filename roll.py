#!/usr/bin/env python3
# (c) Chiel Kooijman 2014
import random
import sys


def __roll_dice(sides):
    """Roll a die."""
    return random.randint(1, sides)


def __roll(expression):
    total = 0
    exp = 0  # Expected value
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


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Roll some dice')
    parser.add_argument('expression', type=str, nargs='+',
                        help='Expression (e.g. 3d6 + 3)')
    parser.add_argument("-v", "--verbosity", action="count",
                        help="Print individual dice and constants")
    parser.add_argument("-e", "--expectancy", action="store_true",
                        help="Print expectancy instead of roll")
    args = parser.parse_args()
    if not args.verbosity:
        args.verbosity = 0

    total, exp, min, max, components = __roll(args.expression)

    # Output
    if exp.is_integer():
        exp = int(exp)  # Omit floating point
    if args.expectancy:
        if args.verbosity < 1:  # Print expectancy only
            print(exp, end="")
        else:  # Print min and max
            print(exp, "\t[min: ", min, ", max: ", max, "]", sep="", end="")
    else:
        print(total, end=" ")
        if args.verbosity and args.verbosity > 0:  # Print components
            print("\t[" + components[:-3] + "]", end=" ")
        if args.verbosity and args.verbosity > 0:  # Print expectancy
            if args.verbosity > 1:
                print("\t(exp: {}, min: {}, max: {}".format(exp, min, max),
                      end=")")
    print()
