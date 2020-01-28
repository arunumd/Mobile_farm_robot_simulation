#!/usr/bin/env python3
import threading

from Input import user_input
from Path import *
from Rover import Rover
from Task import TaskManager
from World import World


class Controller:
    def __init__(self):
        """
        Description:
        -----------
        Initializer function for controller class. The function initializes the initial position of the robot
        through user input. The function also initializes other variables necessary for the functioning of the class.
        The world file is being initialized as a composition object from the json file path. It is a nested dictionary
        """
        self.world = World()
        self.starting_location = "FAR10"
        self.future_location = "Charger"
        self.current_task = "N/A"
        self.future_task = "N/A"
        self.task_node = TaskManager()
        self.planner = Path(self.world)
        while True:
            user_command = input("Please enter a valid starting location for the robot : ")
            self.starting_location = user_input(user_command)[0]
            if self.starting_location != "Invalid task":
                break

    def trigger_nodes(self):
        """
        Description:
        -----------
        This function is the lifeline of the whole pipeline. It does the essential task of integrating all
        other modules together, viz-a-viz., Input, Path, Task, World, etc. to get the rover up and running.
        The function helps to get the next robot location through user input as a string and then run the
        Input module for parsing its meaning. Later, the input module allocates an encoded task to the Task
        module if the command was a valid command. The task module allocates the tasks to the path module
        sequentially and appends the found path to the Rover class instance. The Rover class then takes care
        of the job of walking the rover through every individual waypoint in sequence for every one second.
        """
        task_manager = TaskManager()
        path_planner = Path(self.world)
        rover = Rover(self.world, self.starting_location)
        timer_thread = threading.Thread(target=rover.walk)
        timer_thread.start()
        while True:
            status = 0
            while status == 0:
                next_task = input("Please enter a valid next task for the robot : ")
                task_location = user_input(next_task)
                if task_location[0] != "Invalid task":
                    self.future_location = task_location[0]
                    self.future_task = task_location[1]
                    status = 1
            task_manager.add_task(self.future_location)
            planned_path = path_planner.find_path(set_locations(self.starting_location, task_manager.assign_task()))
            if self.future_task != "N/A":
                planned_path.append(self.future_task)
            rover.append_path(planned_path)
            self.starting_location = self.future_location


if __name__ == "__main__":
    controller = Controller()
    controller.trigger_nodes()
