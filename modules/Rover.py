#!/usr/bin/env python3
import datetime
import threading
import time
from collections import deque

from modules.World import Farm


class Farmer:
    def __init__(self, farm, initial_location="FBR01"):
        """
        Description
        -----------
        Initializer function to initialize the robot at a commanded initial position
        :param farm: An instantiation of the Farm class passed in as a Python object
        :param initial_location: The initial position of the robot being passed in from external location
        """
        self.rover_location = [0, 0]
        self.world = farm
        self.path = deque([], 1000)
        self.time_interval = 1.0
        self.rover_location = initial_location

    def append_path(self, queue=deque([], 50)):
        """Member function to concatenate a newly found path with the existing path. The path objects are deque objects
        :param queue: A newly found path for the next go to location of the robot in the form of a deque object
        """
        self.path += queue

    def get_location(self):
        """Member function to convert the encrypted location to a human understandable form for displaying and other
        purposes
        """
        decrypted_state = self.world.decrypt_location(self.rover_location)
        print(datetime.datetime.now().second, decrypted_state[0], decrypted_state[1])

    def walk(self):
        """A walker function to continuously walk the robot through the available path waypoints every one second.
        The time difference between two successive steps of the robot is calculated based on the time taken to
        execute the task itself in order to compensate for the drift
        """
        next_call = time.time()
        while True:
            try:
                if self.path[0].startswith(("FAR", "FBR", "Cha", "PTH0")):
                    current_location = self.path.popleft()
                    if self.rover_location != current_location:
                        self.rover_location = current_location
                        self.get_location()
                else:
                    crop = self.path.popleft()
                    self.world.update_world(self.rover_location, crop)
                    self.world.write_to_world_file()
                    print(datetime.datetime.now().second, self.world.decrypt_location(self.rover_location)[0],
                          "[", crop, "] successfully planted")
            except IndexError:
                pass
            next_call = next_call + self.time_interval
            time.sleep(next_call - time.time())


if __name__ == "__main__":
    rover = Farmer(Farm())
    timerThread = threading.Thread(target=rover.walk)
    timerThread.start()
    rover.path.append("FBR10")
