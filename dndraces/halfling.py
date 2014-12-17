from dndraces import Race


class Halfling(Race):
    NAME = "halfling"
    LAWFULNESS = (0, .5)  # mu, sigma
    GOODNESS = (0, 1)  # mu, sigma

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
    # Male    2' 8"       +2d4            30 lb.      x 1 lb.
    # Female  2' 6"       +2d4            25 lb.      x 1 lb.

    H_MOD = "2d4"
    H_UNIT = "inch"

    W_MOD = "1"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "2'8\""
        W_BASE = "30lbs"

    class Female(Race.Female):
        H_BASE = "2'8\""
        W_BASE = "25lbs"
