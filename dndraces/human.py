from dndraces import Race
import random

class Human(Race):
    NAME = "human"

    LAWFULNESS = (0, 1)  # mu, sigma
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

    MALE_NAME = ["Adam", "Geoffrey", "Gilbert", "Henry", "Hugh", "John", "Nicholas", "Peter", "Ralph", "Richard", "Robert", "Roger", "Simon", "Thomas", "Walter", "William"]

    FEMALE_NAME = ["Ada", "Agnes", "Alice", "Avice", "Beatrice", "Cecily", "Elwisia", "Emma", "Emelyn", "Gisella", "Isabella", "Joan", "Juliana", "Margery", "Matilda", "Molly", "Rosa", "Yvette"]

    FAMILY_NAME = ["Ashdown", "Abbott", "Barrett", "Baker", "Bradford", "Chance", "Cross", "Eaton", "Fletcher", "Forest", "Garrett", "Gladwyn", "Greene", "Grey", "James", "Lynton", "Moore", "Payne", "Penny", "Quick", "Ward", "Webb"]

    # Gender  Base Height Height Modifier Base Weight Weight Modifier
    # Male    4' 10"      +2d10           120 lb.     x (2d4) lb.
    # Female  4' 5"       +2d10           85 lb.      x (2d4) lb.

    H_MOD = "2d10"
    H_UNIT = "inch"

    W_MOD = "2d4"
    W_UNIT = "lbs"

    class Male(Race.Male):
        H_BASE = "4'10\""
        W_BASE = "120lbs"

    class Female(Race.Female):
        H_BASE = "4'5\""
        W_BASE = "85lbs"

    def make_name(self):
        if self.gender.NAME == "male":
            first_name = random.choice(self.MALE_NAME)
        else: 
            first_name = random.choice(self.FEMALE_NAME)
        family_name = random.choice(self.FAMILY_NAME)
        self.name = first_name + " " + family_name