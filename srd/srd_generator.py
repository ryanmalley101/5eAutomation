from srd.srd_datastructs import *


def generate_test_melee_attack():
    return MeleeWeaponAttack(name="Test Melee Attack",
                             type=BaseAttack.AttackType.MELEEWEAPON,
                             attack_mod=AbilityScore.STRENGTH,
                             attack_bonus=1,
                             description="This is a test description",
                             targets="two creatures.",
                             reach=5,
                             damage_dice=[{"dicestring": "1d4+2d6+8", "damagetype": DamageType.COLD},
                                          {"dicestring": "1d6+M", "damagetype": DamageType.FIRE}])
