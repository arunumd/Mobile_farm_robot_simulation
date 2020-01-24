#!/usr/bin/env python3
import re

from collections import deque
from World import World


def set_locations(current_location="FBR01",
                  next_location="Charger"):
    def get_tuple(location="FBR01"):
        # Code for current location matches
        if re.match(r'FBR\d+', location):
            location_tuple = ("FBR", int((re.findall(r'\d+', location))[0]))
        elif re.match(r'FAR\d+', location):
            location_tuple = ("FAR", int((re.findall(r'\d+', location))[0]))
        else:
            location_tuple = ("Charger", 0)
        return location_tuple

    start = get_tuple(current_location)
    finish = get_tuple(next_location)
    print(start, finish)
    return start + finish


class Path:
    def __init__(self, world):
        self.path = ()
        self.world = world

    def find_path(self, locations=()):
        present_location = list(locations[0:2])
        goal_location = list(locations[2:4])  # If start and goals are in the same fields
        print(present_location, goal_location)
        if goal_location[0] == present_location[0]:
            """
            Description:
            -----------
            Condition to find path when the goal node and current node are in the same field
            """
            if goal_location[0] == 'FBR' or goal_location[0] == 'FAR':
                prefix = goal_location[0]
                # Goal row is higher than present row
                if int(goal_location[1]) - int(present_location[1]) >= 0:
                    return deque([prefix + " " + str(i)
                                  for i in (range(present_location[1] + 1, goal_location[1] + 1))])
                else:
                    return deque([prefix + " " + str(i)
                                  for i in (range(present_location[1] - 1, goal_location[1] - 1, -1))])

        # If start and goals are in different fields
        elif (goal_location[0] == 'FAR' or 'FBR') and (present_location[0] == 'FAR' or 'FBR') and (
                present_location[0] is not "Charger" and goal_location[0] is not "Charger"):
            prefix = present_location[0]

            # Going from field B to field A
            def path_b_to_a(current_coordinate=0, future_coordinate=0, prepend="FBR"):
                path_ba = deque([prepend + " " + str(i)
                                 for i in (range(current_coordinate, 0, -1))])
                prepend = 'PTH02'
                current_coordinate = 0
                path_ba += (deque([prepend + " " + str(i)
                                   for i in (range(current_coordinate, 11))]))
                prepend = 'FAR'
                current_coordinate = 18
                return path_ba + (deque([prepend + " " + str(i)
                                         for i in (range(current_coordinate, future_coordinate - 1, -1))]))

            if goal_location[0] == 'FAR':
                print(present_location, goal_location)
                final_path = path_b_to_a(current_coordinate=present_location[1],
                                         future_coordinate=goal_location[1], prepend=prefix)
                final_path.popleft()
                return final_path
                # Going from field A to field B
            else:
                print(present_location, goal_location)
                final_path = path_b_to_a(current_coordinate=goal_location[1],
                                         future_coordinate=present_location[1])
                final_path.reverse()
                final_path.popleft()
                return final_path

        # If robot has to travel from the fields to the charger
        else:

            def path_field_to_charger(current_coordinate=0, origin='FAR', option=0):
                if option == 0:
                    path_to_charger = deque([origin + " " + str(i)
                                             for i in (range(current_coordinate, 19))])
                    path_to_charger += deque(
                        [("PTH05" if origin == 'FAR' else "PTH04") + " " + str(i) for i in (range(10, -1, -1))])
                else:
                    path_to_charger = deque([origin + " " + str(i)
                                             for i in (range(current_coordinate, 0, -1))])
                    path_to_charger += deque(
                        [("PTH03" if origin == 'FAR' else "PTH01") + " " + str(i) for i in (range(10, -1, -1))])

                if origin == 'FAR':
                    return path_to_charger + deque(["PTH00" + " " + str(i) for i in (range(10, -1, -1))])
                else:
                    return path_to_charger

            if goal_location[0] == 'Charger' and (present_location[0] == 'FAR' or present_location[0] == 'FBR'):
                print("start is field ", present_location, goal_location)
                if present_location[0] == 'FAR':
                    # Go by path 5 if going by path 3 is longer
                    if self.world.path_lengths[3] + present_location[1] - 1 > \
                            self.world.path_lengths[5] + 19 - present_location[1]:
                        final_path = path_field_to_charger(present_location[1])
                        final_path.popleft()
                        return final_path
                    # Otherwise go by path 3
                    else:
                        final_path = path_field_to_charger(present_location[1], option=1)
                        final_path.popleft()
                        return final_path
                else:
                    if self.world.path_lengths[1] + present_location[1] - 1 > \
                            self.world.path_lengths[4] + 19 - present_location[1]:
                        final_path = path_field_to_charger(present_location[1], origin='FBR')
                        final_path.popleft()
                        return final_path
                    # Otherwise go by path 3
                    else:
                        final_path = path_field_to_charger(present_location[1], origin='FBR', option=1)
                        final_path.popleft()
                        return final_path

            else:
                print("start is charger ", present_location, goal_location)
                if goal_location[0] == 'FAR':
                    if self.world.path_lengths[3] + goal_location[1] - 1 > \
                            self.world.path_lengths[5] + 19 - goal_location[1]:
                        mirror_path = path_field_to_charger(goal_location[1])
                        mirror_path.reverse()
                        mirror_path.popleft()
                        return mirror_path
                    else:
                        mirror_path = path_field_to_charger(goal_location[1], option=1)
                        mirror_path.reverse()
                        mirror_path.popleft()
                        return mirror_path
                else:
                    if self.world.path_lengths[1] + goal_location[1] - 1 > \
                            self.world.path_lengths[4] + 19 - goal_location[1]:
                        mirror_path = path_field_to_charger(goal_location[1], origin='FBR')
                        mirror_path.reverse()
                        mirror_path.popleft()
                        return mirror_path
                    else:
                        mirror_path = path_field_to_charger(goal_location[1], origin='FBR', option=1)
                        mirror_path.reverse()
                        mirror_path.popleft()
                        return mirror_path


if __name__ == "__main__":
    path0 = Path(World())
    print(path0.world.path_lengths)
    path1 = path0.find_path(set_locations())
    while path1:
        print(path1.popleft())
