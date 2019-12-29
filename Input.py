import re


# TODO Create docstrings
class Input:
    def user_input(input = 'plant CARROTS in field A row 10'):
        # Command to check if task is for field A
        field_a_command = re.compile(r'goto field A row \d')
        output = field_a_command.search(input)
        if 0 <= int(output) < 20:
            pass
            # TODO : Write code for A row command here
            # Should update task queue in task.py

        # Command to check if task is for field B
        field_b_command = re.compile(r'goto field B row \d')
        output = field_b_command.search(input)
        if 0 <= int(output) < 20:
            pass
            # TODO : Write code for B row command here
            # Should update task queue in task.py

        # Command to check if task is for charger
        charger_command = re.compile(r'goto charger')
        output = charger_command.search(input)
        if output is not None:
            pass
            # TODO : Write code for charger command here
            # Should update task queue in task.py
