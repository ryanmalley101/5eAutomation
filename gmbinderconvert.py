from statblockdatastructs import *
from patterns import DICESTRINGPATTERN
import re

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


def print_monster_ability_scores(monster: MonsterBlock):
    strscore = monster.ability_scores['Strength']
    dexscore = monster.ability_scores['Dexterity']
    conscore = monster.ability_scores['Constitution']
    intscore = monster.ability_scores['Intelligence']
    wisscore = monster.ability_scores['Wisdom']
    chascore = monster.ability_scores['Charisma']

    abilitystring = f"|{strscore} ({score_to_mod(strscore)})"
    abilitystring += f"|{dexscore} ({score_to_mod(dexscore)})"
    abilitystring += f"|{conscore} ({score_to_mod(conscore)})"
    abilitystring += f"|{intscore} ({score_to_mod(intscore)})"
    abilitystring += f"|{wisscore} ({score_to_mod(wisscore)})"
    abilitystring += f"|{chascore} ({score_to_mod(chascore)})|\n"
    return abilitystring


def print_monster_ability(ability: AbilityDescription):
    ability_string =  f"> ***{ability.name}*** {ability.description}\n"
    ability_string += f"> \n"


def print_monster_actions(monster):
    action_string = ""
    for action in monster.actions:
        if isinstance(action, AbilityDescription):
            action_string += print_monster_ability(action)
        elif isinstance(action, BaseAttack):
            # The modifier of the ability score associated with the attack
            attack_ability_mod = score_to_mod(
                monster.ability_scores[action.attack_mod])
            action_string = ""
            if isinstance(action, MeleeWeaponAttack):
                action_string += f"> ***{action.name}*** *Melee Weapon Attack* +{monster.get_attack_bonus(action)} to hit, reach {action.reach} ft., {action.targets}. Hit: "

                # The dice counter variable keeps track of the number of damage dice
                # We need this to add a 'plus' at the end of the intermediate damage
                dicecounter = len(action.damage_dice) - 1
                for damagepair in action.damage_dice:
                    action_string += f"{BaseAttack.calculate_dicestring_damage(damagepair['dicestring'], attack_ability_mod)} ({damagepair['dicestring'].replace('M', attack_ability_mod)}) {damagepair['damagetype']} damage"
                    if dicecounter > 0:
                        dicecounter -= 1
                        action_string += ' plus '

                action_string += action.description
                action_string += '.\n'
        else:
            raise TypeError("Tried to add a non-ability, "
                            "non-action as an action")

    return action_string


def print_monster_saves(monster):
    save_string = ""
    if monster.strsave or monster.dexsave or monster.consave \
        or monster.intsave or monster.wissave or monster.chasave:
        save_string = "> - **Saving Throws** "
        if monster.strsave:
            save_string += f"STR +{monster.calc_save('Strength')}"
        if monster.dexsave:
            save_string += f"DEX +{monster.calc_save('Dexterity')}"
        if monster.strsave:
            save_string += f"CON +{monster.calc_save('Constitution')}"
        if monster.strsave:
            save_string += f"INT +{monster.calc_save('Intelligence')}"
        if monster.strsave:
            save_string += f"WIS +{monster.calc_save('Wisdom')}"
        if monster.strsave:
            save_string += f"CHA +{monster.calc_save('Charisma')}"
        save_string += '\n'
    return save_string


def print_monster_skills(monster):
    save_string = ""
    if any(monster.skills) is True:
        save_string = "> - **Skills** "

        # Counter for the number of skills so a comma can be added between
        # intermediate values
        counter = len(monster.skills) - 1
        for skill in monster.skills:
            if monster.skills[skill]:
                save_string += f'{skill} +{monster.skill_bonus(skill)}'
            if counter > 0:
                counter -= 1
                save_string += ', '
        save_string += "\n"

    return save_string

def print_monster_vulnerabilities(monster):
    save_string = ""
    if any(monster.skills) is True:
        save_string = "> - **Skills** "

        # Counter for the number of skills so a comma can be added between
        # intermediate values
        counter = len(monster.skills) - 1
        for skill in monster.skills:
            if monster.skills[skill]:
                save_string += f'{skill} +{monster.skill_bonus(skill)}'
            if counter > 0:
                counter -= 1
                save_string += ', '
        save_string += "\n"

    return save_string

