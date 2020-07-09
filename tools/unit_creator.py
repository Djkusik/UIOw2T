import json
import os
from typing import List, Dict, TextIO

path_to_units_file: str = './../backend/game/data/units.json'
classes: Dict = {
    '1': 'Warrior',
    '2': 'Mage',
    '3': 'Archer'
}


def read_json(file: TextIO) -> List[Dict]:
    return json.load(file)


def create_json(content: List[Dict]) -> str:
    return json.dumps(content)


def print_content(content: List[Dict]) -> None:
    for idx, unit in enumerate(content):
        print(f"Unit {idx}: ")
        for key in unit:
            if key != 'statistics':
                print(f"\t{key.capitalize()}: {unit[key]}")
        print('\tStatistics:')
        stats_sum = 0
        for stat in unit['statistics']:
            print(f"\t\t{stat.capitalize()}: {unit['statistics'][stat]}")
            if stat != 'base_hp':
                stats_sum += unit['statistics'][stat]
        print(f"Overall stats sum (without health): {stats_sum}")


def query_yes_no(question: str, default: str = "yes") -> bool:
    valid = {
        "yes": True, "y": True, "ye": True,
        "no": False, "n": False
    }

    if default is None:
        prompt = " [y/n]: "
    elif default == "yes":
        prompt = " [Y/n]: "
    elif default == "no":
        prompt = " [y/N]: "
    else:
        raise ValueError(f"Invalid default answer: {default}")

    while True:
        choice = input(question + prompt)
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no'")


def adding_loop(content: List[Dict]) -> None:
    while True:
        if not query_yes_no("Do You want to add unit?"):
            break
        content.append(add_unit())


def add_unit() -> Dict:
    while True:
        name = input("Name: ")
        while True:
            category = int(input("Category [1. Warrior 2. Mage 3. Archer]: "))
            if category in range(1, 4):
                break

        base_hp = int(input("Base hp: "))
        base_phys_attack = int(input("Base physical attack: "))
        base_phys_defence = int(input("Base physical defence: "))
        base_mag_attack = int(input("Base magical attack: "))
        base_mag_defence = int(input("Base magical defence: "))
        base_speed = int(input("Base speed: "))
        base_reach = int(input("Base reach: "))

        print(f"Name: {name}\nCategory: {classes[str(category)]}\nBase hp: {base_hp}")
        print(f"Base physical attack: {base_phys_attack}\nBase physical defence: {base_phys_defence}")
        print(f"Base magical attack: {base_mag_attack}\nBase magical defence: {base_mag_defence}")
        print(f"Base speed: {base_speed}\nBase reach: {base_reach}\n")
        print(f"Overall stats: {base_phys_attack + base_phys_defence + base_mag_attack + base_mag_defence + base_speed + base_reach}")

        if query_yes_no("Do You want to add this unit?"):
            break

    return {
        "name": name,
        "category": classes[str(category)],
        "statistics": {
            "base_hp": base_hp,
            "base_phys_attack": base_phys_attack,
            "base_phys_defence": base_phys_defence,
            "base_mag_attack": base_mag_attack,
            "base_mag_defence": base_mag_defence,
            "base_speed": base_speed,
            "base_reach": base_reach
        }
    }


def main():
    with open(path_to_units_file, 'r+') as units_file:
        content = read_json(units_file) if os.stat(path_to_units_file).st_size != 0 else []
        adding_loop(content)
        if query_yes_no("Do You want to print all units?"):
            print_content(content)
        if query_yes_no("Save to file?"):
            content = create_json(content)
            try:
                units_file.seek(0)
                units_file.write(content)
                units_file.truncate()
                print("File saved!")
            except Exception as err:
                print(err)


if __name__ == '__main__':
    main()
