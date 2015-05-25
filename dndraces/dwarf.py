from dndraces import Race
import random


class Dwarf(Race):
    NAME = "dwarf"
    LAWFULNESS = (2, 1)  # mu, sigma
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

    MALE_NAME = ["Barendd", "Brottor", "Eberk", "Einkil", "Oskar", "Rurik", "Taklinn", "Torderk", "Traubon", "Ulfgar", "Veit"]

    FEMALE_NAME = ["Artin", "Audhild", "Dagnal", "Diesa", "Gunnloda", "Hlin", "Ilde", "Liftrasa", "Sannl", "Torgga"]

    CLAN_NAME = ["Balderk", "Dankil", "Gorunn", "Holderhek", "Loderr", "Lutgehr", "Rumnaheim", "Strakeln", "Torunn", "Ungart"]

    # Gender  Base Height Height Modifier Base Weight Weight Modifier
    # Male    3' 9"       +2d4            130 lb.     x (2d6) lb.
    # Female  3' 7"       +2d4            100 lb.     x (2d6) lb.

    H_MOD = "2d4"
    H_UNIT = "inch"

    W_MOD = "2d6"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "3'9\""
        W_BASE = "130lbs"

    class Female(Race.Female):
        H_BASE = "3'7\""
        W_BASE = "100lbs"

    def make_name(self):
        if self.gender.NAME == "male":
            first_name = random.choice(self.MALE_NAME)
        else: 
            first_name = random.choice(self.FEMALE_NAME)
        clan_name = random.choice(self.CLAN_NAME)
        self.name = first_name + " " + clan_name