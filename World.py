import json
import pprint

def load_json_file(input = './maps/coding_challenge.json'):
    with open(input) as json_file:
        data = json.load(json_file)
        pprint.pprint(data)
        for keys in data.keys():
            print(keys)

if __name__ == '__main__':
    load_json_file('./maps/coding_challenge.json')