class Race:
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
                  "neurotic"]  # evil <-> good, chaos <-> law

    LAWFULNESS_VARIANCE = range(-1, 1)
    GOODNESS_VARIANCE = range(-2, 2)

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

    class Male:
        NAME = "male"

    class Female:
        NAME = "female"

    GENDERS = [Male, Female]
