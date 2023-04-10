# This is a sample Python script.

from creatures.creature_datastructs import *
from srd.srd_datastructs import *


def generate_test_monster():
    return MonsterStatblock(
        name="TEST CREATURE",
        size=Size.MEDIUM,
        type="Tester",
        alignment='chaotic evil',
        acdesc="natural armor",
        acbonus=2,
        ability_scores={
            AbilityScore.STRENGTH: 12,
            AbilityScore.DEXTERITY: 11,
            AbilityScore.CONSTITUTION: 16,
            AbilityScore.INTELLIGENCE: 19,
            AbilityScore.WISDOM: 20,
            AbilityScore.CHARISMA: 10
        },
        hitdice=7,
        hitpoints=100,
        speed='30 ft.',
        saving_throws={AbilityScore.STRENGTH, AbilityScore.CONSTITUTION, AbilityScore.WISDOM},
        skills={Skill.PERCEPTION, Skill.STEALTH},
        expertise={Skill.ATHLETICS, Skill.PERFORMANCE},
        damage_immunities={DamageType.FIRE, DamageType.FORCE},
        damage_resistances={DamageType.COLD, DamageType.ACID},
        damage_vulnerabilities={DamageType.RADIANT, DamageType.NECROTIC},
        condition_immunities={Condition.CHARMED, Condition.FRIGHTENED},
        senses="darkvision 30 ft.",
        languages="Common, Draconic",
        challengerating=15,
        abilities=[AbilityDescription(name="Legendary Resistance (1/Long Rest)",
                                      description="This is a test ability")],
        actions=[MeleeWeaponAttack(name="PLACEHOLDER ATTACK",
                                   attack_mod=AbilityScore.STRENGTH,
                                   attack_bonus=1,
                                   description="Attack description here.",
                                   damage_dice=[{"dicestring": "1d4+2d6+8",
                                                 "damagetype": "cold"}],
                                   reach=5)],
        reactions=[AbilityDescription(name="Parry",
                                      description="This is a test reaction")],
        bonusactions=[AbilityDescription(name="Misty Step",
                                         description="Teleport 30 feet.")],
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
