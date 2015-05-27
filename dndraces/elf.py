from dndraces import Race
import random


class Elf(Race):
    NAME = "elf"
    LAWFULNESS = (-3, 2)  # mu, sigma
    GOODNESS = (2, 2)  # mu, sigma

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

    MALE_NAME = ["Aramil",
                 "Aust",
                 "Enialis",
                 "Heian",
                 "Himo",
                 "Ivellios",
                 "Lau-cian",
                 "Quarion",
                 "Soverliss",
                 "Thamior",
                 "Tharivol"]

    FEMALE_NAME = ["Anastrianna",
                   "Antinua",
                   "Drusilia",
                   "Felosial",
                   "Ielenia",
                   "Lia",
                   "Mialee",
                   "Qillathe",
                   "Silaqui",
                   "Vadania",
                   "Valanthe",
                   "Xanaphia"]

    FAMILY_NAME = ["Amastacia (Starflower)",
                   "Amakiir (Gemflower)",
                   "Galanodel (Moonwhisper)",
                   "Holimion (Diamonddew)",
                   "Liadon (Silverfrond)",
                   "Meliamne (Oak-enheel)",
                   "Naïlo (Nightbreeze)",
                   "Siannodel (Moonbrook)",
                   "Ilphukiir (Gemblossom)",
                   "Xiloscient (Goldpetal)"]

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

    def make_name(self):
        if self.gender.NAME == "male":
            first_name = random.choice(self.MALE_NAME)
        else:
            first_name = random.choice(self.FEMALE_NAME)
        family_name = random.choice(self.FAMILY_NAME)
        self.name = first_name + " " + family_name
