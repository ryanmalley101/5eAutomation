# This is a sample Python script.

from statblockdatastructs import *
import math
import re
from patterns import DICESTRINGPATTERN

def size_wizard():
    sizeinput = ""
    while not Size.has_value(sizeinput):
        print("Input Creature Size")
        Size.help()
        sizeinput = int(input("\n"))
        if Size.has_value(sizeinput):
            return Size(sizeinput)
        else:
            print("Invalid Size index")


def alignment_wizard():
    alignmentinput = ""
    while not Alignment.has_value(alignmentinput):
        alignmentinput = input("Alignment (eg. Chaotic Good, Lawful Neutral, etc.)\n").strip().upper()
        if alignmentinput:
            return alignmentinput
        else:
            return 'unaligned'


def print_skill_choices(monster=None):
    if monster is None:
        for i, x in enumerate(SKILL_LIST):
            print(f'| {str(i)} - {x} |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(SKILL_LIST):
            isprof = "*" if monster.skills[x] else ""
            print(f"| {str(i)} - {x}{isprof} |")
        print('| (e)xit |')


def print_damage_types(monster=None):
    if monster is None:
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


def print_condition_immunities(monster=None):
    if monster is None:
        for i, x in enumerate(CONDITION_LIST):
            print('| ' + str(i) + ' - ' + x + ' |')
        print('| (e)xit |')
    else:
        for i, x in enumerate(CONDITION_LIST):
            isprof = "*" if monster.conditionimmunities[x] else ""
            print(f"| {str(i)} - {x}{isprof}|")
        print('| (e)xit |')


def get_hit_dice(hitdie, con):
    hitdiceprompt = ""
    while hitdiceprompt != 'a' or hitdiceprompt != 'auto' \
            or not hitdiceprompt.isdigit():
        hitdiceprompt = input("Calculate hit dice and hit points.\n"
                              "Choose below where you would like to calculate "
                              "hit dice from hit points ('auto' or 'a')\n"
                              "or just the input hit dice number and derive "
                              "hit points\n")
        if hitdiceprompt == 'auto' or hitdiceprompt == 'a':
            hitpointsinput = ""
            while not hitpointsinput.isdigit():
                hitpointsinput = input("Enter hit point total\n"
                                       "Note: because of how hit dice "
                                       "correspond to hit points, choosing "
                                       "'auto' may result in a \n"
                                       "hit point total slightly different "
                                       "from your chosen number\n")
                if hitpointsinput.isdigit():
                    hitpointsinput = int(hitpointsinput)
                    hitdice = calculate_hitdice(hitdie=hitdie,
                                                con=con,
                                                hitpoints=hitpointsinput)
                    print(f"Creature has {str(hitdice)}d{hitdie} hitdice")
                    return hitdice
                else:
                    print("Invalid hitpoint total, expected "
                          "an integer greater than 0")
        elif hitdiceprompt.isdigit():
            hitdice = int(hitdiceprompt)
            if hitdice > 0:
                return hitdice
            else:
                print("Invalid hitdice total, expected "
                      "an integer greater than 0")
        else:
            print("Invalid input, expected 'a', 'auto', "
                  "or an integer greater than 0 for manual hitdice input")


def calculate_hitdice(hitdie, con, hitpoints):
    halfdie = hitdie/2
    hdtotal = 1
    temphp = halfdie + con
    while math.floor(temphp) < hitpoints:
        hdtotal += 1
        temphp += (halfdie + con)
    return hdtotal


def calculate_hitpoints(hitdie, con, hitdice):
    halfdie = hitdie/2
    temphp = 0
    for i in range(hitdice):
        temphp += (halfdie+con)
    return math.floor(temphp)


def get_ability_score(score):
    scoreinput = ""
    while not scoreinput.isdigit():
        scoreinput = input(f"Monster {score} Score (not the modifier)\n")
        if scoreinput.isdigit() and int(scoreinput) >= 0:
            return int(scoreinput)
        elif scoreinput == "":
            return 10
        else:
            print("Invalid " + score + "Score. Must be an integer greater "
                                       "than or equal to 0")


def save_prof_wizard(monster):
    print('Entering saving throw wizard. Default response for options is no')
    strprof = input("Is the creature proficient in "
                    "Strength saves, (y)es or (n)o\n")
    if strprof == 'y' or strprof == 'yes':
        monster.strsave = True
    dexprof = input("Is the creature proficient in "
                    "Dexterity saves, (y)es or (n)o\n")
    if dexprof == 'y' or dexprof == 'yes':
        monster.dexsave = True
    conprof = input("Is the creature proficient in "
                    "Constitution saves, (y)es or (n)o\n")
    if conprof == 'y' or conprof == 'yes':
        monster.consave = True
    intprof = input("Is the creature proficient in "
                    "Intelligence saves, (y)es or (n)o\n")
    if intprof == 'y' or intprof == 'yes':
        monster.intsave = True
    wisprof = input("Is the creature proficient in "
                    "Wisdom saves, (y)es or (n)o\n")
    if wisprof == 'y' or wisprof == 'yes':
        monster.wissave = True
    chaprof = input("Is the creature proficient in "
                    "Charisma saves, (y)es or (n)o\n")
    if chaprof == 'y' or chaprof == 'yes':
        monster.chasave = True
    return monster


def toggle_skill(monster, skill):
    monster.skills[skill] = not monster.skills[skill]


def toggle_damage(monster, damage, damagemodifier=None):
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


def toggle_condition(monster, condition):
    monster.conditionimmunities[condition] = \
        not monster.conditionimmunities[condition]


def skill_prof_wizard(monster, initialize=True):
    print("Entering skill proficiency wizard. "
          "Default response for options is no")
    if initialize:
        for skill in SKILL_LIST:
            monster.skills[skill] = False

    skillprompt = 'WIZARD'
    while skillprompt != '' and skillprompt != 'exit':
        print("Enter the digit corresponding to the skill proficiency "
              "you would like to add to the creature.\n"
              "If the creature is already proficient with the chosen skill, "
              "that proficiency will be removed.\n"
              "Skills the creature is already "
              "proficient in are marked with a *"
              "Enter 'exit' or just hit return to exit the skill wizard\n")
        print_skill_choices(monster)
        skillprompt = input()
        if skillprompt.isdigit():
            skillchoice = int(skillprompt)
            if 0 <= skillchoice < len(SKILL_LIST):
                toggle_skill(monster, SKILL_LIST[skillchoice])
            else:
                print(f'Invalid index. Expected integer '
                      f'between 0 and {len(SKILL_LIST)}')
                continue
        elif skillprompt == "" or skillprompt == "e" or skillprompt == "exit":
            break
        else:
            print(f'Invalid input. Expected integer '
                  f'between 0 and {len(SKILL_LIST)}')
    return monster


def damage_type_wizard(monster, mode=None, initialize=True):
    print(f"Entering damage {mode} wizard. Default response for options is no")
    damageprompt = 'WIZARD'
    if initialize:
        for damage in DAMAGE_LIST:
            monster.damageresistances[damage] = False
            monster.damageimmunities[damage] = False
            monster.damagevulnerabilities[damage] = False

    while damageprompt != '' and damageprompt != 'exit':
        print(f"Enter the digit corresponding to the damage {mode} you would "
              f"like to add to the creature.\n If the creature is already "
              f"proficient with the chosen skill, that proficiency will be "
              f"removed.\n Skills the creature is already proficient in are "
              f"marked with a * Enter 'exit' or just hit return to exit the "
              f"skill wizard\n")

        print_damage_types(monster)
        damage_prompt = input()
        if damage_prompt.isdigit():
            damage_choice = int(damage_prompt)
            if 0 <= damage_choice < len(DAMAGE_LIST):
                toggle_damage(monster, DAMAGE_LIST[damage_choice], mode)
            else:
                print(f'Invalid index. Expected integer '
                      f'between 0 and {len(DAMAGE_LIST)}')
        elif damage_prompt == "" or damage_prompt == "e" \
                or damage_prompt == "exit":
            break
        else:
            print(f'Invalid input. Expected integer '
                  f'between 0 and {len(DAMAGE_LIST)}')
    return monster


def condition_immunity_wizard(monster, initialize=True):
    print(f"Entering condition immunity wizard. "
          f"Default response for options is no")
    conditionprompt = 'WIZARD'
    if initialize:
        for condition in CONDITION_LIST:
            monster.conditionimmunities[condition] = False

    while conditionprompt != '' and conditionprompt != 'exit':
        print(f"Enter the digit corresponding to the condition immunity "
              f"you would like to add to the creature.\n If the creature is "
              f"already immune to the chosen condition, that immunity will be "
              f"removed.\n Conditions the creature is already immune to are "
              f"marked with a * Enter 'exit' or just hit return to exit the "
              f"skill wizard\n")

        print_condition_immunities(monster)
        condition_prompt = input()
        if condition_prompt.isdigit():
            condition_prompt = int(condition_prompt)
            if 0 <= condition_prompt < len(DAMAGE_LIST):
                toggle_condition(monster, CONDITION_LIST[condition_prompt])
            else:
                print(
                    f'Invalid index. Expected integer '
                    f'between 0 and {len(CONDITION_LIST)}')
        elif condition_prompt == "" or condition_prompt == "e" \
                or condition_prompt == "exit":
            break
        else:
            print(
                f'Invalid input. Expected integer '
                f'between 0 and {len(CONDITION_LIST)}')
    return monster

def get_challenge_rating():
    crinput = ""
    while not crinput.isdigit():
        crinput = input(f"Monster Challenge Rating (Default 0)\n")
        if crinput.isdigit() and int(crinput) >= 0:
            return int(crinput)
        elif crinput == "":
            return 0
        else:
            print("Invalid Challenge Rating. Must be an integer greater "
                                             "than or equal to 0")


def ability_wizard():
    ability_list = []
    ability_prompt = ''
    while ability_prompt != 'e' and ability_prompt != 'exit':
        print("Add abilities to the creature. Any input other than (e)xit "
              "will be treated as the name of the ability, after which you "
              "will be able to add a description to it.\n")
        ability_prompt = input()
        if ability_prompt != 'e' and ability_prompt != 'exit':
            newability = AbilityDescription(name=ability_prompt)
            description = input(f"Enter description for {newability}\n")
            newability.description = description
            ability_list.append(newability)

    return ability_list


def action_wizard():

    action_list = []
    action_prompt = ''
    while action_prompt != 'e' and action_prompt != 'exit':
        print("Add attacks or actions for the creature. Any input other than "
              "(e)xit will be treated as the name of the ability, after which "
              "you will be able to add a additional information about it, "
              "like damage or range\n")

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
                    AbilityDescription(name=action_name,
                                       description=description))
                continue

            attack_mod, attack_bonus = get_attack_bonus()
            damage_dice = get_damage_dice()
            description = input("Input a description for the attack. Most "
                                "attacks do not have a description, this is "
                                "only used for attacks that have additional "
                                "effects like a Marilith's trail grapple.\n")

            if actiontype_prompt == '2':
                action_list.append(
                    ranged_weapon_attack_wizard(name=action_name,
                                                attack_mod=attack_mod,
                                                attack_bonus=attack_bonus,
                                                damage_dice=damage_dice,
                                                description=description))
            elif actiontype_prompt == '3':
                action_list.append(
                    melee_spell_attack_wizard(name=action_name,
                                              attack_mod=attack_mod,
                                              attack_bonus=attack_bonus,
                                              damage_dice=damage_dice,
                                              description=description))
            elif actiontype_prompt == '4':
                action_list.append(
                    ranged_spell_attack_wizard(name=action_name,
                                               attack_mod=attack_mod,
                                               attack_bonus=attack_bonus,
                                               damage_dice=damage_dice,
                                               description=description))
            else:
                action_list.append(
                    melee_weapon_attack_wizard(name=action_name,
                                               attack_mod=attack_mod,
                                               attack_bonus=attack_bonus,
                                               damage_dice=damage_dice,
                                               description=description))
    print("Exiting attack setup")
    return action_list


