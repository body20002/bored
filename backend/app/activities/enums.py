from enum import Enum

class Participants(Enum):
    alone = "alone"
    party = "party"
    with_a_frined = "with a friend"
    with_the_gang = "with the gang"


class Types(Enum):
    busywork = "busywork"
    charity = "charity"
    cooking = "cooking"
    diy = "diy"
    education = "education"
    music = "music"
    recreational = "recreational"
    relaxation = "relaxation"
    social = "social"


class Accessibility(Enum):
    few_to_no_challenges = "Few to no challenges"
    major_challenges = "Major challenges"
    minor_challenges = "Minor challenges"


class Duration(Enum):
    hours = "hours"
    minutes = "minutes"
    days = "days"
    week = "week"
    weeks = "weeks"


class Price(Enum):
    expensive = "expensive"
    inexpensive = "inexpensive"
    free = "free"


