# This is a sample Python script.
import dataclasses
from enum import Enum
import math
import re
from dataclasses import dataclass, field
import time
import json


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


class Alignment(Enum):
    LG = "Lawful Good"
    NG = "Neutral Good"
    CG = "Chaotic Good"
    LN = "Lawful Neutral"
    N = "Neutral"
    CN = "Chaotic Neutral"
    LE = "Lawful Evil"
    NE = "Neutral Evil"
    CE = "Chaotic Evil"
    U = "Unaligned"
    CHANGEME = "CHANGEME"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def help(cls):
        print("Valid alignments:")
        for value in cls:
            print(value)

    @classmethod
    def convert(cls, value):
        if value in cls._value2member_map_:
            return cls(value)
        match value:
            case "LG":
                return Alignment.LG
            case "NG":
                return Alignment.NG
            case "CG":
                return Alignment.CG
            case "LN":
                return Alignment.LN
            case "N":
                return Alignment.N
            case "CN":
                return Alignment.CN
            case "LE":
                return Alignment.LE
            case "NE":
                return Alignment.NE
            case "CE":
                return Alignment.CE
            case "U":
                return Alignment.U
            case "UN":
                return Alignment.U
            case _:
                return Alignment.CHANGEME


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


@dataclass
class MonsterBlock():
    name: str = "PLACEHOLDER"
    size: Size = Size.CHANGEME
    alignment: Alignment = Alignment.CHANGEME
    acdesc: str = ""
    acbonus: int = 10
    ability_scores:dict = field(default_factory=dict)
    strength: int = 10
    dexterity: int = 10
    constitution: int = 10
    intelligence: int = 10
    wisdom: int = 10
    charisma: int = 10
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
    abilities: list = field(default_factory=list)
    actions: list = field(default_factory=list)
    reactions: list = field(default_factory=list)
    legendaryactions: list = field(default_factory=list)
    mythicdescription: str = None
    mythicactions: list = field(default_factory=list)

    VULNERABILITY = "VULNERABILITY"
    IMMUNITY = "IMMUNITY"
    RESISTANCE = "RESISTANCE"

    def toJSON(self):
        monster_dict = dataclasses.asdict(self)
        monster_dict['size'] = self.size.value
        monster_dict['alignment'] = self.alignment.value
        monster_dict['ability_scores'] = [v.value for v in self.ability_scores]
        monster_dict['abilities'] = [dataclasses.asdict(a) for a in self.abilities]
        monster_dict['actions'] = [c.toDict() for c in self.actions]
        monster_dict['reaction'] = [dataclasses.asdict(r) for r in self.reactions]
        monster_dict['legendaryactions'] = [dataclasses.asdict(l) for l in self.legendaryactions]
        monster_dict['mythicactions'] = [dataclasses.asdict(m) for m in self.mythicactions]
        return json.dumps(monster_dict)

    def saveJsonToFile(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        monster_json = open(timestr + '.json', "w")
        n = monster_json.write(self.toJSON())
        print(n)
        monster_json.close()



@dataclass
class AbilityDescription:
    name: str = "PLACEHOLDER ABILITY"
    description: str = "NO DESCRIPTION"

    def toDict(self):
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
    attack_mod: str = ""
    attack_bonus: int = 0
    description:str = ""
    targets: str = "one target."
    damage_dice: list = field(default_factory=list)
    type: AttackType = AttackType.UNKNOWN

    def toDict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        return attackdict

@dataclass
class MeleeWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEEWEAPON
    reach: int = 5

    def toDict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['reach'] = self.reach
        return attackdict


@dataclass
class RangedWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDWEAPON
    short_range: int = 20
    long_range: int = 60

    def toDict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['short_range'] = self.short_range
        attackdict['long_range'] = self.long_range
        return attackdict


@dataclass
class MeleeSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEESPELL
    reach: int = 5

    def toDict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['reach'] = self.reach
        return attackdict

@dataclass
class RangedSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDSPELL
    range: int = 30

    def toDict(self):
        attackdict = dataclasses.asdict(self)
        attackdict['type'] = self.type.value
        attackdict['range'] = self.reach
        return attackdict


# Regex for valid dice roll strings (like 1d6+4). M is used to inherit the
# ability modifier
# Valid Strings:
# 1d8
# 10d2+10
# 2d4+M
# 1d6-10
# 6d2-M
# 1d6+2d8+10d4+7
# 2d4+4d6+6d8+M
# Invalid Strings:
# 1d8+3M2
# 1d8-1d6+1d8+N
DICESTRINGPATTERN = r"^\d+d\d+(?:[+-]\d+|M)?(?:\+\d+d\d+(?:[+-]\d+|M)?)*$"

def sizeWizard():
    sizeinput = ""
    while not Size.has_value(sizeinput):
        print("Input Creature Size")
        Size.help()
        sizeinput = int(input("\n"))
        if Size.has_value(sizeinput):
            return Size(sizeinput)
        else:
            print("Invalid Size index")

def alignmentWizard():
    alignmentinput = ""
    while not Alignment.has_value(alignmentinput):
        alignmentinput = input("Alignment (eg. cg for Chaotic Good, "
                          "LN for Lawful Neutral, etc.) case insensitive\n").strip().upper()
        alignmentinput = Alignment.convert(alignmentinput)
        if alignmentinput != Alignment.CHANGEME:
            return alignmentinput
            continue
        elif alignmentinput == 'Help':
            Alignment.help()
        else:
            print("Invalid Alignment parameter. Type 'help' for a full list")

def calculateAverageDamage(dicestring, bonusdamage):
    match = re.match(DICESTRINGPATTERN, dicestring)
    if match:
        num_dice = int(match.group(1))
        num_sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        avg_roll = num_dice * ((num_sides + 1) / 2) + modifier
        return avg_roll
    else:
        raise ValueError('Invalid dice roll format')


def printSkillChoices(monster = None):
    if monster == None:
        for i, x in enumerate(SKILL_LIST):
            print(f'| {str(i)} - {x} |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(SKILL_LIST):
            isprof = "*" if monster.skills[x] else ""
            print(f"| {str(i)} - {x}{isprof} |")
        print('| (e)xit |')


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

def printDamageTypes(monster = None):
    if monster == None:
        for i, x in enumerate(DAMAGE_LIST):
            print('| ' + str(i) + ' - ' + x + ' |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(DAMAGE_LIST):
            isprof = ""
            if monster.damageimmunities[x]:
                isprof = "i"
            elif monster.damagevulnerabilities[x]:
                isprof = "v"
            elif monster.damageresistances[x]:
                isprof = "r"
            print(f"| {str(i)} - {x} {isprof}|")
        print('| (e)xit |')


def printConditionImmunities(monster = None):
    if monster == None:
        for i, x in enumerate(CONDITION_LIST):
            print('| ' + str(i) + ' - ' + x + ' |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(CONDITION_LIST):
            isprof = "*" if monster.conditionimmunities[x] else ""
            print(f"| {str(i)} - {x}{isprof}|")
        print('| (e)xit |')

def scoretomod(score):
    if score < 0:
        raise Exception("Ability Score is less than 0")

    return int((score-10)/2)


def getHitDice(hitdie, con):
    hitdiceprompt = ""
    while hitdiceprompt != 'a' or hitdiceprompt != 'auto' or not hitdiceprompt.isdigit():
        hitdiceprompt = input("Calculate hit dice and hit points.\n"
                              "Choose below where you would like to calculate hit dice from hit points ('auto' or 'a')\n"
                              "or just the input hit dice number and derive hit points\n")
        if hitdiceprompt == 'auto' or hitdiceprompt == 'a':
            hitpointsinput = ""
            while not hitpointsinput.isdigit():
                hitpointsinput = input("Enter hit point total\n"
                                       "Note: because of how hit dice correspond to hit points, choosing 'auto' may result in a \n"
                                       "hit point total slightly different from your chosen number\n")
                if hitpointsinput.isdigit():
                    hitpointsinput = int(hitpointsinput)
                    hitdice = calculatehitdice(hitdie=hitdie, con=con, hitpoints=hitpointsinput)
                    print(f"Creature has {str(hitdice)}d{hitdie} hitdice")
                    return hitdice
                else:
                    print("Invalid hitpoint total, expected an integer greater than 0")
        elif hitdiceprompt.isdigit():
            hitdice = int(hitdiceprompt)
            if hitdice > 0:
                return hitdice
            else:
                print("Invalid hitdice total, expected an integer greater than 0")
        else:
            print("Invalid input, expected 'a', 'auto', or an integer greater than 0 for manual hitdice input")


def calculatehitdice(hitdie, con, hitpoints):
    halfdie = hitdie/2
    hdtotal = 1
    temphp = halfdie + con
    while math.floor(temphp) < hitpoints:
        hdtotal += 1
        temphp += (halfdie + con)
    return hdtotal


def calculatehitpoints(hitdie, con, hitdice):
    halfdie = hitdie/2
    temphp = 0
    for i in range(hitdice):
        temphp += (halfdie+con)
    return math.floor(temphp)


def getAbilityScore(score):
    scoreinput = ""
    while not scoreinput.isdigit():
        scoreinput = input(f"Monster {score} Score (not the modifier)\n")
        if scoreinput.isdigit() and int(scoreinput) >= 0:
            return int(scoreinput)
        elif scoreinput == "":
            return 10
        else:
            print("Invalid " + score + "Score. Must be an integer greater than or equal to 0")


def saveProfWizard(monster):
    print('Entering saving throw wizard. Default response for options is no')
    strprof = input("Is the creature proficient in Strength saves, (y)es or (n)o\n")
    if strprof == 'y' or strprof =='yes':
        monster.strsave = True
    dexprof = input("Is the creature proficient in Dexterity saves, (y)es or (n)o\n")
    if dexprof == 'y' or dexprof =='yes':
        monster.dexsave = True
    conprof = input("Is the creature proficient in Constitution saves, (y)es or (n)o\n")
    if conprof == 'y' or conprof =='yes':
        monster.consave = True
    intprof = input("Is the creature proficient in Intelligence saves, (y)es or (n)o\n")
    if intprof == 'y' or intprof =='yes':
        monster.intsave = True
    wisprof = input("Is the creature proficient in Wisdom saves, (y)es or (n)o\n")
    if wisprof == 'y' or wisprof =='yes':
        monster.wissave = True
    chaprof = input("Is the creature proficient in Charisma saves, (y)es or (n)o\n")
    if chaprof == 'y' or chaprof =='yes':
        monster.chasave = True
    return monster


def toggleskill(monster, skill):
    monster.skills[skill] = not monster.skills[skill]


def toggledamage(monster, damage, damagemodifier=None):
    if damagemodifier == MonsterBlock.IMMUNITY:
        monster.damageimmunities[damage] = \
            not monster.damageimmunities[damage]
    elif damagemodifier == MonsterBlock.VULNERABILITY:
        monster.damagevulnerabilities[damage] = \
            not monster.damagevulnerabilities[damage]
    elif damagemodifier == MonsterBlock.RESISTANCE:
        monster.damageresistances[damage] = \
            not monster.damageresistances[damage]
    else:
        print(f"Damage Modifier does not match {MonsterBlock.IMMUNITY}, "
              f"{MonsterBlock.VULNERABILITY}, or {MonsterBlock.RESISTANCE}")


def togglecondition(monster, condition):
    monster.conditionimmunities[condition] = \
        not monster.conditionimmunities[condition]

def skillProfWizard(monster, initialize=True):
    print("Entering skill proficiency wizard. Default response for options is no")
    if initialize:
        for skill in SKILL_LIST:
            monster.skills[skill] = False

    skillprompt = 'WIZARD'
    while skillprompt != '' and skillprompt != 'exit':
        print("Enter the digit corresponding to the skill proficiency you would like to add to the creature.\n"
              "If the creature is already proficient with the chosen skill, that proficiency will be removed.\n"
              "Skills the creature is already proficient in are marked with a *"
              "Enter 'exit' or just hit return to exit the skill wizard\n")
        printSkillChoices(monster)
        skillprompt = input()
        if skillprompt.isdigit():
            skillchoice = int(skillprompt)
            if 0 <= skillchoice < len(SKILL_LIST):
                toggleskill(monster, SKILL_LIST[skillchoice])
            else:
                print(f'Invalid index. Expected integer between 0 and {len(SKILL_LIST)}')
                continue
        elif skillprompt == "" or skillprompt == "e" or skillprompt == "exit":
            break
        else:
            print(f'Invalid input. Expected integer between 0 and {len(SKILL_LIST)}')
    return monster


def damageTypeWizard(monster, mode=None, initialize=True):
    print(f"Entering damage {mode} wizard. Default response for options is no")
    damageprompt = 'WIZARD'
    if initialize:
        for damage in DAMAGE_LIST:
            monster.damageresistances[damage] = False
            monster.damageimmunities[damage] = False
            monster.damagevulnerabilities[damage] = False

    while damageprompt != '' and damageprompt != 'exit':
        print(f"Enter the digit corresponding to the damage {mode} you would like to add to the creature.\n"
            "If the creature is already proficient with the chosen skill, that proficiency will be removed.\n"
            "Skills the creature is already proficient in are marked with a *"
            "Enter 'exit' or just hit return to exit the skill wizard\n")
        printDamageTypes(monster)
        damage_prompt = input()
        if damage_prompt.isdigit():
            damage_choice = int(damage_prompt)
            if 0 <= damage_choice < len(DAMAGE_LIST):
                toggledamage(monster, DAMAGE_LIST[damage_choice], mode)
            else:
                print(f'Invalid index. Expected integer between 0 and {len(DAMAGE_LIST)}')
        elif damage_prompt == "" or damage_prompt == "e" or damage_prompt == "exit":
            break
        else:
            print(f'Invalid input. Expected integer between 0 and {len(DAMAGE_LIST)}')
    return monster


def conditionImmunityWizard(monster, initialize=True):
    print(f"Entering condition immunity wizard. Default response for options is no")
    conditionprompt = 'WIZARD'
    if initialize:
        for condition in CONDITION_LIST:
            monster.conditionimmunities[condition] = False

    while conditionprompt != '' and conditionprompt != 'exit':
        print(f"Enter the digit corresponding to the condition immunity you would like to add to the creature.\n"
            "If the creature is already immune to the chosen condition, that immunity will be removed.\n"
            "Conditions the creature is already immune to are marked with a *"
            "Enter 'exit' or just hit return to exit the skill wizard\n")
        printConditionImmunities(monster)
        condition_prompt = input()
        if condition_prompt.isdigit():
            condition_prompt = int(condition_prompt)
            if 0 <= condition_prompt < len(DAMAGE_LIST):
                togglecondition(monster, CONDITION_LIST[condition_prompt])
            else:
                print(
                    f'Invalid index. Expected integer between 0 and {len(CONDITION_LIST)}')
        elif condition_prompt == "" or condition_prompt == "e" or condition_prompt == "exit":
            break
        else:
            print(
                f'Invalid input. Expected integer between 0 and {len(CONDITION_LIST)}')
    return monster

def abilityWizard():
    ability_list = []
    ability_prompt = ''
    while ability_prompt != 'e' and ability_prompt != 'exit':
        print("Add abilities to the creature. Any input other than (e)xit will be "
              "treated as the name of the ability, after which you will be able"
              "to add a description to it.\n")
        ability_prompt = input()
        if ability_prompt != 'e' and ability_prompt != 'exit':
            newability = AbilityDescription(name = ability_prompt)
            description = input(f"Enter description for {newability}\n")
            newability.description = description
            ability_list.append(newability)

    return ability_list


def actionWizard():

    action_list = []
    action_prompt = ''
    while action_prompt != 'e' and action_prompt != 'exit':
        print("Add attacks or actions for the creature. Any input other than (e)xit will be "
              "treated as the name of the ability, after which you will be able"
              "to add a additional information about it, like damage or range\n")
        action_prompt = input()
        if action_prompt != 'e' and action_prompt != 'exit':
            action_name = action_prompt

            print(f"What type of action is {action_name}\n"
                  f"(1) Melee Weapon | (2) Ranged Weapons\n"
                  f"(3) Melee Spell  | (4) Ranged Spell\n"
                  f"(5) Non-Attack (eg. Breath Weapon)\n"
                  f"Default is Melee Weapon\n")

            actiontype_prompt = input("\n")

            if actiontype_prompt == '5':
                description = input("Description for the action.\n")
                action_list.append(
                    AbilityDescription(name = action_name,
                                       description = description))
                continue


            attack_mod, attack_bonus = getAttackBonus()
            damage_dice = getDamageDice()
            description = input("Input a description for the attack. Most "
                                "attacks do not have a description, this is "
                                "only used for attacks that have additional "
                                "effects like a Marilith's trail grapple.\n")

            if actiontype_prompt == '2':
                action_list.append(
                    rangedWeaponAttackWizard(name = action_name,
                                             attack_mod = attack_mod,
                                             attack_bonus = attack_bonus,
                                             damage_dice = damage_dice,
                                             description = description))
            elif actiontype_prompt == '3':
                action_list.append(
                    meleeSpellAttackWizard(name = action_name,
                                           attack_mod = attack_mod,
                                           attack_bonus = attack_bonus,
                                           damage_dice = damage_dice,
                                           description = description))
            elif actiontype_prompt == '4':
                action_list.append(
                    rangedSpellAttackWizard(name=action_name,
                                            attack_mod=attack_mod,
                                            attack_bonus=attack_bonus,
                                            damage_dice=damage_dice,
                                            description=description))
            else:
                action_list.append(
                    meleeWeaponAttackWizard(name=action_name,
                                            attack_mod=attack_mod,
                                            attack_bonus=attack_bonus,
                                            damage_dice=damage_dice,
                                            description=description))
    print("Exiting attack setup")
    return action_list


def getAttackBonus():
    attackmod = None
    while attackmod is None:
        print("What ability is the attack made with?")
        AbilityScores.menu()
        modPrompt = input("\n")
        if modPrompt.isdigit() and 0 <= int(modPrompt) < len(
                AbilityScores):
            attackmod = int(modPrompt)
            continue
        else:
            print(f"Invalid input. Expected an integer between 0 "
                  f"and {len(AbilityScores)}")

    attackbonus = None
    while attackbonus is None:
        bonusPrompt = input("What is the attack's to hit bonus. Do not add a + "
                            "next to the integer bonus. Negative bonuses are "
                            "accepted. Default value is 0\n Note: The base "
                            "attack bonus of the attack is the proficiency "
                            "bonus of the creature plus the ability mod for "
                            "the attack. This bonus shpuld only be used for "
                            "other modifiers like a +1 weapon.\n")
        if bonusPrompt.isdigit():
            attackbonus = int(bonusPrompt)
        elif bonusPrompt == "":
            attackbonus = 0
        else:
            print("Invalid input. Expected an integer")

    return attackmod, attackbonus


def getDamageDice():
    damagedice = []
    damage_prompt = ''
    while damage_prompt != 'e' or damage_prompt != 'exit':
        print("Add the damage the attack deals. Input the damage dice for"
              "the attack in the form 'XdY+Z. More than one set of dice can"
              "be input in this section, you'll input one at a time. \n"
              "Note: The damage bonus is not automatically inherited from the "
              "attack's ability modifier set earlier.\n If you enter an "
              "integer for Z, that value will be used. Instead, you can enter"
              "'M', which will use the attack's ability score automatically\n")
        damage_prompt = input()
        if re.match(DICESTRINGPATTERN, damage_prompt):
            damagepair = {"dicestring":damage_prompt}
            print("What is the damage type?")
            printDamageTypes()
            damage_prompt = input("\n")
            if damage_prompt.isdigit():
                damage_prompt = int(damage_prompt)
                if 0 <= damage_prompt < len(DAMAGE_LIST):
                    damagepair['damagetype'] = DAMAGE_LIST[damage_prompt]
                    damagedice.append(damagepair)
            else:
                print(f'Invalid index. Expected integer between 0 and '
                      f'{len(DAMAGE_LIST)}')
        elif damage_prompt != 'e' or damage_prompt != 'exit':
            break
        else:
            print("Dicestring does not match the pattern")
    return damagedice

def validDistance(distance, default):
    if distance.isdigit():
        if int(distance) % 5 == 0:
            return int(distance)
        else:
            raise ValueError("Valid distances must be a multiple of 5")
    elif distance == "":
        return default
    else:
        raise TypeError("Distances must be a number or an empty string for a default value")

def getDistance(prompt, default):
    reach = None
    while reach is None:
        try:
            reach_input = input(f"What is the reach for the {type} "
                                f"Must be an integer multiple of 5. Default {default}\n")
            reach = validDistance(reach_input, default)
        except (ValueError, TypeError) as e:
            print(e.args[0])

    return reach

def meleeWeaponAttackWizard(name, attack_mod, attack_bonus,
                            damage_dice, description):
    attack = MeleeWeaponAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    attack.reach = getDistance("What is the range for the melee weapon attack\n", 5)
    return attack


def rangedWeaponAttackWizard(name, attack_mod, attack_bonus,
                             damage_dice, description):
    attack = RangedWeaponAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    attack.short_range = getDistance("What is the short range for the ranged attack.", 20)

    attack.long_range = getDistance("What is the long range for the ranged attack.", 60)

    return attack


def meleeSpellAttackWizard(name, attack_mod, attack_bonus,
                           damage_dice, description):

    attack = MeleeSpellAttack(name=name,
                              attack_mod=attack_mod,
                              attack_bonus=attack_bonus,
                              damage_dice=damage_dice,
                              description=description)

    attack.reach = getDistance("What is the range for the melee spell attack\n", 5)

    return attack


def rangedSpellAttackWizard(name, attack_mod, attack_bonus,
                            damage_dice, description):
    attack = RangedSpellAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    attack.reach = getDistance("What is the range for the ranged spell attack\n", 30)

    return attack


def reactionWizard():
    reaction_list = []
    reaction_prompt = ''
    while reaction_prompt != 'e' and reaction_prompt != 'exit':
        reaction_prompt = input("Add reactions for the creature. Any input other than (e)xit "
              "will be treated as the name of the reaction\n")
        if reaction_prompt != 'e' and reaction_prompt != 'exit':
            description = input("Description for the action.\n")
            reaction_list.append(
                AbilityDescription(name=reaction_prompt,
                                   description=description))
    return reaction_list


def legendaryActionWizard():
    legendary_action_list = []
    legendary_toggle = input("Does the creature have legendary actions?"
                             "(y)es or (n)o\n")
    if legendary_toggle == 'y' or legendary_toggle == 'yes':
        legendary_prompt = ''
        while legendary_prompt != 'e' and legendary_prompt != 'exit':
            print("Add legendary actions to the creature. Any input other "
                  "than (e)xit will be treated as the name of the action, "
                  "after which you will be able to add a description to it.\n")
            legendary_prompt = input()
            if legendary_prompt != 'e' and legendary_prompt != 'exit':
                legendaryaction = AbilityDescription(name = legendary_prompt)
                description = input(f"Enter description for {legendaryaction}\n")
                legendaryaction.description = description
                legendary_action_list.append(legendaryaction)

    return legendary_action_list


def mythicActionWizard():
    mythic_action_list = []
    mythic_description = ""
    mythic_toggle = input("Does the creature have "
                          "mythicactions? (y)es or (n)o\n")
    if mythic_toggle == 'y' or mythic_toggle == 'yes':
        mythic_description = input("What is the description for the "
                                   "creature's Mythic Action trait?\n")
        mythic_prompt = ''
        while mythic_prompt != 'e' and mythic_prompt != 'exit':
            print("Add legendary actions to the creature. Any input other "
                  "than (e)xit will be treated as the name of the action, "
                  "after which you will be able to add a description to it.\n")
            mythic_prompt = input()
            if mythic_prompt != 'e' and mythic_prompt != 'exit':
                mythicaction = AbilityDescription(name = mythic_prompt)
                description = input(f"Enter description for {mythicaction}\n")
                mythicaction.description = description
                mythic_action_list.append(mythicaction)

    return mythic_description, mythic_action_list


def interactiveMonsterGen():
    monster = MonsterBlock()
    print("Welcome to the interactive 5e creature generator\n"
          "All of the following fields are optional, just hit return to skip one\n")

    # Get creature name
    nameinput = input("Creature Name\n")
    monster.name = "PLACEHOLDER" if nameinput == "" else nameinput

    # Get creature size
    monster.size = sizeWizard()


    # Get creature alignment
    monster.alignment = alignmentWizard()

    # Get creature type
    creaturetype = input("Monster Type (eg. celestial, humanoid(demi-human), etc\n").strip().upper()
    monster.type = creaturetype

    # Get AC bonus
    acbonusinput = "NOTADIGIT"
    while not acbonusinput.isdigit():
        acbonusinput = input("Monster AC Bonus (eg. armor bonus) disgregading dex bonuses\n")

        if acbonusinput.isdigit():
            monster.acbonus = int(acbonusinput)
            break
        elif acbonusinput == "":
            monster.acbonus = 0
            break
        else:
            print("Invalid AC bonus. Must be an integer greater than or equal to 0\n")

    # Get AC Bonus description
    monster.acdesc = input("AC Bonus description (eg. plate, natural armor, mage armor, etc.\n")

    # Get Ability Scores
    monster.ability_scores[AbilityScores.STRENGTH] = getAbilityScore("Strength")
    monster.ability_scores[AbilityScores.DEXTERITY]  = getAbilityScore("Dexterity")
    monster.ability_scores[AbilityScores.CONSTITUTION] = getAbilityScore("Constitution")
    monster.ability_scores[AbilityScores.INTELLIGENCE] = getAbilityScore("Intelligence")
    monster.ability_scores[AbilityScores.WISDOM]  = getAbilityScore("Wisdom")
    monster.ability_scores[AbilityScores.CHARISMA]  = getAbilityScore("Charisma")

    # Get hit dice through the hp wizard
    monster.hitdice = getHitDice(hitdie=Size.hitdice(monster.size),
                                 con=monster.constitution)
    monster.hitpoints = calculatehitpoints(hitdie=Size.hitdice(monster.size),
                                           con=monster.constitution,
                                           hitdice=monster.hitdice)


    # Get speed
    speedinput = input("Monster Speed (default 30 ft.)\n")
    monster.speed = "30 ft." if speedinput == "" else speedinput

    # Get save proficients
    saveprompt = input("Does the creature have any saving throw proficiencies: (y)es or (n)o? Default no\n")
    if saveprompt == 'y' or saveprompt == 'yes':
        monster = saveProfWizard(monster)

    # Get skill proficiencies
    skillprompt = input("Does the creature have any skill proficiencies: (y)es or (n)o? Default no\n")
    if skillprompt == 'y' or skillprompt == 'yes':
        monster = skillProfWizard(monster)

    # Get damage vulnerabilities
    vulnerabilityprompt = input("Does the creature have any damage vulnerabilities: (y)es or (n)o? Default no\n")
    if vulnerabilityprompt == 'y' or vulnerabilityprompt == 'yes':
        monster = damageTypeWizard(monster, MonsterBlock.VULNERABILITY, initialize=True)

    # Get damage resistances
    resistanceprompt = input(
        "Does the creature have any damage resistances: (y)es or (n)o? Default no\n")
    if resistanceprompt == 'y' or resistanceprompt == 'yes':
        monster = damageTypeWizard(monster, MonsterBlock.RESISTANCE, initialize=True)


    # Get damage resistances
    immunityprompt = input(
        "Does the creature have any damage immunities: (y)es or (n)o? Default no\n")
    if immunityprompt == 'y' or immunityprompt == 'yes':
        monster = damageTypeWizard(monster, MonsterBlock.IMMUNITY, initialize=True)

    conditionprompt = input("Does the creature have any condition immunities: (y)es or (n)o? Default no\n")
    if conditionprompt == 'y' or conditionprompt == 'yes':
        monster = conditionImmunityWizard(monster)

    # Get senses
    senseinput = input("Monster Senses (eg. darkvision 60 ft., blindsight 10 ft.\n")
    monster.senses = senseinput

    # Get languages
    languageinput = input("Monster languages (eg. Common, Draconic, understands Gnomish\n")
    monster.senses = languageinput

    monster.abilities = abilityWizard()
    monster.actions = actionWizard()
    monster.reactions = reactionWizard()
    monster.legendaryactions = legendaryActionWizard()
    monster.mythicdescription, monster.mythicactions = mythicActionWizard()

    return monster


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    monster = interactiveMonsterGen()
    monster.saveJsonToFile()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# ___
# > ## Monster Name
# >*Size, Alignment*
# > ___
# > - **Armor Class** AC
# > - **Hit Points** Hitpoints
# > - **Speed** Speed
# >___
# >|STR|DEX|CON|INT|WIS|CHA|
# >|:---:|:---:|:---:|:---:|:---:|:---:|
# >|Str (Mod)|Dex (Mod)|Con (Mod)|Int (Mod)|Wis (Mod)|Cha (Mod)|
# >___
# > - **Saving Throws** saving_throws
# > - **Skills** skills
# > - **Damage Vulnerabilities** damage_vulnerabilities
# > - **Damage Resistances** Resi stances
# > - **Damage Immunities** Damage_Immunities
# > - **Condition Immunities** condition_Immunities
# > - **Senses** Senses
# > - **Languages** Languages
# > - **Challenge** Challenge and Xp
# > ___
# >
# > ### Actions
# > ***Multiattack.*** The Creature Name makes Number and type of attacks
# >
# > ***Ability Description.*** *Attack Style:* Attack Bonus to hit, Reach/Range, one target. *Hit:* Damage Damage Type damage
# >
# > ***General Ability Description.*** General Attack Description
