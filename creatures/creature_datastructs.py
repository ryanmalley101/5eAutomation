from enum import Enum
from dataclasses import dataclass, field, asdict
import time
import json
import math
from patterns import DICESTRINGPATTERN
import re
from srd.srd_datastructs import Size, AbilityScores, SKILL_TO_ABILITY, score_to_mod, get_prof_bonus

@dataclass
class CreatureStatblock:
    name: str = "PLACEHOLDER"
    size: Size = Size.CHANGEME
    type: str = "NOTYPE"
    tag: str = ""
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
        creature_dict = asdict(self)
        creature_dict['size'] = self.size.value
        creature_dict['alignment'] = self.alignment
        creature_dict['ability_scores'] = [{score.value: self.ability_scores[score]}
                                          for score in self.ability_scores]
        creature_dict['abilities'] = [asdict(abil)
                                     for abil in self.abilities]
        creature_dict['actions'] = [c.to_dict() for c in self.actions]
        creature_dict['bonusactions'] = [asdict(ba)
                                        for ba in self.bonusactions]
        creature_dict['reactions'] = [asdict(react)
                                    for react in self.reactions]
        creature_dict['legendaryactions'] = [asdict(la)
                                            for la in self.legendaryactions]
        creature_dict['mythicactions'] = [asdict(myth)
                                         for myth in self.mythicactions]
        print(creature_dict)
        return json.dumps(creature_dict)

    def load_json(self, creature_json):
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

        print(creature_json)
        creature_statblock = CreatureStatblock()
        creature_statblock.name = creature_json['name']
        creature_statblock.size = Size(creature_json['size'])
        creature_statblock.type = creature_json['type']
        creature_statblock.tag = creature_json['tag']
        creature_statblock.alignment = creature_json['alignment']
        creature_statblock.acdesc = creature_json['acdesc']
        creature_statblock.acbonus = int(creature_json['acbonus'])
        for score in creature_json['ability_scores']:
            for key in score:
                print(key)
                creature_statblock.ability_scores[AbilityScores(key)] = score[key]
        creature_statblock.hitdice = creature_json['hitdice']
        creature_statblock.hitpoints = int(creature_json['hitpoints'])
        creature_statblock.speed = creature_json['speed']
        creature_statblock.strsave = bool(creature_json['strsave'])
        creature_statblock.dexsave = bool(creature_json['dexsave'])
        creature_statblock.consave = bool(creature_json['consave'])
        creature_statblock.intsave = bool(creature_json['intsave'])
        creature_statblock.wissave = bool(creature_json['wissave'])
        creature_statblock.chasave = bool(creature_json['chasave'])
        for skill in creature_json['skills']:
            creature_statblock.skills[skill] = bool(creature_json['skills'][skill])
        for immunity in creature_json['damageimmunities']:
            creature_statblock.damageimmunities[immunity] = bool(creature_json['damageimmunities'][immunity])
        for resistance in creature_json['damageresistances']:
            creature_statblock.damageresistances[resistance] = bool(creature_json['damageresistances'][resistance])
        for vulnerability in creature_json['damagevulnerabilities']:
            creature_statblock.damagevulnerabilities[vulnerability] = bool(creature_json['damagevulnerabilities'][vulnerability])
        for condition in creature_json['conditionimmunities']:
            creature_statblock.conditionimmunities[condition] = bool(creature_json['conditionimmunities'][condition])
        creature_statblock.senses = creature_json['senses']
        creature_statblock.languages = creature_json['languages']
        creature_statblock.challengerating = int(creature_json['challengerating'])
        for ability in creature_json['abilities']:
            creature_statblock.abilities.append(AbilityDescription(name=ability['name'],
                                                                  description=ability['description']))
        for action in creature_json['actions']:
            if 'attack_mod' in action:
                creature_statblock.actions.append(convert_json_attack(action))
            else:
                creature_statblock.actions.append(AbilityDescription(name=action['name'],
                                                                    description=action['description']))

        for bonus_action in creature_json['bonusactions']:
            creature_statblock.bonusactions.append(AbilityDescription(name=bonus_action['name'],
                                                                  description=bonus_action['description']))

        for reaction in creature_json['reactions']:
            creature_statblock.reactions.append(AbilityDescription(name=reaction['name'],
                                                                  description=reaction['description']))

        for legendary_action in creature_json['legendaryactions']:
            creature_statblock.legendaryactions.append(AbilityDescription(name=legendary_action['name'],
                                                                  description=legendary_action['description']))

        creature_statblock.mythicdescription = creature_json['mythicdescription']
        for mythic_action in creature_json['mythicactions']:
            creature_statblock.mythicactions.append(AbilityDescription(name=mythic_action['name'],
                                                                  description=mythic_action['description']))

        return creature_statblock

    def save_json(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        creature_json = open(timestr + '.json', "w")
        n = creature_json.write(self.to_json())
        print(n)
        creature_json.close()

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


@dataclass
class AbilityDescription:
    name: str = "PLACEHOLDER ABILITY"
    description: str = "NO DESCRIPTION"

    def to_dict(self):
        return asdict(self)


@dataclass
class BaseAttack:
    class AttackType(Enum):
        MELEEWEAPON = 'mw'
        RANGEDWEAPON = 'rw'
        MELEESPELL = 'ms'
        RANGEDSPELL = 'rs'
        UNKNOWN = 'un'

    name: str = "PLACEHOLDER ATTACK"
    attack_mod: AbilityScores = AbilityScores.STRENGTH
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
        attackdict = asdict(self)
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
        attackdict = asdict(self)
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
        attackdict = asdict(self)
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
        attackdict = asdict(self)
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
        attackdict = asdict(self)
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

