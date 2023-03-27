from statblockdatastructs import *
from gmbinderconvert import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generated_monster = MonsterBlock(
        name="TEST MONSTER",
        size=Size.MEDIUM,
        alignment=Alignment.CE,
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
    # generated_monster.save_json()
    print(convert_monster(generated_monster))
