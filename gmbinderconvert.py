from statblockdatastructs import *


def print_monster_ability_scores(monster: MonsterBlock):
    strscore = monster.ability_scores[AbilityScores.STRENGTH]
    dexscore = monster.ability_scores[AbilityScores.DEXTERITY]
    conscore = monster.ability_scores[AbilityScores.CONSTITUTION]
    intscore = monster.ability_scores[AbilityScores.INTELLIGENCE]
    wisscore = monster.ability_scores[AbilityScores.WISDOM]
    chascore = monster.ability_scores[AbilityScores.CHARISMA]

    abilitystring = f"|{strscore} ({score_to_mod(strscore)})"
    abilitystring += f"|{dexscore} ({score_to_mod(dexscore)})"
    abilitystring += f"|{conscore} ({score_to_mod(conscore)})"
    abilitystring += f"|{intscore} ({score_to_mod(intscore)})"
    abilitystring += f"|{wisscore} ({score_to_mod(wisscore)})"
    abilitystring += f"|{chascore} ({score_to_mod(chascore)})|\n"
    return abilitystring


def print_monster_ability(ability: AbilityDescription):
    ability_string = f"> ***{ability.name}*** {ability.description}\n"
    ability_string += f"> \n"
    return ability_string


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
                action_string += f"> ***{action.name}*** *Melee Weapon Attack* +{monster.get_attack_bonus(action)}" \
                                 f" to hit, reach {action.reach} ft., {action.targets}. Hit: "

                # The dice counter variable keeps track of the number of damage dice
                # We need this to add a 'plus' at the end of the intermediate damage
                dicecounter = len(action.damage_dice) - 1
                for damagepair in action.damage_dice:
                    action_string += f"{BaseAttack.calculate_dicestring_damage(damagepair['dicestring'], attack_ability_mod)} ({damagepair['dicestring'].replace('M', str(attack_ability_mod))}) {damagepair['damagetype']} damage"
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
            save_string += f"STR +{monster.save_bonus(AbilityScores.STRENGTH)}, "
        if monster.dexsave:
            save_string += f"DEX +{monster.save_bonus(AbilityScores.DEXTERITY)}, "
        if monster.strsave:
            save_string += f"CON +{monster.save_bonus(AbilityScores.CONSTITUTION)}, "
        if monster.strsave:
            save_string += f"INT +{monster.save_bonus(AbilityScores.INTELLIGENCE)}, "
        if monster.strsave:
            save_string += f"WIS +{monster.save_bonus(AbilityScores.WISDOM)}, "
        if monster.strsave:
            save_string += f"CHA +{monster.save_bonus(AbilityScores.CHARISMA)} "
        save_string += '\n'
    return save_string


def print_monster_skills(monster):
    skill_string = ""
    if any(monster.skills) is True:
        skill_string = "> - **Skills** "

        # Counter for the number of skills so a comma can be added between
        # intermediate values
        counter = len(monster.skills) - 1
        for skill in monster.skills:
            if monster.skills[skill]:
                skill_string += f'{skill} +{monster.skill_bonus(skill)}'
            if counter > 0:
                counter -= 1
                skill_string += ', '
        skill_string += "\n"

    return skill_string


def print_monster_vulnerabilities(monster):
    vulnerability_string = ""
    if any(monster.damagevulnerabilities) is True:
        vulnerability_string = "> - **Damage Vulnerabilities** "
        # Counter for the number of vulnerabilities so a comma can be added between
        # intermediate values
        counter = len(monster.damagevulnerabilities) - 1
        for vulnerability in monster.damagevulnerabilities:
            if monster.damagevulnerabilities[vulnerability]:
                vulnerability_string += f'{vulnerability}'
            if counter > 0:
                counter -= 1
                vulnerability_string += ', '
        vulnerability_string += "\n"

    return vulnerability_string


def print_monster_resistances(monster):
    resistance_string = ""
    if any(monster.damageresistances) is True:
        resistance_string = "> - **Damage Resistances** "
        # Counter for the number of vulnerabilities so a comma can be added between
        # intermediate values
        counter = len(monster.damageresistances) - 1
        for resistance in monster.damageresistances:
            if monster.damageresistances[resistance]:
                resistance_string += f'{resistance}'
            if counter > 0:
                counter -= 1
                resistance_string += ', '
        resistance_string += "\n"

    return resistance_string


def print_monster_immunities(monster):
    immunity_string = ""
    if any(monster.damageimmunities) is True:
        immunity_string = "> - **Damage Immunities** "
        # Counter for the number of vulnerabilities so a comma can be added between
        # intermediate values
        counter = len(monster.damageimmunities) - 1
        for immunity in monster.damageimmunities:
            if monster.damageimmunities[immunity]:
                immunity_string += f'{immunity}'
            if counter > 0:
                counter -= 1
                immunity_string += ', '
        immunity_string += "\n"

    return immunity_string

def print_monster_condition_immunities(monster):
    condition_string = ""
    if any(monster.conditionimmunities) is True:
        condition_string = "> - **Condition Immunities** "
        # Counter for the number of vulnerabilities so a comma can be added between
        # intermediate values
        counter = len(monster.conditionimmunities) - 1
        for condition in monster.conditionimmunities:
            if monster.conditionimmunities[condition]:
                condition_string += f'{condition}'
            if counter > 0:
                counter -= 1
                condition_string += ', '
        condition_string += "\n"

    return condition_string


def print_monster_senses(monster):
    senses_string = f"> - **Senses** "
    if monster.senses != "":
        senses_string += f"{monster.senses}, "

    senses_string += f'Passive Perception {monster.passive_perception()}\n'
    return senses_string


def convert_monster(monster: MonsterBlock):
    monster_markup  =  "# ___\n"
    monster_markup += f"# > ## {monster.name}\n"
    monster_markup += f"# >* {monster.size.value}, {monster.alignment}\n"
    monster_markup += f"> ___\n"
    monster_markup += f"> - **Armor Class** {monster.get_total_ac()} ({monster.acdesc})\n"
    monster_markup += f"> - **Hit Points** {monster.hitpoints} ({monster.hitdice})\n"
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
    if len(monster.bonusactions) > 0:
        monster_markup += f"> ### Bonus Actions\n"
        for bonus_action in monster.reactions:
            monster_markup += print_monster_ability(bonus_action)
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
        monster_markup += f"> {monster.mythicdescription}\n"
        for mythicaction in monster.mythicactions:
            monster_markup += print_monster_ability(mythicaction)

    return monster_markup

