# lib/cli.py

from helpers import (
    exit_program,
    view_members,
    get_member,
    view_tasks,
    tasks_by_id

)


def main():
    main_menu()



def main_menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. View family members")
    print("2. View tasks")
    choice = input(">")
    if choice == "0":
        exit_program()
    elif choice == "1":
        view_members()
        family_menu()
    elif choice == "2":
        view_tasks()
        task_menu()
    else:
        print("Invalid choice")
        main_menu()

def family_menu():
    print("please enter the number for the family member you want to select")
    print("0. Back to main menu")
    view_members()
    choice = input(">")
    if choice == "0":
        main_menu()
    else:
        family_member_menu(choice)

def family_member_menu(id):
    get_member(id)
    print("0. Return to main menu")
    print("1. View tasks")
    print("2. Update information")
    print("3. Delete member D:!!!")
    choice = input(">")
    if choice == "0":
        main_menu()
    elif choice == "1":
        tasks_by_id(id)
        family_member_menu(id)
    elif choice == "2":
        ##update_member_info(id)
        family_member_menu(id)
    elif choice == "3":
        ##delete_member(id)
        main_menu()
    else:
        print("Invalid choice")
        family_member_menu(id)

def task_menu():
    pass

if __name__ == "__main__":
    main()
