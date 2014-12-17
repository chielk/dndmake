
from dndraces import Race


class HalfElf(Race):
    NAME = "half-elf"
    LAWFULNESS = (-2, 1)  # mu, sigma
    GOODNESS = (0, 2)  # mu, sigma

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
    # Male    4' 7"       +2d8            100 lb.     x (2d4) lb.
    # Female  4' 5"       +2d8            80 lb.      x (2d4) lb.

    H_MOD = "2d8"
    H_UNIT = "inch"

    W_MOD = "2d4"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "4'7\""
        W_BASE = "100lbs"

    class Female(Race.Female):
        H_BASE = "4'5\""
        W_BASE = "80lbs"
