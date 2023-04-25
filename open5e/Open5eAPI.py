from srd.srd_datastructs import Size, AbilityScore, Skill, DamageType, Condition, AbilityDescription, BaseAttack, MeleeWeaponAttack, MeleeSpellAttack, RangedWeaponAttack, RangedSpellAttack
from creatures.creature_datastructs import MonsterStatblock
from gmbinderconvert.convert_creature import convert_monster
import requests
import re


def fetch_all_srd_monsters():
    url = "https://api.open5e.com/monsters/?format=json&limit=1000&source=5e%20srd"
    monsters = []

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            monsters.extend(data['results'])
            url = data['next']
        else:
            print("Error fetching monsters from API")
            break
    print(f"Fetched {len(monsters)} monsters from API")
    return monsters


def fetch_srd_monster(monster_name):
    api_url = f'https://api.open5e.com/monsters/{monster_name}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def convertAPIMonster(monster_dict):
    convertedMonster = MonsterStatblock()
    # Get basic information
    convertedMonster.name = monster_dict['name']
    convertedMonster.size = Size[monster_dict['size'].upper()]
    convertedMonster.type = monster_dict['type']
    convertedMonster.alignment = monster_dict['alignment']

    # Get armor class information
    convertedMonster.acdesc = monster_dict['armor_desc']
    convertedMonster.acbonus = int(monster_dict['armor_class'])

    # Get ability scores
    ability_scores = {AbilityScore.STRENGTH: int(monster_dict['strength']),
                      AbilityScore.DEXTERITY: int(monster_dict['dexterity']),
                      AbilityScore.CONSTITUTION: int(monster_dict['constitution']),
                      AbilityScore.INTELLIGENCE: int(monster_dict['intelligence']),
                      AbilityScore.WISDOM: int(monster_dict['wisdom']),
                      AbilityScore.CHARISMA: int(monster_dict['charisma'])}
    convertedMonster.ability_scores = ability_scores

    # Get hit points and hit dice
    convertedMonster.hitdice = int(monster_dict['hit_dice'].split('d')[0])
    convertedMonster.hitpoints = int(monster_dict['hit_points'])

    # Get speed information
    speed_string = ""
    for speed, value in monster_dict['speed'].items():
        if speed == 'walk':
            speed_string += f"{value} ft."
        else:
            speed_string += f", {speed} {value} ft."
    convertedMonster.speed = speed_string

    # Get saving throws
    saving_throws = set()
    if monster_dict['strength_save'] is not None:
        saving_throws.add(AbilityScore.STRENGTH)
    if monster_dict['dexterity_save'] is not None:
        saving_throws.add(AbilityScore.DEXTERITY)
    if monster_dict['constitution_save'] is not None:
        saving_throws.add(AbilityScore.CONSTITUTION)
    if monster_dict['intelligence_save'] is not None:
        saving_throws.add(AbilityScore.INTELLIGENCE)
    if monster_dict['wisdom_save'] is not None:
        saving_throws.add(AbilityScore.WISDOM)
    if monster_dict['charisma_save'] is not None:
        saving_throws.add(AbilityScore.CHARISMA)
    convertedMonster.saving_throws = saving_throws

    # Get skills and expertise
    skills = set()
    expertise = set()
    if 'skills' in monster_dict:
        for skill_string in monster_dict['skills'].keys():
            skill = Skill[skill_string.strip().upper()]
            skills.add(skill)
            # TODO: Implement expertises
            # if monster_dict.get('expertise') and skill_string.strip().lower() in monster_dict['expertise'].split(
            #         ','):
            #     expertise.add(skill)
    convertedMonster.skills = skills
    convertedMonster.expertise = expertise

    # Get damage immunities, resistances, and vulnerabilities
    damage_immunities = set(map(DamageType.__getitem__, monster_dict.get("damage_immunities", [])))
    damage_resistances = set(map(DamageType.__getitem__, monster_dict.get("damage_resistances", [])))
    damage_vulnerabilities = set(map(DamageType.__getitem__, monster_dict.get("damage_vulnerabilities", [])))
    condition_immunities = set(map(Condition.__getitem__, monster_dict.get("condition_immunities", [])))

    convertedMonster.damage_immunities = damage_immunities
    convertedMonster.damage_resistances = damage_resistances
    convertedMonster.damage_vulnerabilities = damage_vulnerabilities
    convertedMonster.condition_immunities = condition_immunities

    convertedMonster.senses = monster_dict.get("senses", "").split("passive")[0].rstrip(', ')
    convertedMonster.languages = monster_dict.get("languages", "")

    convertedMonster.challengerating = int(monster_dict["cr"])

    # Get abilities
    abilities_list = []
    if monster_dict.get("special_abilities"):
        for ability in monster_dict["special_abilities"]:
            abilities_list.append(AbilityDescription(name=ability["name"],
                                                     description=ability["desc"]))
    convertedMonster.abilities = abilities_list

    actions_list = []
    if monster_dict.get("actions"):
        for action in monster_dict["actions"]:
            if len(action):
                actions_list.append(AbilityDescription(name=action["name"],
                                                         description=action["desc"]))
            else:
                attack_type = BaseAttack.AttackType(action.split(':')[0])
                attack_mod = AbilityScore.__getitem__(action["attack_bonus"]["ability"].upper())
                attack_bonus = action["attack_bonus"]
                damage_bonus = action["damage_bonus"]
                attack_mod = 0
                for score, value in ability_scores.items():
                    if value + convertedMonster.proficiency_bonus() == attack_bonus:
                        attack_mod = score

                dice = []
                if action.get("damage"):
                    dice_strings = action["damage_dice"].split("+")
                    damage_type_pattern = r"(\b\w+\b) damage"
                    damage_types = re.findall(damage_type_pattern, action['desc'])
                    for index, (dicestring, damagetype) in enumerate(zip(dice_strings, damage_types)):
                        dice.append({"dicestring": dicestring,
                                     "damagetype": damagetype})
                else:
                    dice = []
                description = action["desc"].split('damage.')[1]


                name = action["name"]
                match attack_type:
                    case BaseAttack.AttackType.MELEEWEAPON:
                        reach = 5
                        reach_pattern = r"(?<=reach\s)\d+(?=\sft\.)"
                        range_match = re.search(reach_pattern, action['desc'])
                        if range_match:
                            reach = int(range_match.group(0))
                        actions_list.append(MeleeWeaponAttack(name=name,
                                                              attack_mod=attack_mod,
                                                              attack_bonus=attack_bonus,
                                                              description=description,
                                                              damage_dice=dice,
                                                              reach=reach))
                    case BaseAttack.AttackType.MELEESPELL:
                        reach = 5
                        reach_pattern = r"(?<=reach\s)\d+(?=\sft\.)"
                        range_match = re.search(reach_pattern, action['desc'])
                        if range_match:
                            reach = int(range_match.group(0))
                        actions_list.append(MeleeSpellAttack(name=name,
                                                              attack_mod=attack_mod,
                                                              attack_bonus=attack_bonus,
                                                              description=description,
                                                              damage_dice=dice,
                                                              reach=reach))
                    case BaseAttack.AttackType.RANGEDWEAPON:
                        short_range = 20
                        long_range = 60
                        range_pattern = r"range\s(\d+)\W(\d+)\sft"
                        range_match = re.search(range_pattern, action['desc'])
                        if range_match:
                            short_range = int(range_match.group(1))
                            short_range = int(range_match.group(2))
                        actions_list.append(RangedWeaponAttack(name=name,
                                                               attack_mod=attack_mod,
                                                               attack_bonus=attack_bonus,
                                                               description=description,
                                                               damage_dice=dice,
                                                               short_range=short_range,
                                                               long_range=long_range))

                    case BaseAttack.AttackType.RANGEDSPELL:
                        spell_range = 30
                        range_pattern = r"(?<=range\s)\d+(?=\sft\.)"
                        range_match = re.search(range_pattern, action['desc'])
                        if range_match:
                            spell_range = int(range_match.group(0))
                        actions_list.append(RangedSpellAttack(name=name,
                                                               attack_mod=attack_mod,
                                                               attack_bonus=attack_bonus,
                                                               description=description,
                                                               damage_dice=dice,
                                                               range=spell_range))

    convertedMonster.actions = actions_list

    # Get reactions
    reactions_list = []
    if monster_dict.get("reactions"):
        for reaction in monster_dict["reactions"]:
            reactions_list.append(AbilityDescription(name=reaction["name"],
                                                     description=reaction["desc"]))
    convertedMonster.abilities = reactions_list

    # Get bonus actions
    bonusactions_list = []
    if monster_dict.get("bonusactions"):
        for bonusaction in monster_dict["bonusactions"]:
            bonusactions_list.append(AbilityDescription(name=bonusaction["name"],
                                                        description=bonusaction["desc"]))
    convertedMonster.bonusactions = bonusactions_list

    # Get legendary actions
    legendaryaction_list = []
    if monster_dict.get("legendary_actions"):
        for legendary_action in monster_dict["legendary_actions"]:
            legendaryaction_list.append(AbilityDescription(name=legendary_action["name"],
                                                           description=legendary_action["desc"]))
    convertedMonster.legendaryactions = legendaryaction_list

    # Get mythic actions
    mythic_description = ""
    if monster_dict.get("mythic_description"):
        mythic_description = monster_dict["mythic_description"]
    mythicaction_list = []
    if monster_dict.get("mythic_actions"):
        for mythic_action in monster_dict["mythic_actions"]:
            mythicaction_list.append(AbilityDescription(name=mythic_action["name"],
                                                        description=mythic_action["desc"]))
    convertedMonster.mythicdescription = mythic_description
    convertedMonster.mythicactions = mythicaction_list

    return convertedMonster

if __name__ == '__main__':
    print(convert_monster((convertAPIMonster(fetch_srd_monster("aboleth")))))