def get_attack_bonus():
    attackmod = None
    while attackmod is None:
        print("What ability is the attack made with?")
        AbilityScores.menu()
        mod_prompt = input("\n")
        if mod_prompt.isdigit() and 0 <= int(mod_prompt) < len(
                AbilityScores):
            attackmod = int(mod_prompt)
            continue
        else:
            print(f"Invalid input. Expected an integer between 0 "
                  f"and {len(AbilityScores)}")

    attackbonus = None
    while attackbonus is None:
        bonus_prompt = input("What is the attack's to hit bonus. Do not add a "
                             "+ next to the integer bonus. Negative bonuses "
                             "are accepted. Default value is 0\n Note: The "
                             "base attack bonus of the attack is the "
                             "proficiency bonus of the creature plus the "
                             "ability mod for the attack. This bonus should "
                             "only be used for other modifiers like a +1 "
                             "weapon.\n")

        if bonus_prompt.isdigit():
            attackbonus = int(bonus_prompt)
        elif bonus_prompt == "":
            attackbonus = 0
        else:
            print("Invalid input. Expected an integer")

    return attackmod, attackbonus


def get_damage_dice():
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
            damagepair = {"dicestring": damage_prompt}
            print("What is the damage type?")
            print_damage_types()
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


def valid_distance(distance, default):
    if distance.isdigit():
        if int(distance) % 5 == 0:
            return int(distance)
        else:
            raise ValueError("Valid distances must be a multiple of 5")
    elif distance == "":
        return default
    else:
        raise TypeError("Distances must be a number or an "
                        "empty string for a default value")


