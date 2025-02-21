# lib/cli.py

from helpers import (
    exit_program,
    view_members
)


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            view_members()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View family members")
    print("2. View tasks")


if __name__ == "__main__":
    main()
