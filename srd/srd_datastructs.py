from enum import Enum
import math
from dataclasses import asdict, dataclass, field
import json
from patterns import DICESTRINGPATTERN
import re


class Size(Enum):
    TINY = 'Tiny'
    SMALL = 'Small'
    MEDIUM = 'Medium'
    LARGE = 'Large'
    HUGE = 'Huge'
    GARGANTUAN = 'Gargantuan'

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


class AbilityScore(Enum):
    STRENGTH = "Strength"
    DEXTERITY = "Dexterity"
    CONSTITUTION = "Constitution"
    INTELLIGENCE = "Intelligence"
    WISDOM = "Wisdom"
    CHARISMA = "Charisma"

    @classmethod
    def menu(cls):
        for i, value in enumerate(cls):
            print(f"({i}) {value} ")


class Skill(Enum):
    ACROBATICS = "Acrobatics"
    ANIMAL_HANDLING = "Animal Handling"
    ARCANA = "Arcana"
    ATHLETICS = "Athletics"
    DECEPTION = "Deception"
    HISTORY = "History"
    INSIGHT = "Insight"
    INTIMIDATION = "Intimidation"
    INVESTIGATION = "Investigation"
    MEDICINE = "Medicine"
    NATURE = "Nature"
    PERCEPTION = "Perception"
    PERFORMANCE = "Performance"
    PERSUASION = "Persuasion"
    RELIGION = "Religion"
    SLEIGHT_OF_HAND = "Sleight of Hand"
    STEALTH = "Stealth"
    SURVIVAL = "Survival"


PROFICIENT = "Proficient"
EXPERT = "Expertise"


class DamageType(Enum):
    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    POISON = "poison"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"


class Condition(Enum):
    BLEED = "bleed"
    BLINDED = "blinded"
    CHARMED = "charmed"
    DEAFENED = "deafened"
    EXHUASTION = "exhaustion"
    FRIGHTENED = "frightened"
    FROSTBITE = "frostbite"
    GRAPPLED = "grappled"
    INCAPACITATED = "incapacitated"
    INVISIBLE = "invisible"
    PARALYZED = "paralyzed"
    PETRIFIED = "petrified"
    POISONED = "poisoned"
    PRONE = "prone"
    RESTRAINED = "restrained"
    STUNNED = "stunned"
    UNCONCIOUS = "unconcious"


SKILL_TO_ABILITY = {
    Skill.ATHLETICS: AbilityScore.STRENGTH,
    Skill.ACROBATICS: AbilityScore.DEXTERITY,
    Skill.SLEIGHT_OF_HAND: AbilityScore.DEXTERITY,
    Skill.STEALTH: AbilityScore.DEXTERITY,
    Skill.ARCANA: AbilityScore.INTELLIGENCE,
    Skill.HISTORY: AbilityScore.INTELLIGENCE,
    Skill.INVESTIGATION: AbilityScore.INTELLIGENCE,
    Skill.NATURE: AbilityScore.INTELLIGENCE,
    Skill.RELIGION: AbilityScore.INTELLIGENCE,
    Skill.ANIMAL_HANDLING: AbilityScore.WISDOM,
    Skill.INSIGHT: AbilityScore.WISDOM,
    Skill.MEDICINE: AbilityScore.WISDOM,
    Skill.PERCEPTION: AbilityScore.WISDOM,
    Skill.SURVIVAL: AbilityScore.WISDOM,
    Skill.DECEPTION: AbilityScore.CHARISMA,
    Skill.INTIMIDATION: AbilityScore.CHARISMA,
    Skill.PERFORMANCE: AbilityScore.CHARISMA,
    Skill.PERSUASION: AbilityScore.CHARISMA
}


def score_to_mod(score):
    if score < 0:
        raise Exception("Ability Score is less than 0")

    return int((score-10)/2)


def proficiency_bonus(cr):
    return max(math.floor((cr - 1) / 4), 0) + 2


@dataclass
class AbilityDescription:
    name: str = "PLACEHOLDER ABILITY"
    description: str = "NO DESCRIPTION"

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(asdict(self))


