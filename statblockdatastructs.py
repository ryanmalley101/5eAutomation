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
    alignment: str = 'unaligned'
    acdesc: str = ""
    acbonus: int = 10
    ability_scores: dict = field(default_factory=dict)
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
    bonusactions: list = field(default_factory=list)
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
        monster_dict['alignment'] = self.alignment
        monster_dict['ability_scores'] = [{score.value: self.ability_scores[score]}
                                          for score in self.ability_scores]
        monster_dict['abilities'] = [dataclasses.asdict(abil)
                                     for abil in self.abilities]
        monster_dict['actions'] = [c.to_dict() for c in self.actions]
        monster_dict['bonusactions'] = [dataclasses.asdict(ba)
                                        for ba in self.bonusactions]
        monster_dict['reactions'] = [dataclasses.asdict(react)
                                    for react in self.reactions]
        monster_dict['legendaryactions'] = [dataclasses.asdict(la)
                                            for la in self.legendaryactions]
        monster_dict['mythicactions'] = [dataclasses.asdict(myth)
                                         for myth in self.mythicactions]
        print(monster_dict)
        return json.dumps(monster_dict)

    def save_json(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        monster_json = open(timestr + '.json', "w")
        n = monster_json.write(self.to_json())
        print(n)
        monster_json.close()

    def get_total_ac(self):
        return 10 + score_to_mod(self.ability_scores[AbilityScores.DEXTERITY]) + self.acbonus

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

    def load_json(self, monster_json):
        def convert_json_attack(json_attack):
            if json_attack['type'] == BaseAttack.AttackType.MELEESPELL.value:
                return MeleeSpellAttack(name=json_attack['name'],
                                        attack_mod=AbilityScores(json_attack['attack_mod']),
                                        attack_bonus=int(json_attack['attack_bonus']),
                                        description=json_attack['description'],
                                        targets=json_attack['targets'],
                                        damage_dice=json_attack['damage_dice'],
                                        type=BaseAttack.AttackType(json_attack['type']),
                                        reach=json_attack['reach'])
            elif json_attack['type'] == BaseAttack.AttackType.MELEEWEAPON.value:
                return MeleeWeaponAttack(name=json_attack['name'],
                                        attack_mod=AbilityScores(json_attack['attack_mod']),
                                        attack_bonus=int(json_attack['attack_bonus']),
                                        description=json_attack['description'],
                                        targets=json_attack['targets'],
                                        damage_dice=json_attack['damage_dice'],
                                        type=BaseAttack.AttackType(json_attack['type']),
                                        reach=json_attack['reach'])
            elif json_attack['type'] == BaseAttack.AttackType.RANGEDWEAPON.value:
                return RangedWeaponAttack(name=json_attack['name'],
                                        attack_mod=AbilityScores(json_attack['attack_mod']),
                                        attack_bonus=int(json_attack['attack_bonus']),
                                        description=json_attack['description'],
                                        targets=json_attack['targets'],
                                        damage_dice=json_attack['damage_dice'],
                                        type=BaseAttack.AttackType(json_attack['type']),
                                        short_range=json_attack['short_range'],
                                        long_range=json_attack['long_range'])
            elif json_attack['type'] == BaseAttack.AttackType.RANGEDSPELL.value:
                return RangedSpellAttack(name=json_attack['name'],
                                        attack_mod=AbilityScores(json_attack['attack_mod']),
                                        attack_bonus=int(json_attack['attack_bonus']),
                                        description=json_attack['description'],
                                        targets=json_attack['targets'],
                                        damage_dice=json_attack['damage_dice'],
                                        type=BaseAttack.AttackType(json_attack['type']),
                                        range=json_attack['range'])
            else:
                raise ValueError('Invalid attack type')

        print(monster_json)
        monster_statblock = MonsterBlock()
        monster_statblock.name = monster_json['name']
        monster_statblock.size = Size(monster_json['size'])
        monster_statblock.alignment = monster_json['alignment']
        monster_statblock.acdesc = monster_json['acdesc']
        monster_statblock.acbonus = int(monster_json['acbonus'])
        for score in monster_json['ability_scores']:
            for key in score:
                print(key)
                monster_statblock.ability_scores[AbilityScores(key)] = score[key]
        monster_statblock.hitdice = monster_json['hitdice']
        monster_statblock.hitpoints = int(monster_json['hitpoints'])
        monster_statblock.speed = monster_json['speed']
        monster_statblock.strsave = bool(monster_json['strsave'])
        monster_statblock.dexsave = bool(monster_json['dexsave'])
        monster_statblock.consave = bool(monster_json['consave'])
        monster_statblock.intsave = bool(monster_json['intsave'])
        monster_statblock.wissave = bool(monster_json['wissave'])
        monster_statblock.chasave = bool(monster_json['chasave'])
        for skill in monster_json['skills']:
            monster_statblock.skills[skill] = bool(monster_json['skills'][skill])
        for immunity in monster_json['damageimmunities']:
            monster_statblock.damageimmunities[immunity] = bool(monster_json['damageimmunities'][immunity])
        for resistance in monster_json['damageresistances']:
            monster_statblock.damageresistances[resistance] = bool(monster_json['damageresistances'][resistance])
        for vulnerability in monster_json['damagevulnerabilities']:
            monster_statblock.damagevulnerabilities[vulnerability] = bool(monster_json['damagevulnerabilities'][vulnerability])
        for condition in monster_json['conditionimmunities']:
            monster_statblock.conditionimmunities[condition] = bool(monster_json['conditionimmunities'][condition])
        monster_statblock.senses = monster_json['senses']
        monster_statblock.languages = monster_json['languages']
        monster_statblock.challengerating = int(monster_json['challengerating'])
        for ability in monster_json['abilities']:
            monster_statblock.abilities.append(AbilityDescription(name=ability['name'],
                                                                  description=ability['description']))
        for action in monster_json['actions']:
            if 'attack_mod' in action:
                monster_statblock.actions.append(convert_json_attack(action))
            else:
                monster_statblock.actions.append(AbilityDescription(name=action['name'],
                                                                    description=action['description']))

        for bonus_action in monster_json['bonusactions']:
            monster_statblock.bonusactions.append(AbilityDescription(name=bonus_action['name'],
                                                                  description=bonus_action['description']))

        for reaction in monster_json['reactions']:
            monster_statblock.reactions.append(AbilityDescription(name=reaction['name'],
                                                                  description=reaction['description']))

        for legendary_action in monster_json['legendaryactions']:
            monster_statblock.legendaryactions.append(AbilityDescription(name=legendary_action['name'],
                                                                  description=legendary_action['description']))

        monster_statblock.mythicdescription = monster_json['mythicdescription']
        for mythic_action in monster_json['mythicactions']:
            monster_statblock.mythicactions.append(AbilityDescription(name=mythic_action['name'],
                                                                  description=mythic_action['description']))

        return monster_statblock

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
    attack_mod: AttackType = AttackType.UNKNOWN
    attack_bonus: int = 0
    description: str = ""
    targets: str = "one target."
    damage_dice: list = field(default_factory=list)
    type: AttackType = AttackType.UNKNOWN

    @classmethod
    def calculate_dicestring_damage(cls, dicestring, ability_mod=0):
        def len_no_empty(lst):
            return len(list(filter(lambda x: x != "", lst)))

        matches = re.findall(DICESTRINGPATTERN, dicestring)
        avg_roll = 0
        modifier = None
        if matches:
            for match in matches:
                if len_no_empty(match) == 1:
                    modifier = match[2]
                elif len_no_empty(match) == 2:
                    num_dice = int(match[0])
                    num_sides = int(match[1])
                    avg_roll += num_dice * ((num_sides + 1) / 2)

            modifier = modifier if modifier is not None else "0"
            if modifier.isdigit():
                modifier = int(modifier)
            elif modifier == 'M':
                modifier = ability_mod
            else:
                raise ValueError("Invalid die modifier")
            avg_roll += modifier
            return int(avg_roll)
        else:
            raise ValueError('Invalid dice roll format')

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['attack_mod'] = self.attack_mod.value
        return attackdict


@dataclass
class MeleeWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEEWEAPON
    reach: int = 5

    def __post_init__(self):
        self.type = BaseAttack.AttackType.MELEEWEAPON

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = BaseAttack.AttackType.MELEEWEAPON.value
        attackdict['attack_mod'] = self.attack_mod.value
        attackdict['reach'] = self.reach
        return attackdict


@dataclass
class RangedWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDWEAPON
    short_range: int = 20
    long_range: int = 60

    def __post_init__(self):
        self.type = BaseAttack.AttackType.RANGEDWEAPON

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = BaseAttack.AttackType.RANGEDWEAPON.value
        attackdict['short_range'] = self.short_range
        attackdict['attack_mod'] = self.attack_mod.value
        attackdict['long_range'] = self.long_range
        return attackdict


@dataclass
class MeleeSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEESPELL
    reach: int = 5

    def __post_init__(self):
        self.type = BaseAttack.AttackType.MELEESPELL

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = BaseAttack.AttackType.MELEESPELL.value
        attackdict['attack_mod'] = self.attack_mod.value
        attackdict['reach'] = self.reach
        return attackdict


@dataclass
class RangedSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDSPELL
    range: int = 30

    def __post_init__(self):
        self.type = BaseAttack.AttackType.RANGEDSPELL

    def to_dict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = BaseAttack.AttackType.RANGEDSPELL.value
        attackdict['attack_mod'] = self.attack_mod.value
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
