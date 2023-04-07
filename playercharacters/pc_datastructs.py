import dataclasses
from enum import Enum
from dataclasses import dataclass, field, asdict
import json
import time


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

@dataclass
class Subclass:
    associated_class: ClassNames.UNKNOWN
    name: str = "PLACEHOLDER SUBCLASS"
    description: str = "This placeholder subclass is terrible, don't pick it"


class Background:
    name: str = "PLACEHOLDER BACKGROUND"
    description: str = "You picked the worst background, congratulations"


