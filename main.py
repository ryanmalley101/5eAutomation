# This is a sample Python script.
from enum import Enum
import math
import re
from dataclasses import dataclass, field
import time
import json

class Size(Enum):
    TINY = "Tiny"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    HUGE = "Huge"
    GARGANTUAN = "Gargantuan"
    CHANGEME = "CHANGEME"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def help(cls):
        print("Valid sizes:")
        for value in cls:
            print(value)

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
            return value
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
            case _:
                return Alignment.CHANGEME

class AbilityScores(Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"


    def menu(cls):
        for i, value in enumerate(cls):
            print(f"({i}) value ")

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
class MonsterBlock:
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
    damageimmunities: set = field(default_factory=set)
    damageresistances: set = field(default_factory=set)
    damagevulnerabilities: set = field(default_factory=set)
    conditionimmunities: set = field(default_factory=set)
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


@dataclass
class AbilityDescription:
    name: str = "PLACEHOLDER ABILITY"
    description: str = "NO DESCRIPTION"


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


@dataclass
class MeleeWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEEWEAPON
    reach: int = 5


@dataclass
class RangedWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDWEAPON
    short_range: int = 20
    long_range: int = 60


@dataclass
class MeleeSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEESPELL
    reach: int = 5


@dataclass
class RangedSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDSPELL
    range: int = 30


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
            print('| ' + str(i) + ' - ' + x + ' |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(SKILL_LIST):
            isprof = "*" if monster.skills[x] else ""
            print(f"| {str(i)} - + {x} + {isprof}|")
        print('| (e)xit |')


damage_list = [
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
]


def printDamageTypes(monster = None):
    if monster == None:
        for i, x in enumerate(damage_list):
            print('| ' + str(i) + ' - ' + x + ' |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(damage_list):
            isprof = ""
            if monster.damageimmunities[x]:
                isprof = "i"
            elif monster.damagevulnerabilities[x]:
                isprof = "v"
            elif monster.damageresistances[x]:
                isprof = "r"
            isprof = "*" if monster.skills[x] else ""
            print(f"| {str(i)} - + {x} + {isprof}|")
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
                                       "hit point total slightly different from your chosen number")
                if hitpointsinput.isdigit():
                    hitpointsinput = int(hitpointsinput)
                    hitdice = calculatehitdice(hitdie=hitdie, con=con, hitpoints=hitpointsinput)
                    print("Creature has " + str(hitdice) + "d" + hitdie + " hitdice")
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
        scoreinput = input("Monster Strength Score (not the modifier)")
        if scoreinput.isdigit() and int(score) >= 0:
            return int(scoreinput)
        else:
            print("Invalid " + score + "Score. Must be an integer greater than or equal to 0")


def saveProfWizard(monster):
    print('Entering saving throw wizard. Default response for options is no')
    strprof = input("Is the creature proficient in Strength saves, (y)es or (n)o")
    if strprof == 'y' or strprof =='yes':
        monster.strsave = True
    dexprof = input("Is the creature proficient in Dexterity saves, (y)es or (n)o")
    if dexprof == 'y' or dexprof =='yes':
        monster.dexsave = True
    conprof = input("Is the creature proficient in Constitution saves, (y)es or (n)o")
    if conprof == 'y' or conprof =='yes':
        monster.consave = True
    intprof = input("Is the creature proficient in Intelligence saves, (y)es or (n)o")
    if intprof == 'y' or intprof =='yes':
        monster.intsave = True
    wisprof = input("Is the creature proficient in Wisdom saves, (y)es or (n)o")
    if wisprof == 'y' or wisprof =='yes':
        monster.wissave = True
    chaprof = input("Is the creature proficient in Charisma saves, (y)es or (n)o")
    if chaprof == 'y' or chaprof =='yes':
        monster.chasave = True
    return monster


def toggleskill(monster, skillindex):
    monster.skills[SKILL_LIST[skillindex]] = not monster.skills[SKILL_LIST[skillindex]]


def toggledamage(monster, damage, damagemodifier=None):
    if damagemodifier == MonsterBlock.IMMUNITY:
        if damage in monster.damageimmunities:
            monster.damageimmunities.remove(damage)
        else:
            monster.damageimmunities.add(damage)
    elif damagemodifier == MonsterBlock.VULNERABILITY:
        if damage in monster.damagevulnerabilities:
            monster.damagevulnerabilities.remove(damage)
        else:
            monster.damagevulnerabilities.add(damage)
    elif damagemodifier == MonsterBlock.RESISTANCE:
        if damage in monster.damageresistances:
            monster.damageresistances.remove(damage)
        else:
            monster.damageresistances.add(damage)
    else:
        print(f"Damage Modifier does not match {MonsterBlock.IMMUNITY}, "
              f"{MonsterBlock.VULNERABILITY}, or {MonsterBlock.RESISTANCE}")


def skillProfWizard(monster):
    print("Entering skill proficiency wizard. Default response for options is no")
    skillprompt = 'WIZARD'
    while skillprompt != '' and skillprompt != 'exit':
        print("Enter the digit corresponding to the skill proficiency you would like to add to the creature.\n"
              "If the creature is already proficient with the chosen skill, that proficiency will be removed.\n"
              "Skills the creature is already proficient in are marked with a *"
              "Enter 'exit' or just hit return to exit the skill wizard")
        printSkillChoices(monster)
        skillprompt = input()
        if skillprompt.isdigit():
            skillchoice = int(skillprompt)
            if 0 <= skillchoice < len(SKILL_LIST):
                toggleskill(monster, SKILL_LIST[skillchoice])
            else:
                print(f'Invalid index. Expected integer between 0 and {len(SKILL_LIST)}')
                continue
        else:
            print(f'Invalid input. Expected integer between 0 and {len(SKILL_LIST)}')
    return monster


def damageTypeWizard(monster, mode=None):
    print(f"Entering damage {mode} wizard. Default response for options is no")
    damageprompt = 'WIZARD'
    while damageprompt != '' and damageprompt != 'exit':
        print(f"Enter the digit corresponding to the damage {mode} you would like to add to the creature.\n"
            "If the creature is already proficient with the chosen skill, that proficiency will be removed.\n"
            "Skills the creature is already proficient in are marked with a *"
            "Enter 'exit' or just hit return to exit the skill wizard")
        printDamageTypes(monster)
        damage_choice = input()
        if damageprompt.isdigit():
            damage_choice = int(damage_choice)
            if 0 <= damage_choice < len(damage_list):
                toggledamage(monster, damage_list[damage_choice], mode)
            else:
                print(f'Invalid index. Expected integer between 0 and {len(damage_list)}')
        else:
            print(f'Invalid input. Expected integer between 0 and {len(damage_list)}')
    return monster


def abilityWizard():
    ability_list = []
    ability_prompt = ''
    while ability_prompt is not 'e' and ability_prompt is not 'exit':
        print("Add abilities to the creature. Any input other than (e)xit will be "
              "treated as the name of the ability, after which you will be able"
              "to add a description to it.")
        ability_prompt = input()
        if ability_prompt is not 'e' and ability_prompt is not 'exit':
            newability = AbilityDescription(name = ability_prompt)
            description = input(f"Enter description for {newability}")
            newability.description = description
            ability_list.append(newability)

    return ability_list


def attackWizard():

    action_list = []
    action_prompt = ''
    while action_prompt is not 'e' and action_prompt is not 'exit':
        print("Add attacks or actions for the creature. Any input other than (e)xit will be "
              "treated as the name of the ability, after which you will be able"
              "to add a additional information about it, like damage or range")
        action_prompt = input()
        if action_prompt is not 'e' and action_prompt is not 'exit':
            action_name = action_prompt

            print(f"What type of action is {action_name}\n"
                  f"(1) Melee Weapon | (2) Ranged Weapons\n"
                  f"(3) Melee Spell  | (4) Ranged Spell\n"
                  f"(5) Non-Attack (eg. Breath Weapon)\n"
                  f"Default is Melee Weapon\n")

            actiontype_prompt = input()

            if actiontype_prompt == '5':
                description = input("Description for the action.")
                action_list.append(
                    AbilityDescription(name = action_name,
                                       description = description))
                continue


            attack_mod, attack_bonus = getAttackBonus()
            damage_dice = getDamageDice()
            description = input("Input a description for the attack. Most "
                                "attacks do not have a description, this is "
                                "only used for attacks that have additional "
                                "effects like a Marilith's trail grapple.")

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
        modPrompt = input()
        if modPrompt.isdigit() and 0 >= int(modPrompt) < len(
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
                            "other modifiers like a +1 weapon.")
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
              "attack's ability modifier set earlier. If you enter an "
              "integer for Z, that value will be used. Instead, you can enter"
              "'M', which will use the attack's ability score automatically")
        damage_prompt = input()
        if re.match(DICESTRINGPATTERN, damage_prompt):
            damagepair = {"dicestring":damage_prompt}
            print("What is the damage type?")
            printDamageTypes()
            damageprompt = input()
            if damageprompt.isdigit():
                damage_choice = int(damage_choice)
                if 0 <= damage_choice < len(damage_list):
                    damagepair['damagetype'] = damage_list[damage_choice]
                    damagedice.append(damagepair)
            else:
                print(f'Invalid index. Expected integer between 0 and '
                      f'{len(damage_list)}')

    return damagedice


def meleeWeaponAttackWizard(name, attack_mod, attack_bonus,
                            damage_dice, description):
    attack = MeleeWeaponAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    reach_input = int(input("What is the reach for the melee attack. "
                            "Must be an integer multiple of 5. Default 5"))

    attack.reach = int(reach_input) if reach_input % 5 == 0 else 5
    return attack


def rangedWeaponAttackWizard(name, attack_mod, attack_bonus,
                             damage_dice, description):
    attack = RangedWeaponAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)
    short_input = int(input("What is the short range for the ranged attack. "
                        "Must be an integer multiple of 5. Default 20"))
    attack.short_range = int(short_input) if short_input % 5 == 0 else 20

    long_input = int(input("What is the long range for the ranged attack. "
                        "Must be an integer multiple of 5. Default 60"))
    attack.long_range = int(long_input) if long_input % 5 == 0 else 20

    return attack


