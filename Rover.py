#!/usr/bin/env python3
import datetime
import threading
import time

from collections import deque
from World import World


class Rover:
    def __init__(self, world, initial_location="FBR01"):
        self.rover_location = [0, 0]
        self.world = world
        self.path = deque([], 1000)
        self.time_interval = 1.0
        self.rover_location = initial_location

    def append_path(self, queue=deque([], 50)):
        self.path += queue

    def get_location(self):
        decrypted_state = self.world.decrypt_location(self.rover_location)
        print(datetime.datetime.now().second, decrypted_state[0], decrypted_state[1])

    def walk(self):
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
            next_call = next_call + 1
            time.sleep(next_call - time.time())


if __name__ == "__main__":
    rover = Rover(World())
    timerThread = threading.Thread(target=rover.walk)
    timerThread.start()
    rover.path.append("FBR10")
