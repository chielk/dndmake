from .race import Race
from simpleunit import Length, Weight, Inch
from dice import roll


class Human(Race):
    NAME = "human"

    LAWFULNESS_VARIANCE = range(-1, 1)
    GOODNESS_VARIANCE = range(-2, 2)

    HAIR = {"black": 20,
            "brown": 35,
            "blond": 15,
            "ginger": 8,
            "green": 1,
            "blue": 1,
            "white": 1,
            "red": 1,
            }

    EYES = {"blue": 20,
            "brown": 40,
            "green": 10,
            "black": 10,
            "red": 1,
            "violet": 1,
            }

    # Gender  Base Height Height Modifier Base Weight Weight Modifier
    # Male    4' 10"      +2d10           120 lb.     x (2d4) lb.
    # Female  4' 5"       +2d10           85 lb.      x (2d4) lb.

    H_MOD = "2d10"
    H_MOD_TALL = "d5 + d6 + 11"
    H_MOD_SHORT = "2d6"
    H_UNIT = Inch

    W_MOD = "2d4"
    W_MOD_HEAVY = "d2 + d3 + 3"
    W_MOD_LIGHT = "d2 + d3"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = Length(ft=4, inch=10)
        W_BASE = Weight(lbs=120)

    class Female(Race.Female):
        H_BASE = Length(ft=4, inch=5)
        W_BASE = Weight(lbs=85)

    GENDERS = [Male, Female]
