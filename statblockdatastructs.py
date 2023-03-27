import dataclasses
from enum import Enum
from dataclasses import dataclass, field
import time
import json
import math
from patterns import DICESTRINGPATTERN
import re

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


class Alignment(Enum):
    LG = "Lawful Good"
    NG = "Neutral Good"
    CG = "Chaotic Good"
    LN = "Lawful Neutral"
    N = "Neutral"
    CN = "Chaotic Neutral"
    LE = "Lawful Evil"
    NE = "Neutral Evil"
    CE = "Chaotic Evil"
    U = "Unaligned"
    CHANGEME = "CHANGEME"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def help(cls):
        print("Valid alignments:")
        for value in cls:
            print(value)

    @classmethod
    def convert(cls, value):
        if value in cls._value2member_map_:
            return cls(value)
        match value:
            case "LG":
                return Alignment.LG
            case "NG":
                return Alignment.NG
            case "CG":
                return Alignment.CG
            case "LN":
                return Alignment.LN
            case "N":
                return Alignment.N
            case "CN":
                return Alignment.CN
            case "LE":
                return Alignment.LE
            case "NE":
                return Alignment.NE
            case "CE":
                return Alignment.CE
            case "U":
                return Alignment.U
            case "UN":
                return Alignment.U
            case _:
                return Alignment.CHANGEME


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
    "non-magical b,p,s"
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


@dataclass
class MonsterBlock:
    name: str = "PLACEHOLDER"
    size: Size = Size.CHANGEME
    alignment: Alignment = Alignment.CHANGEME
    acdesc: str = ""
    acbonus: int = 10
    ability_scores: dict = field(default_factory=dict)
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
    hitdice: str = '0d0'
    hitpoints: int = 0
    speed: str = '30 ft.'
    strsave: bool = False
    dexsave: bool = False
    consave: bool = False
    intsave: bool = False
    wissave: bool = False
    chasave: bool = False
    skills: dict = field(default_factory=dict)
    damageimmunities: dict = field(default_factory=dict)
    damageresistances: dict = field(default_factory=dict)
    damagevulnerabilities: dict = field(default_factory=dict)
    conditionimmunities: dict = field(default_factory=dict)
    senses: str = ""
    languages: str = ""
    challengerating: int = 0
    abilities: list = field(default_factory=list)
    actions: list = field(default_factory=list)
    reactions: list = field(default_factory=list)
    legendaryactions: list = field(default_factory=list)
    mythicdescription: str = None
    mythicactions: list = field(default_factory=list)

    VULNERABILITY = "VULNERABILITY"
    IMMUNITY = "IMMUNITY"
    RESISTANCE = "RESISTANCE"

    def to_json(self):
        monster_dict = dataclasses.asdict(self)
        monster_dict['size'] = self.size.value
        monster_dict['alignment'] = self.alignment.value
        monster_dict['ability_scores'] = [score.value
                                          for score in self.ability_scores]
        monster_dict['abilities'] = [dataclasses.asdict(abil)
                                     for abil in self.abilities]
        monster_dict['actions'] = [c.to_dict() for c in self.actions]
        monster_dict['reaction'] = [dataclasses.asdict(react)
                                    for react in self.reactions]
        monster_dict['legendaryactions'] = [dataclasses.asdict(la)
                                            for la in self.legendaryactions]
        monster_dict['mythicactions'] = [dataclasses.asdict(myth)
                                         for myth in self.mythicactions]
        return json.dumps(monster_dict)

    def save_json(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        monster_json = open(timestr + '.json', "w")
        n = monster_json.write(self.to_json())
        print(n)
        monster_json.close()

    def get_total_ac(self):
        return score_to_mod(self.ability_scores['Dexterity'] + self.acbonus)

    def get_attack_bonus(self, attack):
        return get_prof_bonus(self.challengerating) + \
               self.ability_scores[attack.attack_mod] + \
               attack.attack_bonus

    def initialize_ability_scores(self):
        self.ability_scores[AbilityScores.STRENGTH] = 10
        self.ability_scores[AbilityScores.DEXTERITY] = 10
        self.ability_scores[AbilityScores.CONSTITUTION] = 10
        self.ability_scores[AbilityScores.INTELLIGENCE] = 10
        self.ability_scores[AbilityScores.WISDOM] = 10
        self.ability_scores[AbilityScores.CHARISMA] = 10

    def prof_bonus(self):
        return get_prof_bonus(self.challengerating)

    def save_bonus(self, save):
        return self.prof_bonus() + score_to_mod(self.ability_scores[save])

    def skill_bonus(self, skill):
        return self.prof_bonus() + score_to_mod(
            self.ability_scores[SKILL_TO_ABILITY[skill]])

    def passive_perception(self):
        if self.skills['Perception']:
            return 10 + self.skill_bonus('Perception')
        else:
            return 10 + score_to_mod(self.ability_scores[AbilityScores.WISDOM])

@dataclass
class AbilityDescription:
    name: str = "PLACEHOLDER ABILITY"
    description: str = "NO DESCRIPTION"

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclass
class BaseAttack:
    class AttackType(Enum):
        MELEEWEAPON = 'mw'
        RANGEDWEAPON = 'rw'
        MELEESPELL = 'ms'
        RANGEDSPELL = 'rs'
        UNKNOWN = 'un'

    name: str = "PLACEHOLDER ATTACK"
    attack_mod: str = ""
    attack_bonus: int = 0
    description: str = ""
    targets: str = "one target."
    damage_dice: list = field(default_factory=list)
    type: AttackType = AttackType.UNKNOWN

    @classmethod
    def calculate_dicestring_damage(cls, dicestring, ability_mod=0):
        match = re.match(DICESTRINGPATTERN, dicestring)
        if match:
            num_dice = int(match.group(1))
            num_sides = int(match.group(2))
            modifier = match.group(3) if match.group(3) else 0
            if modifier.isdigit():
                modifier = int(modifier)
            elif modifier == 'M':
                modifier = ability_mod
            else:
                raise ValueError("Invalid die modifier")
            avg_roll = num_dice * ((num_sides + 1) / 2) + modifier
            return avg_roll
        else:
            raise ValueError('Invalid dice roll format')

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        return attackdict


@dataclass
class MeleeWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEEWEAPON
    reach: int = 5

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['reach'] = self.reach
        return attackdict


@dataclass
class RangedWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDWEAPON
    short_range: int = 20
    long_range: int = 60

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['short_range'] = self.short_range
        attackdict['long_range'] = self.long_range
        return attackdict


@dataclass
class MeleeSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEESPELL
    reach: int = 5

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['reach'] = self.reach
        return attackdict


@dataclass
class RangedSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDSPELL
    range: int = 30

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['range'] = self.range
        return attackdict

CR_TO_XP_TABLE = {
    0: 0,
    .125: 25,
    .25: 50,
    .5: 100,
    1: 200,
    2: 450,
    3: 700,
    4: 1100,
    5: 1800,
    6: 2300,
    7: 2900,
    8: 3900,
    9: 5000,
    10: 5900,
    11: 7200,
    12: 8400,
    13: 10000,
    14: 11500,
    15: 13000,
    16: 15000,
    17: 18000,
    18: 20000,
    19: 22000,
    20: 25000,
    21: 33000,
    22: 41000,
    23: 50000,
    24: 62000,
    25: 76000,
    26: 90000,
    27: 105000,
    28: 120000,
    29: 137000,
    30: 155000
}

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

def get_prof_bonus(cr):
    return max(math.floor((cr - 1) / 4), 0) + 2
