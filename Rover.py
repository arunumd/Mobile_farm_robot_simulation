#!/usr/bin/env python3
from World import World


class Rover:
    def __init__(self, world):
        self.rover_location = [0, 0]
        self.world = world

    def update_location(self, location="FBR08"):
        self.rover_location = self.world.decrypt_location(location)
        return self.rover_location


if __name__ == "__main__":
    rover = Rover(World())
    rover.update_location("FBR08")