def meleeSpellAttackWizard(name, attack_mod, attack_bonus,
                           damage_dice, description):

    attack = MeleeSpellAttack(name=name,
                              attack_mod=attack_mod,
                              attack_bonus=attack_bonus,
                              damage_dice=damage_dice,
                              description=description)

    reach_input = int(input("What is the reach for the melee attack. "
                            "Must be an integer multiple of 5. Default 5"))

    attack.reach = int(reach_input) if reach_input % 5 == 0 else 5
    return attack


def rangedSpellAttackWizard(name, attack_mod, attack_bonus,
                            damage_dice, description):
    attack = RangedSpellAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    range_input = int(input("What is the range for the ranged attack. "
                        "Must be an integer multiple of 5. Default 30"))
    attack.range = int(range_input) if range_input % 5 == 0 else 30

    return attack


def reactionWizard():
    reaction_list = []
    reaction_prompt = ''
    while reaction_prompt is not 'e' and reaction_prompt is not 'exit':
        print("Add reactions for the creature. Any input other than (e)xit "
              "will be treated as the name of the reaction")
        reaction_prompt = input()
        if reaction_prompt is not 'e' and reaction_prompt is not 'exit':
            description = input("Description for the action.")
            reaction_list.append(
                AbilityDescription(name=reaction_prompt,
                                   description=description))
    return reaction_list


