#!/usr/bin/env python3
import json
import math
import re
import operator
import time

from functools import reduce


def get_location(nested_dict=None, keys_list=None):
    if keys_list is None:
        keys_list = []
    if nested_dict is None:
        nested_dict = {}
    return reduce(operator.getitem, keys_list, nested_dict)


# TODO Create docstrings
class World:
    def __init__(self):
        """
        Description
        -----------
        Function to load a json world map to a nested dictionary
        :param self.json_path: Input json file path for loading world map
        """
        self.json_path = './maps/coding_challenge.json'
        status = 0
        while status == 0:
            try:
                with open(self.json_path) as json_file:
                    self.data = json.load(json_file)
            except FileNotFoundError:
                print("The file  ./maps/coding_challenge.json does not exist\n"
                      "Retrying to load the same file again")
            else:
                status = 1

        # Calculate the lengths of paths
        self.field_a_length = self.data['world']['fields']['field-a']['rows']['row-00']['location'][1] - \
                              self.data['world']['fields']['field-a']['rows']['row-19']['location'][1]
        self.row_spacing_field_a = self.field_a_length / 19
        self.field_b_length = self.data['world']['fields']['field-b']['rows']['row-00']['location'][1] - \
                              self.data['world']['fields']['field-b']['rows']['row-19']['location'][1]
        self.row_spacing_field_b = self.field_b_length / 19
        self.path_lengths = []

        for path in self.data['world']['paths'].items():
            self.path_lengths.append(
                10 * math.sqrt((math.pow(path[1]['waypoint-0'][0] - path[1]['waypoint-1'][0], 2)) +
                               (math.pow(path[1]['waypoint-0'][1] - path[1]['waypoint-1'][1], 2))))
        for item in self.path_lengths:
            print(item)

    def decrypt_location(self, location="FBR8"):
        print(location)
        if re.match(r'(\s)*charger(\s)*', location, re.IGNORECASE):
            return self.data['world']['charger']['location']
        elif re.match(r'(\s)*FBR(\s)*\d+', location, re.IGNORECASE):
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            key = ["world", "fields", "field-b", "rows", "row-" + str(output), "location"]
            return get_location(self.data, key)
        else:
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            key = ["world", "fields", "field-a", "rows", "row-" + str(output), "location"]
            return get_location(self.data, key)


if __name__ == '__main__':
    start = time.time()
    print(World().decrypt_location())
    end = time.time()
    time_taken = end - start
    print('Time: ', time_taken)
