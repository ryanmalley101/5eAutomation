from dataclasses import dataclass, field, asdict
import json
from srd.srd_datastructs import Size, AbilityDescription, proficiency_bonus, CreatureStatblock


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
        creature_dict['abilities'] = [asdict(abil) for abil in self.abilities]
        creature_dict['actions'] = [c.to_dict() for c in self.actions]
        creature_dict['bonusactions'] = [asdict(ba) for ba in self.bonusactions]
        creature_dict['reactions'] = [asdict(react) for react in self.reactions]
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
