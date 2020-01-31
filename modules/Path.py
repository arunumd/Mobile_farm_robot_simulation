#!/usr/bin/env python3
import re
from collections import deque

from modules.World import Farm


def set_locations(current_location="FBR01",
                  next_location="Charger"):
    """
    Description:
    -----------
    The following lines of code convert a string containing destination type and location
    into a tuple of string and integer. The string is the destination type and integer is
    the location. Example "FBR01" as (("FBR"),(01))
    :param current_location: Current location of the robot as a string
    :param next_location: Next location of the robot as a string
    :return: A concatenated tuple of current location and next location
    """

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
    return start + finish


class Planner:
    """
    Description:
    -----------
    The class "Planner" is useful for finding a valid path from any valid start location
    to any other end location within the scope of the given farm file
    """

    def __init__(self, farm):
        """The init function saves a local version of the passed in farm file. Since the
        file is passed by reference, any changes made here will update the changes everywhere
        :param farm: The farm file in .json format provided to our algorithm
        """
        self.path = ()
        self.world = farm

    def find_path(self, locations=()):
        """
        Description:
        -----------
        Function to find the shortest path between two locations for the rover. The path
        is selected based on predefined possibilities selection based on euclidean distance.
        :param locations: a concatenated tuple of locations as string and integer pairs
        :return: a deque object of path waypoints as strings
        """
        present_location = list(locations[0:2])
        goal_location = list(locations[2:4])
        # If robot's present location and commanded goto location are exactly the same
        if present_location == goal_location:
            return deque([goal_location[0] + " " + str(goal_location[1])])
        # If start and goals are in the same fields
        elif goal_location[0] == present_location[0]:
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
                present_location[0] != "Charger" and goal_location[0] != "Charger"):
            prefix = present_location[0]

            # Going from field B to field A
            def path_b_to_a(current_coordinate=0, future_coordinate=0, prepend="FBR"):
                """
                Description:
                -----------
                Function to find the path between two fields A and B. In order to provide code reusability,
                the task of going from field a to field b, is considered as inverse of going from field b to
                field a. Accordingly the inputs are flipped and the output path is reversed to get the desired
                path.
                :param prepend: The prefix name that represents the field name and row name
                :param current_coordinate: The current row location in a field as an integer
                :param future_coordinate: The next row location in the other field as an integer
                :return: The path as a deque object of path waypoints as strings
                """
                if current_coordinate != 0:
                    path_ba = deque([prepend + " " + str(i)
                                 for i in (range(current_coordinate, 0, -1))])
                else:
                    path_ba = deque([prepend + " " + str(0)])
                prepend = 'PTH02'
                current_coordinate = 0
                path_ba += (deque([prepend + " " + str(i)
                                   for i in (range(current_coordinate, 11))]))
                prepend = 'FAR'
                current_coordinate = 18
                return path_ba + (deque([prepend + " " + str(i)
                                         for i in (range(current_coordinate, future_coordinate - 1, -1))]))

            if goal_location[0] == 'FAR':
                final_path = path_b_to_a(current_coordinate=present_location[1],
                                         future_coordinate=goal_location[1], prepend=prefix)
                final_path.popleft()
                return final_path
                # Going from field A to field B
            else:
                final_path = path_b_to_a(current_coordinate=goal_location[1],
                                         future_coordinate=present_location[1])
                final_path.reverse()
                final_path.popleft()
                return final_path

        # If robot has to travel from the fields to the charger
        else:

            def path_field_to_charger(current_coordinate=0, origin='FAR', option=0):
                """
                Description:
                -----------
                Function to find the path between a field and the charger. In order to provide code reusability,
                the task of going from field a and field b to charger, is considered as inverse of going from charger
                to field a and field b. Accordingly, the inputs are flipped and the output path is reversed to get the
                desired path.
                :param option: A simple mode selection switch based on value
                :param current_coordinate: The current row location in a field as an integer
                :param origin: The origin field name of the robot
                :return: The path as a deque object of path waypoints as strings
                """
                if option == 0:
                    if current_coordinate != 20:
                        path_to_charger = deque([origin + " " + str(i)
                                             for i in (range(current_coordinate, 20))])
                    else:
                        path_to_charger = deque([origin] + " " + str(20))
                    path_to_charger += deque(
                        [("PTH05" if origin == 'FAR' else "PTH04") + " " + str(i) for i in (range(9, -1, -1))])
                else:
                    if current_coordinate != 0:
                        path_to_charger = deque([origin + " " + str(i)
                                             for i in (range(current_coordinate, -1, -1))])
                    else:
                        path_to_charger = deque([origin + " " + str(0)])
                    path_to_charger += deque(
                        [("PTH03" if origin == 'FAR' else "PTH01") + " " + str(i) for i in (range(9, -1, -1))])

                if origin == 'FAR':
                    return path_to_charger + deque(["PTH00" + " " + str(i) for i in (range(9, -1, -1))])
                else:
                    return path_to_charger

            if goal_location[0] == 'Charger' and (present_location[0] == 'FAR' or present_location[0] == 'FBR'):
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
    path0 = Planner(Farm())
    print(path0.world.path_lengths)
    path1 = path0.find_path(set_locations())
    while path1:
        print(path1.popleft())
