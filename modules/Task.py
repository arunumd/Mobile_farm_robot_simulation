#!/usr/bin/env python3
from collections import deque


class TaskManager:
    def __init__(self):
        """
        Description
        -----------
        Initializes a FIFO queue to infinite size
        """
        self.FIFOQueue = deque([], 42)

    def add_task(self, task='FBR10'):
        """
        Description
        -----------
        Function to add tasks from user input to the task manager queue
        :param task: the user input string representing a task
        """
        self.FIFOQueue.append(task)

    def assign_task(self):
        """
        Description
        -----------
        Assigns tasks from the user input to the queue in the form of tuples

        :returns the next task for execution"""
        return self.FIFOQueue.popleft()

    def get_status(self):
        """
        Description
        -----------
        Returns the status of tasks (more tasks left or all the tasks are completed)
        available in the queue

        :returns true if empty; false if not empty"""
        return not self.FIFOQueue
