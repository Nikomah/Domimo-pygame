import random


def calc_number_of_entries(ready_to_move: list, robot_list: list) -> dict:
    """
    Calculates occurrences for each digit of the movable digits.
    :param ready_to_move: list, Nominations of bones suitable for running
    :param robot_list: list, Nominations of all robot's bones
    :return: dict, The key is a digit, the value is the number of occurrences
    """
    entries = {}
    move_digits = [x[0] for x in ready_to_move] + [x[1] for x in ready_to_move]
    robot_digits = [x[0] for x in robot_list] + [x[1] for x in robot_list]
    for dig in move_digits:
        entries[dig] = robot_digits.count(dig)
    return entries


def calc_max_entries(ready_to_move: list, robot_list: list) -> set:
    """
    Determines digits with the largest number of occurrences.
    :param ready_to_move: list, Nominations of bones suitable for running
    :param robot_list: list, Nominations of all robot's bones
    :return: set, digits with the largest number of occurrences, once or more
    """
    max_digits = []
    entries = calc_number_of_entries(ready_to_move, robot_list)
    max_entry = max(set(entries.values()))
    for key, value in entries.items():
        if value == max_entry:
            max_digits.append(key)
    return set(max_digits)


def calc_noms_to_move(ready_to_move: list, robot_list: list) -> list:
    """
    Identifies the bones suitable for the move.
    :param ready_to_move: list
    :param robot_list: list
    :return: list
    """
    noms_to_move = []
    digits = calc_max_entries(ready_to_move, robot_list)
    for nom in ready_to_move:
        if nom[0] in digits or nom[1] in digits:
            noms_to_move.append(nom)
    return noms_to_move


def choice_nom_to_move(ready_to_move: list, robot_list: list, dict_nominal: list) -> [tuple, str]:
    """
    Selects a specific dice for the move.
    :param ready_to_move: list
    :param robot_list: list
    :param dict_nominal: list, End denominations on the gaming table
    :return: tuple & str
    """
    bone = None
    flag = None
    noms_to_move = calc_noms_to_move(ready_to_move, robot_list)
    max_digits = calc_max_entries(ready_to_move, robot_list)
    if dict_nominal[0] == dict_nominal[1]:
        return random.choice(noms_to_move), random.choice(['left', 'right'])
    else:
        for nom in noms_to_move:
            if dict_nominal[0] not in max_digits and dict_nominal[0] in nom:
                bone = nom
                flag = 'left'
            elif dict_nominal[1] not in max_digits and dict_nominal[1] in nom:
                bone = nom
                flag = 'right'
        if bone:
            return bone, flag
        else:
            for nom in noms_to_move:
                if dict_nominal[0] in nom:
                    return nom, 'left'
                else:
                    return nom, 'right'
