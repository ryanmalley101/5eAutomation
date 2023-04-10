from enum import Enum
from dataclasses import dataclass, field, asdict
import time
import json
import math
from patterns import DICESTRINGPATTERN
import re
from srd.srd_datastructs import Size, AbilityScore, AbilityDescription, Skill, DamageType, Condition, SKILL_TO_ABILITY, score_to_mod, proficiency_bonus, BaseAttack, DamageModifier

@dataclass
class CreatureStatblock:
    name: str = "PLACEHOLDER"
    size: Size = Size.MEDIUM
    type: str = "NOTYPE"
    tag: str = ""
    alignment: str = 'unaligned'
    acdesc: str = ""
    acbonus: int = 10
    ability_scores: dict = field(default_factory=dict)
    hitdice: int = 1
    hitpoints: int = 0
    speed: str = '30 ft.'
    saving_throws: set = field(default_factory=set)
    skills: set = field(default_factory=set)
    expertise: set = field(default_factory=set)
    damage_immunities: set = field(default_factory=set)
    damage_resistances: set = field(default_factory=set)
    damage_vulnerabilities: set = field(default_factory=set)
    condition_immunities: set = field(default_factory=set)
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

        skills = creature_dict['skills']
        creature_dict['skills'] = set()
        for skill in skills:
            creature_dict['skills'].add(Skill(skill))

        expertise = creature_dict['expertise']
        creature_dict['expertise'] = set()
        for skill in expertise:
            creature_dict['expertise'].add(Skill(skill))

        immunities = creature_dict['damage_immunities']
        creature_dict['damage_immunities'] = set()
        for immunity in immunities:
            creature_dict['damage_immunities'].add(DamageType(immunity))

        resistances = creature_dict['damage_resistances']
        creature_dict['damage_resistances'] = set()
        for resistance in resistances:
            creature_dict['damage_resistances'].add(DamageType(resistance))

        vulnerabilities = creature_dict['damage_vulnerabilities']
        creature_dict['damage_vulnerabilities'] = set()
        for vulnerability in vulnerabilities:
            creature_dict['damage_vulnerabilities'].add(DamageType(vulnerability))

        conditions = creature_dict['condition_immunities']
        creature_dict['condition_immunities'] = set()
        for condition in conditions:
            creature_dict['condition_immunities'].add(Condition(condition))

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

    def save_json_to_file(self, filename='', timestamp=False):
        if timestamp or filename == '' :
            filename = filename+time.strftime("%Y%m%d-%H%M%S")
        with open(filename + '.json', "w") as creature_json:
            creature_json.write(self.to_json())

    @classmethod
    def load_json_from_file(cls, filename=None):
        if filename:
            with open(filename, "r") as creature_json:
                return MonsterStatblock.load_json(creature_json.read())

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
        if Skill.PERCEPTION in self.skills:
            return 10 + self.skill_bonus(Skill.PERCEPTION)
        else:
            return 10 + score_to_mod(self.ability_scores[AbilityScore.WISDOM])

    def add_damage_modifier(self, damage:DamageType, modifier:DamageModifier):
        if modifier is DamageModifier.IMMUNITY:
            self.damage_vulnerabilities.discard(damage)
            self.damage_resistances.discard(damage)
            self.damage_immunities.add(damage)
        elif modifier is DamageModifier.VULNERABILITY:
            self.damage_immunities.discard(damage)
            self.damage_resistances.discard(damage)
            self.damage_vulnerabilities.add(damage)
        elif modifier is DamageModifier.RESISTANCE:
            self.damage_immunities.discard(damage)
            self.damage_vulnerabilities.discard(damage)
            self.damage_resistances.add(damage)
        else:
            raise ValueError("Tried to add an unaccounted for DamageModifier")

    def add_skill_proficiency(self, skill:Skill):
        self.expertise.discard(skill)
        self.skills.add(skill)

    def add_skill_expertise(self, skill:Skill):
        self.skills.discard(skill)
        self.expertise.add(skill)



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
        creature_dict['condition_immunities'] = [condition.value for condition in self.condition_immunities]
        creature_dict['skills'] = [skill.value for skill in self.skills]
        creature_dict['expertise'] = [skill.value for skill in self.expertise]
        creature_dict['damage_immunities'] = [damage.value for damage in self.damage_immunities]
        creature_dict['damage_resistances'] = [damage.value for damage in self.damage_resistances]
        creature_dict['damage_vulnerabilities'] = [damage.value for damage in self.damage_vulnerabilities]
        creature_dict['abilities'] = [asdict(abil)
                                     for abil in self.abilities]
        creature_dict['actions'] = [c.to_dict() for c in self.actions]
        creature_dict['bonusactions'] = [asdict(ba)
                                        for ba in self.bonusactions]
        creature_dict['reactions'] = [asdict(react)
                                    for react in self.reactions]
        creature_dict['legendaryactions'] = [asdict(la) for la in self.legendaryactions]
        creature_dict['mythicactions'] = [asdict(myth) for myth in self.mythicactions]
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

    @staticmethod
    def calc_monster_hit_dice(target_hit_points: int, size: Size, con: int):
        hit_die = Size.hitdice(size)
        max_hit_dice = 0
        max_hit_points = 0
        average_hit_die = (hit_die / 2) + con
        while max_hit_points + average_hit_die < target_hit_points:
            max_hit_dice += 1
            max_hit_points += average_hit_die
        return max_hit_dice, round(max_hit_points)


    @staticmethod
    def calc_monster_hit_points(hit_dice: int, size: Size, con: int):
        hit_die = Size.hitdice(size)
        average_hit_die = (hit_die / 2) + con
        max_hit_points = round(average_hit_die*hit_dice)
        return max_hit_points

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