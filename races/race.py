from simpleunit import Length, Weight
from dice import roll
from .helper import sample, normal, normal_as_range
from numpy.random import randint, choice


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

    ALIGN = range(-2, 2)  # Character trait index to alignment score

    DIMENSIONS = ["open",  # chaos <-> law
                  "conscientious",  # law <-> chaos
                  "extravert",
                  "agreeable",  # good <-> evil
                  "neurotic"]  # evil/2 <-> good/2, chaos <-> law

    LAWFULNESS = (0, 1)  # mean, stddev
    GOODNESS = (0, 2)  # mean, stddev

    HAIR = {"black": 1}

    EYES = {"brown": 1}

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

    # Default values from Human
    H_MOD = "2d10"
    H_MOD_TALL = "d5+d6+11"
    H_MOD_SHORT = "2d6"
    H_UNIT = "inch"

    W_MOD = "2d4"
    W_MOD_HEAVY = "d2+d3+3"
    W_MOD_LIGHT = "d2+d3"
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

    def __init__(self, settings):
        # Hair and eye colours
        self.hair = sample(self.HAIR)
        self.eyes = sample(self.EYES)

        # Output
        if settings.name:
            self.name = settings.name
        else:
            self.name = "Your character"

        self.make_height_weight(settings)
        self.make_personality(settings)

    def make_height_weight(self, settings):
        """Generate a height and weight given a race and gender."""
        gender = self.make_gender(settings)

        if settings.tall:
            H_MOD = roll(self.H_MOD_TALL)
        elif settings.short:
            H_MOD = roll(self.H_MOD_SHORT)
        else:
            H_MOD = roll(self.H_MOD)

        if settings.heavy:
            W_MOD = roll(self.W_MOD_HEAVY)
        elif settings.light:
            W_MOD = roll(self.W_MOD_LIGHT)
        else:
            W_MOD = roll(self.W_MOD)

        H_BASE = Length.parse(gender.H_BASE)
        H_UNIT = Length.parse(self.H_UNIT)
        W_BASE = Weight.parse(gender.W_BASE)

        self.height = H_BASE + H_UNIT * H_MOD
        self.weight = W_BASE + Weight(**{self.W_UNIT: W_MOD}) * H_MOD
        return self.height, self.weight

    def make_personality(self, settings):
        """Make a random personality based on the Big Five Personality Traits.
        :returns: A tuple containing a personality and an alignment
        """
        while True:
            law = 0
            good = 0
            personality = []
            for dimension in self.DIMENSIONS:
                rand = randint(0, 3)
                if dimension == "open":
                    law -= self.ALIGN[rand]
                elif dimension == "conscientious":
                    law += self.ALIGN[rand]
                elif dimension == "agreeable":
                    good -= self.ALIGN[rand]
                elif dimension == "neurotic":
                    good += self.ALIGN[rand]
                    law -= self.ALIGN[rand] / 2
                personality.append(self.VALUES[dimension][rand])

            if not settings.alignment:
                # Add random element to alignment
                law += normal(self.LAWFULNESS)
                good += normal(self.GOODNESS)

                alignment = Race.score_to_alignment(law, good)

                self.alignment = alignment
                self.personality = personality
                return alignment, personality
            else:
                for l in normal_as_range(self.LAWFULNESS):
                    for g in normal_as_range(self.GOODNESS):
                        tmp_law = law + l
                        tmp_good = good + g
                        alignment = Race.score_to_alignment(tmp_law, tmp_good)
                        if alignment == settings.alignment:
                            self.alignment = alignment
                            self.personality = personality
                            return alignment, personality

    def make_gender(self, settings):
        if settings.male:
            self.gender = self.Male
        elif settings.female:
            self.gender = self.Female
        else:
            self.gender = choice(self.GENDERS)

        return self.gender

    def __str__(self):
        pronoun = "he" if self.gender == self.Male else "she"

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