def legendaryActionWizard():
    legendary_action_list = []
    legendary_toggle = input("Does the creature have legendary actions?"
                             "(y)es or (n)o")
    if legendary_toggle == 'y' or legendary_toggle == 'yes':
        legendary_prompt = ''
        while legendary_prompt is not 'e' and legendary_prompt is not 'exit':
            print("Add legendary actions to the creature. Any input other "
                  "than (e)xit will be treated as the name of the action, "
                  "after which you will be able to add a description to it.")
            legendary_prompt = input()
            if legendary_prompt is not 'e' and legendary_prompt is not 'exit':
                legendaryaction = AbilityDescription(name = legendary_prompt)
                description = input(f"Enter description for {legendaryaction}")
                legendaryaction.description = description
                legendary_action_list.append(legendaryaction)

    return legendary_action_list


def mythicActionWizard():
    mythic_action_list = []
    mythic_description = ""
    mythic_toggle = input("Does the creature have "
                          "mythicactions? (y)es or (n)o")
    if mythic_toggle == 'y' or mythic_toggle == 'yes':
        mythic_description = input("What is the description for the "
                                   "creature's Mythic Action trait?")
        mythic_prompt = ''
        while mythic_prompt is not 'e' and mythic_prompt is not 'exit':
            print("Add legendary actions to the creature. Any input other "
                  "than (e)xit will be treated as the name of the action, "
                  "after which you will be able to add a description to it.")
            mythic_prompt = input()
            if mythic_prompt is not 'e' and mythic_prompt is not 'exit':
                mythicaction = AbilityDescription(name = mythic_prompt)
                description = input(f"Enter description for {mythicaction}")
                mythicaction.description = description
                mythic_action_list.append(mythicaction)

    return mythic_description, mythic_action_list