def get_distance(prompt, default):
    reach = None
    while reach is None:
        try:
            reach_input = input(prompt +
                                f"Must be an integer multiple of 5. "
                                f"Default {default}\n")
            reach = valid_distance(reach_input, default)
        except (ValueError, TypeError) as e:
            print(e.args[0])

    return reach


def melee_weapon_attack_wizard(name, attack_mod, attack_bonus,
                               damage_dice, description):
    attack = MeleeWeaponAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    attack.reach = get_distance("What is the range for the "
                                "melee weapon attack\n", 5)
    return attack


def ranged_weapon_attack_wizard(name, attack_mod, attack_bonus,
                                damage_dice, description):
    attack = RangedWeaponAttack(name=name,
                                attack_mod=attack_mod,
                                attack_bonus=attack_bonus,
                                damage_dice=damage_dice,
                                description=description)

    attack.short_range = get_distance("What is the short range "
                                      "for the ranged attack.", 20)

    attack.long_range = get_distance("What is the long range "
                                     "for the ranged attack.", 60)

    return attack


def melee_spell_attack_wizard(name, attack_mod, attack_bonus,
                              damage_dice, description):

    attack = MeleeSpellAttack(name=name,
                              attack_mod=attack_mod,
                              attack_bonus=attack_bonus,
                              damage_dice=damage_dice,
                              description=description)

    attack.reach = get_distance("What is the range "
                                "for the melee spell attack\n", 5)

    return attack


