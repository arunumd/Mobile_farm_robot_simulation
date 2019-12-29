import json
import pprint


# TODO Create docstrings
class World:
    def load_json_file(input = './maps/coding_challenge.json'):
        """
        Description
        -----------
        Function to load a json world map to a nested dictionary
        :param input: Input json file path for loading world map
        """
        with open(input) as json_file:
            data = json.load(json_file)
            pprint.pprint(data)

if __name__ == '__main__':
    World.load_json_file()