@dataclass
class BaseAttack:
    class AttackType(Enum):
        MELEEWEAPON = 'Melee Weapon'
        RANGEDWEAPON = 'Ranged Weapon'
        MELEESPELL = 'Melee Spell'
        RANGEDSPELL = 'Ranged Spell'
        UNKNOWN = 'un'

    name: str = "PLACEHOLDER ATTACK"
    attack_mod: AbilityScore = AbilityScore.STRENGTH
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

    def get_attack_bonus(self, prof_bonus, attack_mod):
        return prof_bonus + attack_mod + self.attack_bonus

    @staticmethod
    def convert_json_attack(json_attack):
        if json_attack['type'] == BaseAttack.AttackType.MELEESPELL.value:
            return MeleeSpellAttack(name=json_attack['name'],
                                    attack_mod=AbilityScore(json_attack['attack_mod']),
                                    attack_bonus=int(json_attack['attack_bonus']),
                                    description=json_attack['description'],
                                    targets=json_attack['targets'],
                                    damage_dice=json_attack['damage_dice'],
                                    type=BaseAttack.AttackType(json_attack['type']),
                                    reach=json_attack['reach'])
        elif json_attack['type'] == BaseAttack.AttackType.MELEEWEAPON.value:
            return MeleeWeaponAttack(name=json_attack['name'],
                                     attack_mod=AbilityScore(json_attack['attack_mod']),
                                     attack_bonus=int(json_attack['attack_bonus']),
                                     description=json_attack['description'],
                                     targets=json_attack['targets'],
                                     damage_dice=json_attack['damage_dice'],
                                     type=BaseAttack.AttackType(json_attack['type']),
                                     reach=json_attack['reach'])
        elif json_attack['type'] == BaseAttack.AttackType.RANGEDWEAPON.value:
            return RangedWeaponAttack(name=json_attack['name'],
                                      attack_mod=AbilityScore(json_attack['attack_mod']),
                                      attack_bonus=int(json_attack['attack_bonus']),
                                      description=json_attack['description'],
                                      targets=json_attack['targets'],
                                      damage_dice=json_attack['damage_dice'],
                                      type=BaseAttack.AttackType(json_attack['type']),
                                      short_range=json_attack['short_range'],
                                      long_range=json_attack['long_range'])
        elif json_attack['type'] == BaseAttack.AttackType.RANGEDSPELL.value:
            return RangedSpellAttack(name=json_attack['name'],
                                     attack_mod=AbilityScore(json_attack['attack_mod']),
                                     attack_bonus=int(json_attack['attack_bonus']),
                                     description=json_attack['description'],
                                     targets=json_attack['targets'],
                                     damage_dice=json_attack['damage_dice'],
                                     type=BaseAttack.AttackType(json_attack['type']),
                                     range=json_attack['range'])
        else:
            raise ValueError('Invalid attack type')

    def rich_text(self, creature):
        to_hit = creature.ability_scores[self.attack_mod].name + creature.proficiency_bonus() + self.attack_bonus
        text = f'<b>{self.name}.</b> <i>{self.type.value} Attack:</i> +{to_hit} to hit, {self.targets}. <i>Hit:  </i>'
        for index, damage in enumerate(self.damage_dice):
            dicestring_damage = self.calculate_dicestring_damage(damage.dicestring,
                                                                 creature.ability_scores[self.attack_mod].value)
            text += f'{dicestring_damage} ({damage.dicestring}) {damage.type} damage'
            if index < len(self.damage_dice)-1:
                text += ' plus '
        text += f'. {self.description}'
        return text


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

    def rich_text(self, creature):
        to_hit = creature.ability_scores[self.attack_mod] + creature.proficiency_bonus() + self.attack_bonus
        text = f'<b>{self.name}.</b> <i>{self.type.value} Attack:</i> +{to_hit} to hit, ' \
               f'reach {self.reach} ft., {self.targets}. <i>Hit:  </i>'
        for index, damage in enumerate(self.damage_dice):
            dicestring_damage = self.calculate_dicestring_damage(damage["dicestring"],
                                                                 creature.ability_scores[self.attack_mod])
            text += f'{dicestring_damage} ({damage["dicestring"]}) {damage["damagetype"]} damage'
            if index < len(self.damage_dice)-1:
                text += ' plus '
        text += f'. {self.description}'
        return text


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

    def rich_text(self, creature):
        to_hit = creature.ability_scores[self.attack_mod] + creature.proficiency_bonus() + self.attack_bonus
        text = f'<b>{self.name}.</b> <i>{self.type.value} Attack:</i> +{to_hit} to hit, ' \
               f'ranged {self.short_range}/{self.long_range} ft., {self.targets}. <i>Hit:  </i>'
        for index, damage in enumerate(self.damage_dice):
            dicestring_damage = self.calculate_dicestring_damage(damage.dicestring,
                                                                 creature.ability_scores[self.attack_mod])
            text += f'{dicestring_damage} ({damage.dicestring}) {damage.type} damage'
            if index < len(self.damage_dice)-1:
                text += ' plus '
        text += f'. {self.description}'
        return text


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

    def rich_text(self, creature):
        to_hit = creature.ability_scores[self.attack_mod] + creature.proficiency_bonus() + self.attack_bonus
        text = f'<b>{self.name}.</b> <i>{self.type.value} Attack:</i> +{to_hit} to hit, ' \
               f'reach {self.reach} ft., {self.targets}. <i>Hit:  </i>'
        for index, damage in enumerate(self.damage_dice):
            dicestring_damage = self.calculate_dicestring_damage(damage.dicestring,
                                                                 creature.ability_scores[self.attack_mod])
            text += f'{dicestring_damage} ({damage.dicestring}) {damage.type} damage'
            if index < len(self.damage_dice)-1:
                text += ' plus '
        text += f'. {self.description}'
        return text


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

    def rich_text(self, creature):
        to_hit = creature.ability_scores[self.attack_mod] + creature.proficiency_bonus() + self.attack_bonus
        text = f'<b>{self.name}.</b> <i>{self.type.value} Attack:</i> +{to_hit} to hit, ' \
               f'range {self.range} ft., {self.targets}. <i>Hit:  </i>'
        for index, damage in enumerate(self.damage_dice):
            dicestring_damage = self.calculate_dicestring_damage(damage.dicestring,
                                                                 creature.ability_scores[self.attack_mod])
            text += f'{dicestring_damage} ({damage.dicestring}) {damage.type} damage'
            if index < len(self.damage_dice)-1:
                text += ' plus '
        text += f'. {self.description}'
        return text


class DamageModifier(Enum):
    VULNERABILITY = "VULNERABILITY"
    IMMUNITY = "IMMUNITY"
    RESISTANCE = "RESISTANCE"
