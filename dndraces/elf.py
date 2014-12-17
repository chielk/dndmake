from dndraces import Race


class Elf(Race):
    NAME = "elf"
    LAWFULNESS = (0, 1)  # mu, sigma
    GOODNESS = (1, 1)  # mu, sigma

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
    # Male    4' 5"       +2d6            85 lb.      x (1d6) lb.
    # Female  4' 5"       +2d6            80 lb.      x (1d6) lb.

    H_MOD = "2d6"
    H_UNIT = "inch"

    W_MOD = "1d6"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "4'5\""
        W_BASE = "85lbs"

    class Female(Race.Female):
        H_BASE = "4'5\""
        W_BASE = "80lbs"