def convert_monster(monster: MonsterBlock):
    monster_markup  =  "# ___\n"
    monster_markup += f"# > ## {monster.name}\n"
    monster_markup += f"# >*{monster.size}, {monster.alignment}\n"
    monster_markup += f"> ___\n"
    monster_markup += f"> - **Armor Class** {monster.get_total_ac()}\n"
    monster_markup += f"> - **Hit Points** {monster.hitpoints}\n"
    monster_markup += f"> - **Speed** {monster.speed}\n"
    monster_markup += f">___\n"
    monster_markup += f">|STR|DEX|CON|INT|WIS|CHA|\n"
    monster_markup += f">|:---:|:---:|:---:|:---:|:---:|:---:|\n"
    monster_markup += print_monster_ability_scores(monster)
    monster_markup += f"> ___\n"
    monster_markup += f"> \n"
    monster_markup += print_monster_saves(monster)
    monster_markup += print_monster_skills(monster)
    monster_markup += print_monster_vulnerabilities(monster)
    monster_markup += print_monster_resistances(monster)
    monster_markup += print_monster_immunities(monster)
    monster_markup += print_monster_condition_immunities(monster)
    monster_markup += print_monster_senses(monster)
    monster_markup += f"> - **Languages** {monster.languages}\n"
    monster_markup += f"> - **Challenge Rating** {monster.challengerating} ({CR_TO_XP_TABLE[monster.challengerating]})\n"
    for ability in monster.abilities:
        monster_markup += print_monster_ability(ability)
    monster_markup += f"> ### Actions\n"
    monster_markup += f"> \n"
    monster_markup += print_monster_actions(monster)
    if len(monster.reactions) > 0:
        monster_markup += f"> ### Reactions\n"
        for reaction in monster.reactions:
            monster_markup += print_monster_ability(reaction)
    if len(monster.legendaryactions) > 0:
        monster_markup += f"> ### Legendary Actions\n"
        monster_markup += f"> {monster.name} can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature’s turn. {monster.name} regains spent legendary actions at the start of its turn."
        for legendaryaction in monster.legendaryactions:
            monster_markup += print_monster_ability(legendaryaction)
    if len(monster.mythicactions) > 0:
        monster_markup += f"> ### Mythic Actions\n"
        monster_markup += f"> {monster.mythicdescription}"
        for mythicaction in monster.mythicactions:
            monster_markup += print_monster_ability(mythicaction)

    return monster_markup
#
# class MonsterBlock:
#     name: str = "PLACEHOLDER"
#     size: Size = Size.CHANGEME
#     alignment: Alignment = Alignment.CHANGEME
#     acdesc: str = ""
#     acbonus: int = 10
#     ability_scores: dict = field(default_factory=dict)
#     strength: int = 10
#     dexterity: int = 10
#     constitution: int = 10
#     intelligence: int = 10
#     wisdom: int = 10
#     charisma: int = 10
#     hitdice: str = '0d0'
#     hitpoints: int = 0
#     speed: str = '30 ft.'
#     strsave: bool = False
#     dexsave: bool = False
#     consave: bool = False
#     intsave: bool = False
#     wissave: bool = False
#     chasave: bool = False
#     skills: dict = field(default_factory=dict)
#     damageimmunities: dict = field(default_factory=dict)
#     damageresistances: dict = field(default_factory=dict)
#     damagevulnerabilities: dict = field(default_factory=dict)
#     conditionimmunities: dict = field(default_factory=dict)
#     senses: str = ""
#     languages: str = ""
#     abilities: list = field(default_factory=list)
#     actions: list = field(default_factory=list)
#     reactions: list = field(default_factory=list)
#     legendaryactions: list = field(default_factory=list)
#     mythicdescription: str = None
#     mythicactions: list = field(default_factory=list)
#
#     VULNERABILITY = "VULNERABILITY"
#     IMMUNITY = "IMMUNITY"
#     RESISTANCE = "RESISTANCE"
#

