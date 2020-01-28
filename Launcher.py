#!/usr/bin/env python3
from Controller import Controller


def launch_environment():
    print("At any time if you would like to exit the algorithm, then please type 'Ctrl' + 'C'"
          "in the console")
    controller = Controller()
    controller.trigger_nodes()


if __name__ == "__main__":
    launch_environment()
