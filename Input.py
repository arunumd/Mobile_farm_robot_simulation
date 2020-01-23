#!/usr/bin/env python3
import re


# TODO Create docstrings
def user_input(task='      go to    field A row 10'):
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
