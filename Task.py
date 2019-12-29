import queue


class TaskManager:
    def __init__(self):
        """
        Description
        -----------
        Initializes a FIFO queue to infinite size
        """
        self.FIFOQueue = queue.Queue(maxsize=0)

    def add_task(self, task='goto charger'):
        """
        Description
        -----------
        Function to add tasks from user input to the task manager queue
        :param task: the user input string representing a task
        """
        self.FIFOQueue.put(task)

    def assign_task(self):
        """
        Description
        -----------
        Assigns tasks from the user input to the queue in the form of tuples

        :returns the next task for execution"""
        return self.FIFOQueue.get()

    def get_status(self):
        """
        Description
        -----------
        Returns the status of tasks (more tasks left or all the tasks are completed)
        available in the queue

        :returns true if empty; false if not empty"""
        return self.FIFOQueue.empty()