def ranged_spell_attack_wizard(name, attack_mod, attack_bonus,
                               damage_dice, description):
    attack = RangedSpellAttack(name=name,
                               attack_mod=attack_mod,
                               attack_bonus=attack_bonus,
                               damage_dice=damage_dice,
                               description=description)

    attack.reach = get_distance("What is the range "
                                "for the ranged spell attack\n", 30)

    return attack


def bonus_action_wizard():
    reaction_list = []
    reaction_prompt = ''
    while reaction_prompt != 'e' and reaction_prompt != 'exit':
        reaction_prompt = input("Add bonus actions for the creature. "
                                "Any input other than (e)xit "
                                "will be treated as the name of "
                                "the reaction\n")
        if reaction_prompt != 'e' and reaction_prompt != 'exit':
            description = input("Description for the action.\n")
            reaction_list.append(
                AbilityDescription(name=reaction_prompt,
                                   description=description))
    return reaction_list

def reaction_wizard():
    reaction_list = []
    reaction_prompt = ''
    while reaction_prompt != 'e' and reaction_prompt != 'exit':
        reaction_prompt = input("Add reactions for the creature. "
                                "Any input other than (e)xit "
                                "will be treated as the name of "
                                "the reaction\n")
        if reaction_prompt != 'e' and reaction_prompt != 'exit':
            description = input("Description for the action.\n")
            reaction_list.append(
                AbilityDescription(name=reaction_prompt,
                                   description=description))
    return reaction_list


