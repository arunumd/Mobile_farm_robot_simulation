#!/usr/bin/env python3
import re


def user_input(task='      go to    field A row 10'):
    """
    Description
    -----------
    Static function to convert an irregular user input into a regular encoded input for the path
    planning algorithm. The function returns an "Invalid task" if the commanded robot position is
    out of scope of the farm file
    :param task: An irregular user input which may be of irregular spacing and case.
                 Example: go to fieLd a ROw 10
    :return: A regularized encoded string of the commanded location for the robot. Example: FAR10
    """
    match_templates = [r'\s*go\s*to\s*field\s*A\s*row\s*(\d+)\s*',
                       r'\s*go\s*to\s*field\s*B\s*row\s*(\d+)\s*',
                       r'\s*plant\s*(.*?)\s*in\s*field\s*A\s*row\s*(\d+)\s*',
                       r'\s*plant\s*(.*?)\s*in\s*field\s*B\s*row\s*(\d+)\s*',
                       r'\s*go\s*to\s*charger\s*']

    # Condition to check if the robot has to go to somewhere in field A
    match_state = re.match(match_templates[0], task, re.IGNORECASE)
    if match_state is not None:
        return "FAR" + str(match_state[1]), "N/A"

    # Condition to check if the robot has to go to somewhere in field B
    match_state = re.match(match_templates[1], task, re.IGNORECASE)
    if match_state is not None:
        return "FBR" + str(match_state[1]), "N/A"

    # Condition to check if the robot has to plant some crop in field A
    match_state = re.match(match_templates[2], task, re.IGNORECASE)
    if match_state is not None:
        return "FAR" + str(match_state[2]), match_state[1]

    # Condition to check if the robot has to plant some crop in field B
    match_state = re.match(match_templates[3], task, re.IGNORECASE)
    if match_state is not None:
        return "FBR" + str(match_state[2]), match_state[1]

    # Condition to check if the robot has to go to charger
    match_state = re.match(match_templates[4], task, re.IGNORECASE)
    if match_state is not None:
        return "Charger", "N/A"

    else:
        return "Invalid task", "N/A"
