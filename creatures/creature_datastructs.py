from enum import Enum
from dataclasses import dataclass, field, asdict
import time
import json
import math
from patterns import DICESTRINGPATTERN
import re
from srd.srd_datastructs import Size, AbilityScore, AbilityDescription, SKILL_TO_ABILITY, score_to_mod, proficiency_bonus, BaseAttack

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
    saving_throws: set = field(default_factory=set)
    skills: dict = field(default_factory=dict)
    damageimmunities: set = field(default_factory=set)
    damageresistances: set = field(default_factory=set)
    damagevulnerabilities: set = field(default_factory=set)
    conditionimmunities: set = field(default_factory=set)
    senses: str = ""
    languages: str = ""
    abilities: list = field(default_factory=list)
    actions: list = field(default_factory=list)
    bonusactions: list = field(default_factory=list)
    reactions: list = field(default_factory=list)

    def to_dict(self):
        creature_dict = asdict(self)
        creature_dict['size'] = self.size.value
        creature_dict['alignment'] = self.alignment
        creature_dict['ability_scores'] = [{score.value: self.ability_scores[score]} for score in self.ability_scores]
        creature_dict['abilities'] = [asdict(abil) for abil in self.abilities]
        creature_dict['actions'] = [c.to_dict() for c in self.actions]
        creature_dict['bonusactions'] = [asdict(ba) for ba in self.bonusactions]
        creature_dict['reactions'] = [asdict(react) for react in self.reactions]
        return creature_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def convert_json_dict(self, creature_dict):
        creature_dict = json.loads(creature_dict)
        creature_dict['size'] = Size(creature_dict['size'])
        creature_dict['acbonus'] = int(creature_dict['acbonus'])
        ability_scores = creature_dict['ability_scores']
        creature_dict['ability_scores'] = {}
        for index, score in enumerate(ability_scores):
            for key in score:
                creature_dict['ability_scores'][AbilityScore(key)] = score[key]
        creature_dict['hitpoints'] = int(creature_dict['hitpoints'])
        saves = creature_dict['saving_throws']
        creature_dict['saving_throws'] = set()
        for save in saves:
            creature_dict['saving_throws'].add(AbilityScore(save))
        for skill in creature_dict['skills']:
            creature_dict['skills'][skill] = bool(skill)
        for immunity in creature_dict['damageimmunities']:
            creature_dict['damageimmunities'][immunity] = bool(immunity)
        for resistance in creature_dict['damageresistances']:
            creature_dict['damageresistances'][resistance] = bool(resistance)
        for vulnerability in creature_dict['damagevulnerabilities']:
            creature_dict['damagevulnerabilities'][vulnerability] = bool(vulnerability)
        for condition in creature_dict['conditionimmunities']:
            creature_dict['conditionimmunities'][condition] = bool(condition)
        for index, ability in enumerate(creature_dict['abilities']):
            creature_dict['abilities'][index] = AbilityDescription(name=ability['name'],
                                                                   description=ability['description'])
        for index, action in enumerate(creature_dict['actions']):
            if 'attack_mod' in action:
                creature_dict['actions'][index] = BaseAttack.convert_json_attack(action)
            else:
                creature_dict['actions'][index] = AbilityDescription(name=action['name'],
                                                                    description=action['description'])

        for index, bonus_action in enumerate(creature_dict['bonusactions']):
            creature_dict['bonusactions'][index] = AbilityDescription(name=bonus_action['name'],
                                                                  description=bonus_action['description'])

        for index, reaction in enumerate(creature_dict['reactions']):
            creature_dict['reactions'][index] = AbilityDescription(name=reaction['name'],
                                                                  description=reaction['description'])

        return creature_dict

    @classmethod
    def load_json(cls, creature_json):
        return cls(**cls.convert_json_dict(creature_json))

    def save_json(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        creature_json = open(timestr + '.json', "w")
        n = creature_json.write(self.to_json())
        print(n)
        creature_json.close()

    def get_total_ac(self):
        return 10 + score_to_mod(self.ability_scores[AbilityScore.DEXTERITY]) + self.acbonus

    def initialize_ability_scores(self):
        self.ability_scores[AbilityScore.STRENGTH] = 10
        self.ability_scores[AbilityScore.DEXTERITY] = 10
        self.ability_scores[AbilityScore.CONSTITUTION] = 10
        self.ability_scores[AbilityScore.INTELLIGENCE] = 10
        self.ability_scores[AbilityScore.WISDOM] = 10
        self.ability_scores[AbilityScore.CHARISMA] = 10

    def proficiency_bonus(self):
        return 0

    def save_bonus(self, save):
        return self.proficiency_bonus() + score_to_mod(self.ability_scores[save])

    def skill_bonus(self, skill):
        return self.proficiency_bonus() + score_to_mod(
            self.ability_scores[SKILL_TO_ABILITY[skill]])

    def passive_perception(self):
        if self.skills['Perception']:
            return 10 + self.skill_bonus('Perception')
        else:
            return 10 + score_to_mod(self.ability_scores[AbilityScore.WISDOM])


@dataclass
class PlayerCharacterStatblock(CreatureStatblock):
    class_levels: dict = field(default_factory=dict)

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
        print(creature_dict)
        return json.dumps(creature_dict)

    def character_level(self):
        return sum(self.class_levels.values())

    def proficiency_bonus(self):
        return proficiency_bonus(self.character_level())

    @classmethod
    def load_json(cls, creature_json):
        creature_dict = CreatureStatblock.convert_json_dict(creature_json)
        return cls(**creature_dict)


@dataclass
class MonsterStatblock(CreatureStatblock):
    challengerating: int = 0
    legendaryactions: list = field(default_factory=list)
    mythicdescription: str = None
    mythicactions: list = field(default_factory=list)

    def to_json(self):
        creature_dict = asdict(self)
        creature_dict['size'] = self.size.value
        creature_dict['alignment'] = self.alignment
        creature_dict['ability_scores'] = [{score.value: self.ability_scores[score]}
                                          for score in self.ability_scores]
        creature_dict['saving_throws'] = [save.value for save in self.saving_throws]
        creature_dict['abilities'] = [asdict(abil)
                                     for abil in self.abilities]
        creature_dict['actions'] = [c.to_dict() for c in self.actions]
        creature_dict['bonusactions'] = [asdict(ba)
                                        for ba in self.bonusactions]
        creature_dict['reactions'] = [asdict(react)
                                    for react in self.reactions]
        creature_dict['legendaryactions'] = [asdict(la) for la in self.legendaryactions]
        creature_dict['mythicactions'] = [asdict(myth) for myth in self.mythicactions]
        print(creature_dict)
        return json.dumps(creature_dict)

    def proficiency_bonus(self):
        return proficiency_bonus(self.challengerating)

    @classmethod
    def load_json(cls, creature_json):
        creature_dict = CreatureStatblock.convert_json_dict(creature_json)
        for index, legendaryaction in enumerate(creature_dict['legendaryactions']):
            creature_dict['legendaryactions'][index] = AbilityDescription(name=legendaryaction['name'],
                                                                  description=legendaryaction['description'])

        for index, mythicaction in enumerate(creature_dict['mythicactions']):
            creature_dict['mythicactions'][index] = AbilityDescription(name=mythicaction['name'],
                                                                     description=mythicaction['description'])

        return cls(**creature_dict)

class DamageModifiers(Enum):
    VULNERABILITY = "VULNERABILITY"
    IMMUNITY = "IMMUNITY"
    RESISTANCE = "RESISTANCE"

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