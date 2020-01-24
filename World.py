#!/usr/bin/env python3
import json
import math
import re
import operator
import time
import pprint

from functools import reduce


def get_location(nested_dict=None, keys_list=None):
    if keys_list is None:
        keys_list = []
    if nested_dict is None:
        nested_dict = {}
    return reduce(operator.getitem, keys_list, nested_dict)


def update_crops(nested_dict=None, keys_list=None, crop="CARROTS"):
    if keys_list is None:
        keys_list = []
    if nested_dict is None:
        nested_dict = {}
    get_location(nested_dict, keys_list[:-1])[keys_list[-1]] = crop


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
                    pprint.pprint(self.data)
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

    def decrypt_location(self, location="Charger"):
        if re.match(r'(\s)*charger(\s)*', location, re.IGNORECASE):
            return "[charger]", self.data['world']['charger']['location']
        elif re.match(r'(\s)*PTH(\s)*\d+', location, re.IGNORECASE):
            output = (re.findall(r'\d+', location))
            path_number = int(output[0])
            waypoint_number = int(output[1])
            location_key = ["world", "paths", "path-" + str(path_number), "waypoint-" + str(waypoint_number)]
            return "[path-" + str(path_number) + "]", get_location(self.data, location_key)
        else:
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            location_key = ["world", "fields",
                            "field-b" if re.match(r'(\s)*FBR(\s)*\d+', location, re.IGNORECASE) else "field-a", "rows",
                            "row-" + str(output), "location"]
            return "[" + str(location_key[2]) + "]" + "[" + str(location_key[4]) + "]", get_location(self.data,
                                                                                                     location_key)

    def update_world(self, location="FBR8", crop="CARROTS"):
        if re.match(r'(\s)*FBR(\s)*\d+', location, re.IGNORECASE):
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            crop_key = ["world", "fields", "field-b", "rows", "row-" + str(output), "crop"]
            update_crops(self.data, crop_key, crop)
        else:
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            crop_key = ["world", "fields", "field-a", "rows", "row-" + str(output), "crop"]
            update_crops(self.data, crop_key, crop)

    def write_to_world_file(self):
        world_file = open(self.json_path, "w+")
        world_file.write(json.dumps(self.data))
        world_file.close()


if __name__ == '__main__':
    start = time.time()
    print(World().decrypt_location())
    end = time.time()
    time_taken = end - start
    print('Time: ', time_taken)
