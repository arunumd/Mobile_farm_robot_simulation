#!/usr/bin/env python3
import re


def user_input(task='      go to    field A row 10'):
    """
    Description
    -----------
    Static function to convert an irregular user input into a regular encoded input for the path
    planning algorithm. The function returns an "Invalid task" if the commanded robot position is
    out of scope of the world file
    :param task: An irregular user input which may be of irregular spacing and case.
                 Example: go to fieLd a ROw 10
    :return: A regularized encoded string of the commanded location for the robot. Example: FAR10
    """
    # Command to check if task is for field A
    if re.match(r'(\s)*go(\s)*to(\s)*field(\s)*A(\s)*row(\s)*\d+(\s)*',
                task, re.IGNORECASE):
        output = int((re.findall(r'\d+', task))[0])
        if 0 <= output < 20:
            return "FAR" + str(output), "N/A"

    # Command to check if task is for field B
    if re.match(r'(\s)*go(\s)*to(\s)*field(\s)*B(\s)*row(\s)*\d+(\s)*',
                task, re.IGNORECASE):
        output = int((re.findall(r'\d+', task))[0])
        if 0 <= output < 20:
            return "FBR" + str(output), "N/A"

    # Command to check if task is to plant crops in field A
    if re.match(r'(\s)*plant(\s)*\w*(\s)*in(\s)*field(\s)*A(\s)*row(\s)*\d+(\s)*',
                task, re.IGNORECASE):
        cleaned_input = (re.split(r'\s', task.strip()))
        return "FAR" + str(cleaned_input[6]), cleaned_input[1]

    # Command to check if task is to plant crops in field B
    if re.match(r'(\s)*plant(\s)*\w*(\s)*in(\s)*field(\s)*B(\s)*row(\s)*\d+(\s)*',
                task, re.IGNORECASE):
        cleaned_input = (re.split(r'\s', task.strip()))
        return "FBR" + str(cleaned_input[6]), cleaned_input[1]

    # Command to check if task is for charger
    if re.match(r'(\s)*go(\s)*to(\s)*charger(\s)*', task, re.IGNORECASE):
        return "Charger", "N/A"

    else:
        return "Invalid task", "N/A"


print(user_input())
