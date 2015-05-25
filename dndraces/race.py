from simpleunit import Length, Weight
from dice import roll, E
from .helper import sample, normal, normal_as_range
from numpy.random import randint
import numpy
import random


class Race:
    NAME = "base-race"
    ALIGNMENT_LONG = {"LG": "Lawful Good",
                      "NG": "Neutral Good",
                      "CG": "Chaotic Good",
                      "LN": "Lawful Neutral",
                      "NN": "True Neutral",
                      "CN": "Chaotic Neutral",
                      "LE": "Lawful Evil",
                      "NE": "Neutral Evil",
                      "CE": "Chaotic Evil"}

    ALIGNMENTS = ALIGNMENT_LONG.keys()

    DIMENSIONS = ["open",  # chaos <-> law
                  "conscientious",  # law <-> chaos
                  "extravert",
                  "agreeable",  # good <-> evil
                  "neurotic"]  # evil/2 <-> good/2, chaos <-> law

    LAWFULNESS = (0, 1)  # mean, stddev
    GOODNESS = (0, 2)  # mean, stddev

    HAIR = {"black": 1}

    EYES = {"brown": 1}

    NAME = {"Your Character":1}

    VALUES = {"open": {("inventive and curious", 2): 1,
                       ("curious", 1): 1,
                       ("cautious", -1): 1,
                       ("cautious and conservative", -2): 1},
              "conscientious": {("efficient and organized", 2): 1,
                                ("organized", 1): 1,
                                ("a bit disorganized", -1): 1,
                                ("disorganized", -2): 1},
              "extravert": {("outgoing and energetic", 2): 1,
                            ("outgoing", 1): 1,
                            ("reserved", -1): 1,
                            ("solitary and reserved", -2): 1},
              "agreeable": {("friendly and compassionate", 2): 1,
                            ("friendly", 1): 1,
                            ("somewhat detached", -1): 1,
                            ("analytical and detached", -2): 1},
              "neurotic": {("quickly angered", 2): 1,
                           ("somewhat nervous", 1): 1,
                           ("calm", -1): 1,
                           ("calm and confident", -2): 1}}

    # Default values from Human
    H_MOD = "2d10"
    H_UNIT = "inch"

    W_MOD = "2d4"
    W_UNIT = "lbs"

    class Male:
        NAME = "male"
        H_BASE = "4'10\""
        W_BASE = "120lbs"

    class Female:
        NAME = "female"
        H_BASE = "4'5\""
        W_BASE = "85lbs"

    GENDERS = [Male, Female]

    @staticmethod
    def score_to_alignment(law, good):
        """Convert a lawfulness and goodness score to an alignment."""
        if law > 2:
            lawfulness = "L"
        elif law < -2:
            lawfulness = "C"
        else:
            lawfulness = "N"

        if good > 1:
            goodness = "G"
        elif good < -1:
            goodness = "E"
        else:
            goodness = "N"

        return lawfulness + goodness

    def __init__(self, name=None, gender=None, height=None, weight=None,
                 alignment=None):
        # Hair and eye colours
        self.hair = sample(self.HAIR)
        self.eyes = sample(self.EYES)

        # Output

        self.make_height_weight(gender=gender, height=height, weight=weight)
        self.make_personality(alignment=alignment)
        if name:
            self.name = name
        else:
            self.make_name()

    def make_height_weight(self, gender=None, height=None, weight=None):
        """Generate a height and weight given a race and gender."""
        self.make_gender(gender)

        if height == "tall":
            H_MOD = (roll(self.H_MOD) + 2 * E(self.H_MOD)) / 3
        elif height == "short":
            H_MOD = roll(self.H_MOD) / 2
        else:
            H_MOD = roll(self.H_MOD)

        if weight == "heavy":
            W_MOD = (roll(self.W_MOD) + 2 * E(self.W_MOD)) / 3
        elif weight == "light":
            W_MOD = roll(self.W_MOD) / 2
        else:
            W_MOD = roll(self.W_MOD)

        H_BASE = Length.parse(self.gender.H_BASE)
        H_UNIT = Length.parse(self.H_UNIT)
        W_BASE = Weight.parse(self.gender.W_BASE)

        self.height = H_BASE + H_UNIT * H_MOD
        self.weight = W_BASE + Weight(**{self.W_UNIT: W_MOD}) * H_MOD
        return self.height, self.weight

    def random_personality(self):
        """Generate a random personality according to the sample probabilities
        provided by VALUES of the class.
        :returns: lawfulness and goodness scores, and a personality
        """
        law = 0
        good = 0
        personality = []
        for dimension in self.DIMENSIONS:
            dim, val = sample(self.VALUES[dimension])
            if dimension == "open":
                law -= val
            elif dimension == "conscientious":
                law += val
            elif dimension == "agreeable":
                good -= val
            elif dimension == "neurotic":
                good += val
                law -= val / 2
            personality.append(dim)
        return law, good, personality

    def make_personality(self, alignment=None):
        """Make a random personality based on the Big Five Personality Traits.
        Tries to make a personality consistent with the alignment if given.
        :returns: A tuple containing a personality and an alignment
        """
        tries = 0
        add_variance = 0
        wanted_alignment = alignment
        while True:
            if tries > 25:
                add_variance += 1
            tries += 1

            law, good, personality = self.random_personality()

            if not wanted_alignment:
                # Add random element to alignment
                law += normal(self.LAWFULNESS)
                good += normal(self.GOODNESS)

                alignment = Race.score_to_alignment(law, good)

                self.alignment = alignment
                self.personality = personality
                return alignment, personality
            else:
                for l in normal_as_range(self.LAWFULNESS, add=add_variance):
                    for g in normal_as_range(self.GOODNESS, add=add_variance):
                        tmp_law = law + l
                        tmp_good = good + g
                        alignment = Race.score_to_alignment(tmp_law, tmp_good)
                        if alignment == wanted_alignment:
                            self.alignment = alignment
                            self.personality = personality
                            return alignment, personality

    def make_gender(self, gender):
        if gender == "male":
            self.gender = self.Male
        elif gender == "female":
            self.gender = self.Female
        else:
            self.gender = random.choice(self.GENDERS)
    
    def make_name(self):
        self.name = "Boring McBasic"

    def __str__(self):
        pronoun = "he" if self.gender.__name__ == self.Male.__name__ else "she"

        s = "{} is a {} ({}) {} {}, {} ({}) tall and weighs {} ({}). {} has "\
            "{} hair and {} eyes.\n{} is "
        s = s.format(self.name,
                     self.ALIGNMENT_LONG[self.alignment],
                     self.alignment,
                     self.gender.NAME,
                     self.NAME,
                     self.height.metric(),
                     self.height.imperial(),
                     self.weight.metric(),
                     self.weight.imperial(),
                     pronoun.capitalize(),
                     self.hair,
                     self.eyes,
                     pronoun.capitalize())
        s += ", ".join(self.personality[:-1]) + ", and "
        s += self.personality[-1] + "."
        return s
