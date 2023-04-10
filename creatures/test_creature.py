import creature_datastructs
from creature_gmbinder_convert import *
from creature_generator import generate_test_creature
import unittest

class TestCreature(unittest.TestCase):
    def test_json_convert(self):
        generated_monster = generate_test_creature()
        filename = 'testmonster'
        generated_monster.save_json_to_file(filename='testmonster')

        post_json_monster = MonsterStatblock.load_json_from_file(filename=filename+'.json')
        for attr, value in generated_monster.__dict__.items():
            oldvalue = value
            newvalue = post_json_monster.__dict__[attr]
            if oldvalue != newvalue:
                print(f"Old Object: {attr}, {oldvalue}\n"
                      f"New Object: {attr}, {newvalue}")

        self.assertEqual(generated_monster.__dict__.items() ^ post_json_monster.__dict__.items(), set())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    unittest.main()
