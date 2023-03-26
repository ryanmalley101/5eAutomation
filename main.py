# This is a sample Python script.
from enum import Enum
import math
import re
from dataclasses import dataclass, field
from typing import List

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
    tohit: int = 0
    description = ""
    targets: str = "one target."
    damagedice:list = field(default_factory=list)
    type = AttackType.UNKNOWN


@dataclass
class MeleeWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEEWEAPON
    reach: int = 10


@dataclass
class RangedWeaponAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDWEAPON
    short_range: int = 0
    long_range: int = 0


@dataclass
class MeleeSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.MELEESPELL
    reach: int = 0


@dataclass
class RangedSpellAttack(BaseAttack):
    type = BaseAttack.AttackType.RANGEDSPELL
    range: int = 0


# Regex for valid dice roll strings (like 1d6+4)
DICESTRINGPATTERN = '^(?:(\d+)d(\d+))(?:([+-])(\d+))?$'
def calculateAverageDamage(dicestring, bonusdamage):
    match = re.match(r'^(\d+)d(\d+)([+-]\d+)?$', dicestring)
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
        for i, x in enumerate(skill_list):
            print('| ' + str(i) + ' - ' + x + ' |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(skill_list):
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
        for i, x in enumerate(skill_list):
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
    monster.skills[skill_list[skillindex]] = not monster.skills[skill_list[skillindex]]


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
                continue
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
    attack_wizard = []
    attack_prompt = ''
    while action_prompt is not 'e' and action_prompt is not 'exit':
        print("Add attacks or actions for the creature. ny input other than (e)xit will be "
              "treated as the name of the ability, after which you will be able"
              "to add a additional information about it, like damage or range")
        action_prompt = input()
        if action_prompt is not 'e' and action_prompt is not 'exit':
            action_name = action_prompt


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
    monster.strength = getAbilityScore("Strength")
    monster.dexterity = getAbilityScore("Dexterity")
    monster.constitution = getAbilityScore("Constitution")
    monster.intelligence = getAbilityScore("Intelligence")
    monster.wisdom = getAbilityScore("Wisdom")
    monster.charisma = getAbilityScore("Charisma")

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


    return monster

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    printSkillChoices()

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
