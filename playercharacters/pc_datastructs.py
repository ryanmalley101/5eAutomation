from enum import Enum
from dataclasses import dataclass, field, asdict
import json
from srd.srd_datastructs import AbilityDescription, CreatureStatblock, proficiency_bonus


class ClassNames(Enum):
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

    associated_class: ClassNames.UNKNOWN
    name: str = "PLACEHOLDER SUBCLASS"
    description: str = "This placeholder subclass is terrible, don't pick it"
    abilities: list = field(default_factory=list)

    def to_dict(self):
        subclass_dict = asdict(self)
        subclass_dict['associated_class'] = self.associated_class.value
        return subclass_dict

    def to_json(self):
        return json.dumps(self.to_dict())


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
