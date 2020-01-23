#!/usr/bin/env python3
from Controller import Controller


def launch_environment():
    while True:
        user_command = ""
        try:
            user_command = input("Please enter your command: ")
        except ValueError:
            print("That is not a valid command")
            continue
        finally:
            if user_command.lower().strip() == "exit":
                break


if __name__ == "__main__":
    launch_environment()
