import dataclasses
from enum import Enum
from dataclasses import dataclass, field, asdict
import json
import time

class SpellSchools(Enum):
    ABJURATION = "abjuration"
    CONJURATION = "conjuration"
    DIVINATION = "divination"
    ENCHANTMENT = "enchantment"
    EVOCATION = "evocation"
    ILLUSION = "illusion"
    NECROMANCY = "necromancy"
    TRANSMUTATION = "transmutation"


@dataclass
class SpellDescription:
    name: str = "PLACEHOLDER"
    level: int = 10
    school: SpellSchools = SpellSchools.ABJURATION
    casting_time: str = "1 action"
    range: str = "touch"
    components: str = "V, S, M (a tiny ball of bat guano and sulfur)"
    duration: str = "instantaneous"
    description: str = "this is a default spell description"
    higher_levels_description: str = "When you cast this spell using a spell" \
                                     " slot of 4th level or higher, it does " \
                                     "nothing for each slot level above 3rd."

    def to_json(self):
        spell_dict = asdict(self)
        spell_dict['school'] = self.school.value
        print(spell_dict)
        return json.dumps(spell_dict)

    def load_json(self, spell_json):
        spell = SpellDescription(name=spell_json['name'],
                                 level=int(spell_json['level']),
                                 school=SpellSchools(spell_json['school']),
                                 casting_time=spell_json['casting_time'],
                                 range=spell_json['range'],
                                 components=spell_json['components'],
                                 duration=spell_json['duration'],
                                 description=spell_json['description'],
                                 higher_levels_description=
                                 spell_json['higher_levels_description'])
        return spell

    def save_json(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        spell_json = open('spell ' + timestr + '.json', "w")
        n = spell_json.write(self.to_json())
        print(n)
        spell_json.close()