def interactiveMonsterGen():
    monster = MonsterBlock()
    print("Welcome to the interactive 5e creature generator\n"
          "All of the following fields are optional, just hit return to skip one\n")

    # Get creature name
    nameinput = input("Creature Name")
    monster.name = "PLACEHOLDER" if nameinput == "" else nameinput

    # Get creature size
    sizeinput = ""
    while not Size.has_value(sizeinput):
        sizeinput = input("Size (eg. Tiny, Small, Medium) case-insensitive").strip().upper()
        if Size.has_value(sizeinput):
            monster.size = sizeinput
            continue
        elif sizeinput == 'Help':
            Size.help()
        else:
            print("Invalid Size parameter. Type 'help' for a full list")

    # Get creature alignment
    alignmentinput = ""
    while not Alignment.has_value(alignmentinput):
        alignmentinput = input("Alignment (eg. cg for Chaotic Good, "
                          "LN for Lawful Neutral, etc.) case insensitive").strip().upper()
        alignmentinput = Alignment.convert(alignmentinput)
        if alignmentinput != Alignment.CHANGEME:
            monster.alignment = alignmentinput
            continue
        elif sizeinput == 'Help':
            Alignment.help()
        else:
            print("Invalid Alignment parameter. Type 'help' for a full list")

    # Get creature type
    creaturetype = input("Monster Type (eg. celestial, humanoid(demi-human), etc").strip().upper()
    monster.type = creaturetype

    # Get AC bonus
    acbonusinput = "NOTADIGIT"
    while not acbonusinput.isdigit():
        acbonusinput = input("Monster AC Bonus (eg. armor bonus) disgregading dex bonuses")

        if acbonusinput.isdigit():
            monster.acbonus = int(acbonusinput)
            continue
        else:
            print("Invalid AC bonus. Must be an integer greater than or equal to 0")

    # Get AC Bonus description
    monster.acdesc = input("AC Bonus description (eg. plate, natural armor, mage armor, etc.")

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
    speedinput = input("Monster Speed (default 30 ft.)")
    monster.speed = "30 ft." if speedinput == "" else speedinput

    # Get save proficients
    saveprompt = input("Does the creature have any saving throw proficiencies: (y)es or (n)o? Default no")
    if saveprompt == 'y' or saveprompt == 'yes':
        monster = saveProfWizard(monster)

    # Get skill proficiencies
    skillprompt = input("Does the creature have any skill proficiencies: (y)es or (n)o? Default no")
    if skillprompt == 'y' or skillprompt == 'yes':
        monster = skillProfWizard(monster)

    # Get damage vulnerabilities
    vulnerabilityprompt = input("Does the creature have any damage vulnerabilities: (y)es or (n)o? Default no")
    if vulnerabilityprompt == 'y' or vulnerabilityprompt == 'yes':
        monster = damageTypeWizard(monster, MonsterBlock.VULNERABILITY)

    # Get damage resistances
    resistanceprompt = input(
        "Does the creature have any damage resistances: (y)es or (n)o? Default no")
    if resistanceprompt == 'y' or resistanceprompt == 'yes':
        monster = damageTypeWizard(monster, MonsterBlock.RESISTANCE)


    # Get damage resistances
    immunityprompt = input(
        "Does the creature have any damage immunities: (y)es or (n)o? Default no")
    if immunityprompt == 'y' or immunityprompt == 'yes':
        monster = damageTypeWizard(monster, MonsterBlock.IMMUNITY)

    # Get senses
    senseinput = input("Monster Senses (eg. darkvision 60 ft., blindsight 10 ft.")
    monster.senses = senseinput

    # Get languages
    languageinput = input("Monster languages (eg. Common, Draconic, understands Gnomish")
    monster.senses = languageinput

    monster.abilities = abilityWizard()
    monster.attacks = attackWizard()
    monster.reactions = reactionWizard()
    monster.legendaryactions = legendaryActionWizard()
    monster.mythicdescription, monster.mythicactions = mythicActionWizard()

    return monster


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    timestr = time.strftime("%Y%m%d-%H%M%S")
    monster_json = open('monster' + timestr, "w")
    n = monster_json.write(json.dumps(interactiveMonsterGen()))

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
