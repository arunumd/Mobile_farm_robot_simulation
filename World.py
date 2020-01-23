#!/usr/bin/env python3
import json
import math


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


if __name__ == '__main__':
    World()
