from spells.spells_datastructs import *


def convert_spell(spell:SpellDescription):
    def ordinal(n: int):
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        return str(n) + suffix

    spell_level_description = f"{ordinal(spell.level)}-level {spell.school.value}" if spell.level > 0 \
        else f"{spell.school.value} cantrip"

    spell_markup =  f"#### {spell.name}\n"
    spell_markup += f"*{spell_level_description}*\n"
    spell_markup += f"___\n"
    spell_markup += f"- **Casting Time:** {spell.casting_time}\n"
    spell_markup += f"- **Range:** {spell.range}\n"
    spell_markup += f"- **Components:** {spell.components}\n"
    spell_markup += f"- **Duration:** {spell.duration}\n"
    spell_markup += f"___\n"
    spell_markup += f"{spell.description}\n\n"
    spell_markup += f"***At Higher Levels*** {spell.higher_levels_description}\n"

# #### Spell Name
# *Spell Type*
# ___
# - **Casting Time:** Casting Time
# - **Range:** Range
# - **Components:** V, S
# - **Duration:**  Duration
# ___
# A description bursts from the caster's fingers and spreads at the speed of the reader's comprehension.
#
#
