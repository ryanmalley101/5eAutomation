from playercharacters.pc_datastructs import *
import pandas as pd
import numpy as np

def convert_subclass(subclass:Subclass):
    def ordinal(n: int):
        if 11 <= (n % 100) <= 13:
            suffix = 'th'
        else:
            suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
        return str(n) + suffix

    subclass_string =  f"### {subclass.name}\n"
    subclass_string += f"{subclass.description}\n\n"
    for ability in subclass.abilities:
        subclass_string += f"#### {ability.name}\n"
        subclass_string += f"*{ordinal(ability.class_level)}-level {subclass.name} feature*\n"
        subclass_string += f"___\n"
        subclass_string += f"{ability.description}\n\n"

    return subclass_string

def convert_subclass_excel():
    subclass_excel = pd.read_excel('Subclasses.xlsx', sheet_name='Sheet1', header=0)
    subclass_excel = subclass_excel.replace(np.nan, None)
    subclass_list = []
    for index, row in subclass_excel.iterrows():
        subclass_name = row['Name']
        class_name = ClassName(row['Class'])
        description = "" if row['Description'] is None else row['Description']
        ability_list = []
        if row['Feature 1A Name'] is not None:
            ability_list.append({"name": row['Feature 1A Name'], "description": row['Feature 1A Description'], "level": 0})
        if row['Feature 1B Name'] is not None:
            ability_list.append({"name": row['Feature 1B Name'], "description": row['Feature 1B Description'], "level": 0})
        if row['Feature 2A Name'] is not None:
            ability_list.append(
                {"name": row['Feature 2A Name'], "description": row['Feature 2A Description'], "level": 1})
        if row['Feature 2B Name'] is not None:
            ability_list.append(
                {"name": row['Feature 2B Name'], "description": row['Feature 2B Description'], "level": 1})
        if row['Feature 3A Name'] is not None:
            ability_list.append(
                {"name": row['Feature 3A Name'], "description": row['Feature 3A Description'], "level": 2})
        if row['Feature 3B Name'] is not None:
            ability_list.append(
                {"name": row['Feature 3B Name'], "description": row['Feature 3B Description'], "level": 2})
        if row['Feature 4A Name'] is not None:
            ability_list.append(
                {"name": row['Feature 4A Name'], "description": row['Feature 4A Description'], "level": 3})
        if row['Feature 4B Name'] is not None:
            ability_list.append(
                {"name": row['Feature 4B Name'], "description": row['Feature 4B Description'], "level": 3})
        if row['Feature 5A Name'] is not None:
            ability_list.append(
                {"name": row['Feature 5A Name'], "description": row['Feature 5A Description'], "level": 4})
        if row['Feature 5B Name'] is not None:
            ability_list.append(
                {"name": row['Feature 5B Name'], "description": row['Feature 5B Description'], "level": 4})
        subclass = Subclass.convert_excel_template_subclass(subclass_name, class_name, description, ability_list)
        subclass_list.append(subclass)

    last_subclass = ClassName.UNKNOWN
    for subclass in subclass_list:
        if last_subclass != subclass.associated_class:
            print(f'## {subclass.associated_class.value}\n')
            last_subclass = subclass.associated_class
        print(convert_subclass(subclass))

if __name__ == '__main__':
    convert_subclass_excel()
