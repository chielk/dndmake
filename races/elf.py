from .race import Race
from simpleunit import Length, Weight, Inch


class Elf(Race):
    LAWFULNESS_VARIANCE = range(-1, 1)
    GOODNESS_VARIANCE = range(0, 4)

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

    VALUES = {"open": ("inventive and curious", "curious", "cautious",
                       "cautious and conservative"),
              "conscientious": ("efficient and organized", "organized",
                                "a bit disorganized", "disorganized"),
              "extravert": ("outgoing and energetic", "outgoing", "reserved",
                            "solitary and reserved"),
              "agreeable": ("friendly and compassionate", "friendly",
                            "somewhat detached", "analytical and detached"),
              "neurotic": ("quickly angered", "somewhat nervous", "calm",
                           "calm and confident")}

    # Gender  Base Height Height Modifier Base Weight Weight Modifier
    # Male    4' 5"       +2d6            85 lb.      x (1d6) lb.
    # Female  4' 5"       +2d6            80 lb.      x (1d6) lb.


    H_MOD = "2d6"
    H_MOD_TALL = "2d4 + 4"
    H_MOD_SHORT = "2d4"
    H_UNIT = Inch()

    W_MOD = "1d6"
    W_MOD_HEAVY = "d3 + 3"
    W_MOD_LIGHT = "d3"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = Length(ft=4, inch=5)
        W_BASE = Weight(lbs=85)

    class Female(Race.Female):
        H_BASE = Length(ft=4, inch=5)
        W_BASE = Weight(lbs=85)

    GENDERS = [Male, Female]
