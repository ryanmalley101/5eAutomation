from enum import Enum
import math
from dataclasses import asdict, dataclass
import json

class Size(Enum):
    TINY = 0
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    HUGE = 4
    GARGANTUAN = 5
    CHANGEME = 6

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def help(cls):
        print("Valid sizes:")
        for name in cls:
            print(f'| {name.value} - {name} |')

    @classmethod
    def hitdice(cls, value):
        match value:
            case Size.TINY:
                return 4
            case Size.SMALL:
                return 6
            case Size.MEDIUM:
                return 8
            case Size.LARGE:
                return 10
            case Size.HUGE:
                return 12
            case Size.GARGANTUAN:
                return 20


class AbilityScores(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

    @classmethod
    def menu(cls):
        for i, value in enumerate(cls):
            print(f"({i}) {value} ")

SKILL_LIST = [
    "Acrobatics",
    "Animal Handling",
    "Arcana",
    "Athletics",
    "Deception",
    "History",
    "Insight",
    "Intimidation",
    "Investigation",
    "Medicine",
    "Nature",
    "Perception",
    "Persuasion",
    "Religion",
    "Sleight of Hand",
    "Stealth",
    "Survival"
]

DAMAGE_LIST = (
    "acid",
    "bludgeoning",
    "cold",
    "fire",
    "force",
    "lightning",
    "necrotic",
    "piercing",
    "poison",
    "psychic",
    "radiant",
    "slashing",
    "thunder",
)

CONDITION_LIST = (
    "bleed",
    "blinded",
    "charmed",
    "deafened",
    "exhaustion",
    "frightened",
    "frostbitten",
    "grappled",
    "incapacitated",
    "invisible",
    "paralyzed",
    "petrified",
    "poisoned",
    "prone",
    "restrained",
    "stunned",
    "unconcious"
)


SKILL_TO_ABILITY = {
    "Athletics": AbilityScores.STRENGTH,
    "Acrobatics": AbilityScores.DEXTERITY,
    "Sleight of Hand": AbilityScores.DEXTERITY,
    "Stealth": AbilityScores.DEXTERITY,
    "Arcana": AbilityScores.INTELLIGENCE,
    "History": AbilityScores.INTELLIGENCE,
    "Investigation": AbilityScores.INTELLIGENCE,
    "Nature": AbilityScores.INTELLIGENCE,
    "Religion": AbilityScores.INTELLIGENCE,
    "Animal Handling": AbilityScores.WISDOM,
    "Insight": AbilityScores.WISDOM,
    "Medicine": AbilityScores.WISDOM,
    "Perception": AbilityScores.WISDOM,
    "Survival": AbilityScores.WISDOM,
    "Deception": AbilityScores.CHARISMA,
    "Intimidation": AbilityScores.CHARISMA,
    "Performance": AbilityScores.CHARISMA,
    "Persuasion": AbilityScores.CHARISMA
}

def score_to_mod(score):
    if score < 0:
        raise Exception("Ability Score is less than 0")

    return int((score-10)/2)

def proficiency_bonus(cr):
    return max(math.floor((cr - 1) / 4), 0) + 2


@dataclass
class AbilityDescription:
    name: str = "PLACEHOLDER ABILITY"
    description: str = "NO DESCRIPTION"

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(asdict(self))

