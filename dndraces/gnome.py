from dndraces import Race
import random

class Gnome(Race):
    NAME = "gnome"
    LAWFULNESS = (0, 2)  # mu, sigma
    GOODNESS = (2, 2.5)  # mu, sigma

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

    MALE_NAME = ["Boddynock", "Dimble", "Fonkin", "Gimble", "Glim", "Gerbo", "Jebeddo", "Namfoodle", "Roondar", "Seebo", "Zook"]

    FEMALE_NAME = ["Bimpnottin", "Caramip", "Duvamil", "Ellywick", "Ellyjobell", "Loopmottin", "Mardnab", "Roywyn", "Shamil", "Waywocket"]

    CLAN_NAME = ["Beren", "Daergel", "Folkor", "Garrick", "Nackle", "Murnig", "Ningel", "Raulnor", "Scheppen", "Turen"]

    # Gender  Base Height Height Modifier Base Weight Weight Modifier
    # Male    3' 0"       +2d4            40 lb.      x 1 lb.
    # Female  2' 10"      +2d4            35 lb.      x 1 lb.

    H_MOD = "2d4"
    H_UNIT = "inch"

    W_MOD = "1"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "3'0\""
        W_BASE = "40lbs"

    class Female(Race.Female):
        H_BASE = "3'7\""
        W_BASE = "35lbs"


    def make_name(self):
        if self.gender.NAME == "male":
            first_name = random.choice(self.MALE_NAME)
        else: 
            first_name = random.choice(self.FEMALE_NAME)
        clan_name = random.choice(self.CLAN_NAME)
        self.name = first_name + " " + clan_name

