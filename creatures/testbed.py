from creature_datastructs import *
from creature_gmbinder_convert import *
from creature_generator import generate_test_creature

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    generated_monster = generate_test_creature()
    monster_json = generated_monster.to_json()
    post_json_monster = CreatureStatblock().load_json(json.loads(monster_json))
    for attr, value in generated_monster.__dict__.items():
        oldvalue = value
        newvalue = post_json_monster.__dict__[attr]
        if oldvalue != newvalue:
            print(f"Old Object: {attr}, {oldvalue}\n"
                  f"New Object: {attr}, {newvalue}")

    assert generated_monster == post_json_monster
    generated_monster.save_json()
    # print(convert_monster(generated_monster))