def legendary_action_wizard():
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
                legendaryaction = AbilityDescription(name=legendary_prompt)
                description = input(f"Enter description "
                                    f"for {legendaryaction}\n")
                legendaryaction.description = description
                legendary_action_list.append(legendaryaction)

    return legendary_action_list


def mythic_action_wizard():
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
                mythicaction = AbilityDescription(name=mythic_prompt)
                description = input(f"Enter description for {mythicaction}\n")
                mythicaction.description = description
                mythic_action_list.append(mythicaction)

    return mythic_description, mythic_action_list


def interactive_monster_gen():
    monster = MonsterBlock()
    print("Welcome to the interactive 5e creature generator\n"
          "All of the following fields are optional, "
          "just hit return to skip one\n")

    # Get creature name
    nameinput = input("Creature Name\n")
    monster.name = "PLACEHOLDER" if nameinput == "" else nameinput

    # Get creature size
    monster.size = size_wizard()

    # Get creature alignment
    monster.alignment = alignment_wizard()

    # Get creature type
    creaturetype = input("Monster Type (eg. celestial, humanoid(demi-human), "
                         "etc\n").strip().upper()
    monster.type = creaturetype

    # Get AC bonus
    acbonusinput = "NOTADIGIT"
    while not acbonusinput.isdigit():
        acbonusinput = input("Monster AC Bonus (eg. armor bonus) "
                             "disgregading dex bonuses\n")

        if acbonusinput.isdigit():
            monster.acbonus = int(acbonusinput)
            break
        elif acbonusinput == "":
            monster.acbonus = 0
            break
        else:
            print("Invalid AC bonus. Must be an integer "
                  "greater than or equal to 0\n")

    # Get AC Bonus description
    monster.acdesc = input("AC Bonus description (eg. plate, "
                           "natural armor, mage armor, etc.\n")

    # Get Ability Scores
    monster.ability_scores[AbilityScores.STRENGTH] = \
        get_ability_score("Strength")
    monster.ability_scores[AbilityScores.DEXTERITY] = \
        get_ability_score("Dexterity")
    monster.ability_scores[AbilityScores.CONSTITUTION] = \
        get_ability_score("Constitution")
    monster.ability_scores[AbilityScores.INTELLIGENCE] = \
        get_ability_score("Intelligence")
    monster.ability_scores[AbilityScores.WISDOM] = \
        get_ability_score("Wisdom")
    monster.ability_scores[AbilityScores.CHARISMA] = \
        get_ability_score("Charisma")

    # Get hit dice through the hp wizard
    monster.hitdice = get_hit_dice(hitdie=Size.hitdice(monster.size),
                                   con=monster.constitution)
    monster.hitpoints = calculate_hitpoints(hitdie=Size.hitdice(monster.size),
                                            con=monster.constitution,
                                            hitdice=monster.hitdice)

    # Get speed
    speedinput = input("Monster Speed (default 30 ft.)\n")
    monster.speed = "30 ft." if speedinput == "" else speedinput

    # Get save proficients
    saveprompt = input("Does the creature have any saving throw "
                       "proficiencies: (y)es or (n)o? Default no\n")
    if saveprompt == 'y' or saveprompt == 'yes':
        monster = save_prof_wizard(monster)

    # Get skill proficiencies
    skillprompt = input("Does the creature have any skill "
                        "proficiencies: (y)es or (n)o? Default no\n")
    if skillprompt == 'y' or skillprompt == 'yes':
        monster = skill_prof_wizard(monster)

    # Get damage vulnerabilities
    vulnerabilityprompt = input("Does the creature have any damage "
                                "vulnerabilities: (y)es or (n)o? Default no\n")
    if vulnerabilityprompt == 'y' or vulnerabilityprompt == 'yes':
        monster = damage_type_wizard(monster, MonsterBlock.VULNERABILITY,
                                     initialize=True)

    # Get damage resistances
    resistanceprompt = input(
        "Does the creature have any damage resistances:"
        " (y)es or (n)o? Default no\n")
    if resistanceprompt == 'y' or resistanceprompt == 'yes':
        monster = damage_type_wizard(monster, MonsterBlock.RESISTANCE,
                                     initialize=True)

    # Get damage resistances
    immunityprompt = input(
        "Does the creature have any damage immunities: "
        "(y)es or (n)o? Default no\n")
    if immunityprompt == 'y' or immunityprompt == 'yes':
        monster = damage_type_wizard(monster, MonsterBlock.IMMUNITY,
                                     initialize=True)

    conditionprompt = input("Does the creature have any condition "
                            "immunities: (y)es or (n)o? Default no\n")
    if conditionprompt == 'y' or conditionprompt == 'yes':
        monster = condition_immunity_wizard(monster)

    # Get senses
    monster.senses = input("Monster Senses (eg. darkvision "
                       "60 ft., blindsight 10 ft.\n")

    # Get languages
    monster.languages = input("Monster languages (eg. Common, "
                          "Draconic, understands Gnomish\n")

    monster.challengerating = get_challenge_rating()

    monster.abilities = ability_wizard()
    monster.actions = action_wizard()
    monster.bonusactions = bonus_action_wizard()
    monster.reactions = reaction_wizard()
    monster.legendaryactions = legendary_action_wizard()
    monster.mythicdescription, monster.mythicactions = mythic_action_wizard()

    return monster

