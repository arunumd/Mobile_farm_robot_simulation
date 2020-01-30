#!/usr/bin/env python3
import json
import math
import operator
import re
import time
from functools import reduce


def get_location(nested_dict=None, keys_list=None):
    """
    Description
    -----------
    Static function to get a value of a nested key from a nested dictionary
    :param nested_dict: Nested dictionary from which the nested value is to be retrieved
    :param keys_list: The verbose keys corresponding to the desired value being passed in
                     as a python list of list
    :return: The expected value corresponding to the provided nested keys
    """
    if keys_list is None:
        keys_list = []
    if nested_dict is None:
        nested_dict = {}
    return reduce(operator.getitem, keys_list, nested_dict)


def update_crops(nested_dict=None, keys_list=None, crop="CARROTS"):
    """
    Description
    -----------
    Static function to update a value of a nested key in a nested dictionary
    :param crop: The name of the crop that is to be planted in the specific location
    :param nested_dict: Nested dictionary in which the nested value is to be updated
    :param keys_list: The verbose keys corresponding to the desired value being passed in
                     as a python list of list
    """
    if keys_list is None:
        keys_list = []
    if nested_dict is None:
        nested_dict = {}
    get_location(nested_dict, keys_list[:-1])[keys_list[-1]] = crop


class Farm:
    def __init__(self):
        """
        Description
        -----------
        Function to load a json farm map to a nested dictionary. The file is repeatedly attempted to
        be opened and loaded if the file does not exist in the given location. The initializer function
        also calculates the lengths of all paths and fields using the data available in the predefined
        farm map. The lengths of irregular paths are calculated using the euclidean distance formula
        """
        self.json_path = ''
        status = 0
        while status == 0:
            try:
                self.json_path = input("Please enter the world file path : ")
                with open(self.json_path) as json_file:
                    self.data = json.load(json_file)
            except:
                print("The said world file does not exist. Please enter a valid path again")
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

    def decrypt_location(self, location="Charger"):
        """
        Description
        -----------
        Member function to return the exact location coordinates of a specific location of the robot based
        on path waypoint numbers and row numbers in the two given fields
        :param location: The location of the robot in the form of a string. Example: Charger, FBR10, etc.
        :return: The location coordinates as a string. Example: [300, 500], [1000, 50], etc.
        """
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
        """
        Description
        -----------
        Member function to plant a crop in the farm file at the desired field and row location
        :param location: An encoded name of the field and row location passed in as a string
        :param crop: The name of the crop to be planted passed in as a string
        """
        if re.match(r'(\s)*FBR(\s)*\d+', location, re.IGNORECASE):
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            crop_key = ["world", "fields", "field-b", "rows", "row-" + str(output), "crop"]
            update_crops(self.data, crop_key, crop)
        else:
            output = "{0:0=2d}".format(int((re.findall(r'\d+', location))[0]))
            crop_key = ["world", "fields", "field-a", "rows", "row-" + str(output), "crop"]
            update_crops(self.data, crop_key, crop)

    def write_to_world_file(self):
        """
        Description
        -----------
        Member function to write the current farm file to the given json file. The function simply opens the json
        file which is initialized by the __init__ function and then writes the stored dictionary to the file and
        closes it
        """
        with open(self.json_path, "w+") as world_file:
            world_file.write(json.dumps(self.data))


if __name__ == '__main__':
    start = time.time()
    print(Farm().decrypt_location())
    end = time.time()
    time_taken = end - start
    print('Time: ', time_taken)
