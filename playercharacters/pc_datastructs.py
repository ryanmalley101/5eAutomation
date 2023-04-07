from enum import Enum
from dataclasses import dataclass, field, asdict
import json
import time
from srd.srd_datastructs import AbilityScores, AbilityDescription


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

