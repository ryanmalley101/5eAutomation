from enum import Enum
from dataclasses import dataclass, field, asdict
import json
from srd.srd_datastructs import AbilityDescription, CreatureStatblock, proficiency_bonus


class ClassName(Enum):
    ARTIFICER = "Artificer"
    BARBARIAN = "Barbarian"
    BARD = "Bard"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    ROGUE = "Rogue"
    SORCERER = "Sorcerer"
    WARLOCK = "Warlock"
    WIZARD = "Wizard"
    UNKNOWN = "Unknown"


SubclassLevels = {
    ClassName.ARTIFICER: [3, 5, 9, 15],
    ClassName.BARBARIAN: [3, 6, 10, 14],
    ClassName.BARD: [3, 6, 14],
    ClassName.CLERIC: [1, 2, 6, 8, 17],
    ClassName.DRUID: [2, 6, 10, 14],
    ClassName.FIGHTER: [3, 7, 10, 15],
    ClassName.MONK: [3, 6, 11, 17],
    ClassName.PALADIN: [3, 7, 15, 20],
    ClassName.RANGER: [3, 7, 11, 15],
    ClassName.ROGUE: [3, 9, 13, 17],
    ClassName.SORCERER: [1, 6, 14, 18],
    ClassName.WARLOCK: [1, 6, 10, 14],
    ClassName.WIZARD: [2, 6, 10, 14]
}


@dataclass
class Race:
    name: str = "PLACEHOLDER RACE"
    lore_descriptions_list: list = field(default_factory=list)
    traits_list: list = field(default_factory=list)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass
class Subclass:
    @dataclass
    class SubclassAbility(AbilityDescription):
        class_level: int = 0

    associated_class: ClassName.UNKNOWN
    name: str = "PLACEHOLDER SUBCLASS"
    description: str = "This placeholder subclass is terrible, don't pick it"
    abilities: list = field(default_factory=list)

    def to_dict(self):
        subclass_dict = asdict(self)
        subclass_dict['associated_class'] = self.associated_class.value
        return subclass_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def convert_excel_template_subclass(subclass_name:str, associated_class:ClassName, subclass_description:str, subclass_abilities:list):
        new_subclass = Subclass(name=subclass_name, associated_class=associated_class, description=subclass_description, abilities=[])
        new_subclass.name = subclass_name
        new_subclass.associated_class = associated_class
        new_subclass.description = subclass_description
        for ability in subclass_abilities:
            level = SubclassLevels[associated_class][ability['level']]
            subclass_ability = Subclass.SubclassAbility(name=ability['name'], description=ability['description'], class_level=level)
            new_subclass.abilities.append(subclass_ability)
        return new_subclass



@dataclass
class Background:
    name: str = "PLACEHOLDER BACKGROUND"
    description: str = "You picked the worst background, congratulations"
    abilities: list = field(default_factory=list)

    def to_json(self):
        return json.dumps(asdict(self))


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
