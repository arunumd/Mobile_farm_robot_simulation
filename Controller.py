#!/usr/bin/env python3
from Input import user_input
from Path import *
from Task import TaskManager


class Controller:
    def __init__(self, world):
        self.world = world
        self.starting_location = "FAR10"
        self.future_location = "FAR00"
        self.future_task = "N/A"
        self.task_node = TaskManager()
        self.planner = Path(self.world)
        while True:
            user_command = input("Please enter a valid starting location for the robot : ")
            self.starting_location = user_input(user_command)[0]
            if self.starting_location != "Invalid task":
                break

    def trigger_nodes(self):
        self.task_node.add_task(self.future_location)
        planned_route = self.planner.find_path(set_locations(self.starting_location, self.task_node.assign_task()))
        while planned_route:
            print(planned_route.popleft())


if __name__ == "__main__":
    command_center = Controller(world=World())
    command_center.trigger_nodes()
