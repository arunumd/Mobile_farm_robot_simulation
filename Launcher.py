#!/usr/bin/env python3
from modules.Controller import CommandCenter


def launch_environment():
    print("At any time if you would like to exit the algorithm, then please type 'Ctrl' + 'C'"
          "in the console")
    command_center = CommandCenter()
    command_center.trigger_nodes()


if __name__ == "__main__":
    launch_environment()
