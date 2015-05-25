from dndraces import Race
import random

class HalfOrc(Race):
    NAME = "half-orc"

    LAWFULNESS = (-1, 1)  # mu, sigma
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

    MALE_NAME = ["Dench", "Feng", "Gell", "Henk", "Holg", "Imsh", "Keth", "Krusk", "Ront", "Shump", "Thokk"]
    
    FEMALE_NAME = ["Baggi", "Emen", "Engong", "Myev", "Neega", "Ovak", "Ownka", "Shautha", "Vola", "Volen"]

    # Gender  Base Height Height Modifier Base Weight Weight Modifier
    # Male    4' 10"      +2d12           150 lb.     x (2d6) lb.
    # Female  4' 5"       +2d12           110 lb.     x (2d6) lb.

    H_MOD = "2d12"
    H_UNIT = "inch"

    W_MOD = "2d6"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "4'10\""
        W_BASE = "150lbs"

    class Female(Race.Female):
        H_BASE = "4'5\""
        W_BASE = "110lbs"

    def make_name(self):
        if self.gender.NAME == "male":
            self.name = random.choice(self.MALE_NAME)
        else: 
            self.name = random.choice(self.FEMALE_NAME)