def generate_test_monster():
    return MonsterBlock(
        name="TEST MONSTER",
        size=Size.MEDIUM,
        alignment='chaotic evil',
        acdesc="natural armor",
        acbonus=2,
        ability_scores={
            AbilityScores.STRENGTH: 12,
            AbilityScores.DEXTERITY: 11,
            AbilityScores.CONSTITUTION: 16,
            AbilityScores.INTELLIGENCE: 19,
            AbilityScores.WISDOM: 20,
            AbilityScores.CHARISMA: 10
        },
        hitdice='7d8',
        hitpoints=100,
        speed='30 ft.',
        strsave=True,
        dexsave=False,
        consave=True,
        intsave=False,
        wissave=True,
        chasave=False,
        skills={"Perception": True, "Stealth": True},
        damageimmunities={"fire": True, "cold": True},
        damageresistances={"psychic": True, "lightning": True},
        damagevulnerabilities={"radiant": True, "necrotic": True},
        conditionimmunities={"bleed": True, "stunned": True},
        senses="darkvision 30 ft.",
        languages="Common, Draconic",
        challengerating=15,
        abilities=[AbilityDescription(name="Legendary Resistance (1/Long Rest)",
                                      description="This is a test ability")],
        actions=[MeleeWeaponAttack(name="PLACEHOLDER ATTACK",
                                   attack_mod=AbilityScores.STRENGTH,
                                   attack_bonus=1,
                                   description="Attack description here.",
                                   damage_dice=[{"dicestring": "1d4+2d6+8",
                                                 "damagetype": "cold"}],
                                   reach=5)],
        reactions=[AbilityDescription(name="Parry",
                                      description="This is a test reaction")],
        legendaryactions=[AbilityDescription(name="Move",
                                             description="This is a test legendary action"),
                          AbilityDescription(name="Attack",
                                             description="This is another test legendary action")],
        mythicdescription="Test mythic description",
        mythicactions=[AbilityDescription(name="Mythic Move",
                                          description="This is a test mythic action"),
                       AbilityDescription(name="Mythic Swipe",
                                          description="This is another test mythic action")]
    )

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
